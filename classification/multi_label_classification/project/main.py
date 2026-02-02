# main.py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm.auto import tqdm # Ensure tqdm is imported here

# from dataset import MoviePosterDataset
# from model import get_resnet18
# from train import train_per_epoch
# from utils import *

def main():
  # Added a warning if running on CPU
  if DEVICE == 'cpu':
      print("⚠️ Warning: No GPU found. Training will be significantly slower on CPU.")
      print("Consider changing your Colab runtime to 'GPU' (Runtime > Change runtime type).")

  train_dataset=MoviePosterDataset("/content/data/train","/content/data/labels_train.csv",get_train_transform())
  val_dataset=MoviePosterDataset("/content/data/val","/content/data/labels_val.csv",get_val_transform())
  test_dataset=MoviePosterDataset("/content/data/test","/content/data/labels_test.csv",get_val_transform())

  train_loader=DataLoader(train_dataset,batch_size=BATCH_SIZE,shuffle=True)
  val_loader=DataLoader(val_dataset,batch_size=BATCH_SIZE,shuffle=True)
  test_loader=DataLoader(test_dataset,batch_size=BATCH_SIZE,shuffle=True)

  model=get_resnet18(NUM_CLASSES).to(DEVICE)
  criterion=nn.BCEWithLogitsLoss()
  optimizer=optim.Adam(model.fc.parameters(),lr=LR)

  for epoch in tqdm(range(EPOCHS), desc="Training Epochs"): # Added tqdm for epoch progress
    train_loss=train_per_epoch(model,train_loader,optimizer,criterion,DEVICE)
    val_acc=evaluate(model,val_loader,DEVICE)
    test_acc=evaluate(model,test_loader,DEVICE)

    print(f"epoch{epoch+1}/{EPOCHS}]",
          f"train_loss={train_loss:.4f}]",
          f"val_acc={val_acc:.4f}]",
          f"test accuracy={test_acc:.4f}]")

if __name__=="__main__":
  main()