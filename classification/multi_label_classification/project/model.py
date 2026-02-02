#model.py

import torch.nn as nn
from torchvision import models

def get_resnet18(num_classes):

  model=models.resnet18(pretrained=True)

  for param in model.parameters():
    param.requires_grad=False

  model.fc = nn.Linear(model.fc.in_features,num_classes)
  return model
