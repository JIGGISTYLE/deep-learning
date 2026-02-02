#prepare_data.py (run only once)

#download and upload dataset from keggle and upload to drive and use collab

# from google.colab import drive
# drive.mount('/content/drive')

# !unzip "/content/drive/MyDrive/archive (1).zip"


import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

RAW_IMG_DIR = "/content/Multi_Label_dataset/Images"
RAW_LABELS = "/content/Multi_Label_dataset/train.csv"
OUT_DIR = "data"

os.makedirs(OUT_DIR, exist_ok=True)
for s in ["train", "val", "test"]:
    os.makedirs(os.path.join(OUT_DIR, s), exist_ok=True)

df = pd.read_csv(RAW_LABELS)

train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

def copy_images(split_df, split):
    for fname_id in split_df["Id"]:
        src = os.path.join(RAW_IMG_DIR, f"{fname_id}.jpg") 
        dst = os.path.join(OUT_DIR, split, f"{fname_id}.jpg") 
        if os.path.exists(src):
            shutil.copy(src, dst)
        else:
            print(f"Warning: Image not found at {src}")

copy_images(train_df, "train")
copy_images(val_df, "val")
copy_images(test_df, "test")

train_df.to_csv("data/labels_train.csv", index=False)
val_df.to_csv("data/labels_val.csv", index=False)
test_df.to_csv("data/labels_test.csv", index=False)

print("✅ Dataset prepared successfully")