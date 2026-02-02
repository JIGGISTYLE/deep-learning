#!/usr/bin/env python3
"""Create a git commit without requiring the `git` binary.

Usage: run this from the repository root:
  python scripts/git_commit_no_git.py "Commit message"

This script writes blob/tree/commit objects into .git and updates the current branch ref.
It intentionally keeps things minimal and should be used with care.
"""
import hashlib
import os
import sys
import time
import zlib


def repo_root():
    return os.getcwd()


def git_dir(root):
    return os.path.join(root, '.git')


def read_head(gd):
    head_path = os.path.join(gd, 'HEAD')
    with open(head_path, 'r', encoding='utf-8') as f:
        data = f.read().strip()
    if data.startswith('ref: '):
        ref = data.split('ref: ', 1)[1]
        return ('ref', ref)
    else:
        return ('sha', data)


def read_ref(gd, ref):
    ref_path = os.path.join(gd, ref.replace('/', os.sep))
    if os.path.exists(ref_path):
        with open(ref_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None


def write_ref(gd, ref, sha):
    ref_path = os.path.join(gd, ref.replace('/', os.sep))
    d = os.path.dirname(ref_path)
    os.makedirs(d, exist_ok=True)
    with open(ref_path, 'w', encoding='utf-8') as f:
        f.write(sha + '\n')


def write_object(gd, obj_type, data_bytes):
    header = f"{obj_type} {len(data_bytes)}\0".encode('utf-8')
    full = header + data_bytes
    sha = hashlib.sha1(full).hexdigest()
    obj_dir = os.path.join(gd, 'objects', sha[:2])
    obj_path = os.path.join(obj_dir, sha[2:])
    if not os.path.exists(obj_path):
        os.makedirs(obj_dir, exist_ok=True)
        with open(obj_path, 'wb') as f:
            f.write(zlib.compress(full))
    return sha


def build_blob(gd, path):
    with open(path, 'rb') as f:
        content = f.read()
    return write_object(gd, 'blob', content)


def build_tree(gd, root, prefix=''):
    entries = []
    full_dir = os.path.join(root, prefix) if prefix else root
    for name in sorted(os.listdir(full_dir)):
        if prefix == '' and name == '.git':
            continue
        path = os.path.join(full_dir, name)
        rel_path = os.path.join(prefix, name) if prefix else name
        if os.path.isdir(path):
            tree_sha = build_tree(gd, root, rel_path)
            entries.append(('40000', name, tree_sha))
        else:
            blob_sha = build_blob(gd, path)
            entries.append(('100644', name, blob_sha))

    # build tree content
    content = b''
    for mode, name, sha in entries:
        mode_name = f"{mode} {name}".encode('utf-8') + b"\0"
        sha_bytes = bytes.fromhex(sha)
        content += mode_name + sha_bytes

    tree_sha = write_object(gd, 'tree', content)
    return tree_sha


def get_user_info(gd):
    # Try to read from .git/config
    cfg_path = os.path.join(gd, 'config')
    name = None
    email = None
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('name = '):
                        name = line.split('=', 1)[1].strip()
                    if line.startswith('email = '):
                        email = line.split('=', 1)[1].strip()
        except Exception:
            pass
    if not name:
        name = os.environ.get('GIT_AUTHOR_NAME', 'You')
    if not email:
        email = os.environ.get('GIT_AUTHOR_EMAIL', 'you@example.com')
    return name, email


def create_commit(gd, tree_sha, parent_sha, message):
    name, email = get_user_info(gd)
    now = int(time.time())
    tz = time.strftime('%z') or '+0000'
    lines = []
    lines.append(f"tree {tree_sha}")
    if parent_sha:
        lines.append(f"parent {parent_sha}")
    lines.append(f"author {name} <{email}> {now} {tz}")
    lines.append(f"committer {name} <{email}> {now} {tz}")
    lines.append('')
    lines.append(message)
    body = '\n'.join(lines).encode('utf-8')
    commit_sha = write_object(gd, 'commit', body)
    return commit_sha


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/git_commit_no_git.py "Commit message"')
        sys.exit(1)
    msg = sys.argv[1]
    root = repo_root()
    gd = git_dir(root)
    if not os.path.isdir(gd):
        print('.git directory not found in', root)
        sys.exit(1)

    head_type, head_val = read_head(gd)
    parent = None
    ref = None
    if head_type == 'ref':
        ref = head_val
        parent = read_ref(gd, ref)
    else:
        parent = head_val if head_val else None

    tree_sha = build_tree(gd, root, '')
    commit_sha = create_commit(gd, tree_sha, parent, msg)

    if ref:
        write_ref(gd, ref, commit_sha)
        print('Updated', ref, '->', commit_sha)
    else:
        # detached HEAD: write HEAD directly
        head_path = os.path.join(gd, 'HEAD')
        with open(head_path, 'w', encoding='utf-8') as f:
            f.write(commit_sha + '\n')
        print('Set HEAD to', commit_sha)

    print('Commit created:', commit_sha)


if __name__ == '__main__':
    main()
