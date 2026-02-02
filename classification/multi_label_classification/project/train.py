# train.py
import torch
from tqdm.auto import tqdm # Import tqdm here

def train_per_epoch(model,loader,optimizer,criterion,device):
  model.train()
  total_loss=0

  for image,label in tqdm(loader, desc="Training Batch", leave=False): # Added tqdm to the loader
    image=image.to(device)
    label=label.to(device)
    optimizer.zero_grad()

    output=model(image)
    loss=criterion(output,label)
    loss.backward()
    optimizer.step()
    total_loss+=loss.item()
  avg_loss=total_loss/len(loader)

  return avg_loss

def evaluate(model,loader,device):
  model.eval()
  correct=0
  total=0

  with torch.no_grad():
    for image,label in tqdm(loader, desc="Evaluation Batch", leave=False): # Added tqdm to the loader
      image=image.to(device)
      label=label.to(device)
      output=torch.sigmoid(model(image))
      preds=(output>0.5).float()
      correct+=(preds==label).sum().item()
      total+=label.numel()

    return correct/total