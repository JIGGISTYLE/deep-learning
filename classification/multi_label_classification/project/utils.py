#utils.py

import torch
from torchvision import transforms

DEVICE= "cuda" if torch.cuda.is_available() else "cpu"

NUM_CLASSES=25
BATCH_SIZE=32
EPOCHS=10
LR=1e-4

def get_train_transform():
  return transforms.Compose([
      transforms.Resize((224,224)),
      transforms.RandomHorizontalFlip(),
      transforms.ToTensor(),
      transforms.Normalize(
          mean=[0.485,0.456,0.406],
          std=[0.229,0.224,0.225]
      )
  ])

def get_val_transform():
  return transforms.Compose([
      transforms.Resize((224,224)),
      transforms.ToTensor(),
      transforms.Normalize(
          mean=[0.485,0.456,0.406],
          std=[0.229,0.224,0.225]
      )
  ])