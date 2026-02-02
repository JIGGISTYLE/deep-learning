erDataset(Dataset):      # pytorch base class
  def __init__(self,image_dir,csv_file,transform=None):
    self.image_dir=image_dir
    self.data=pd.read_csv(csv_file)  # read csv
    self.transform=transform
  def __len__(self):
    return len(self.data)  # length of data

  def __getitem__(self,idx):
    row=self.data.iloc[idx]
    img_path=os.path.join(self.image_dir, f"{row[0]}.jpg") # Added .jpg extension
    image=Image.open(img_path).convert("RGB")
    label=torch.tensor(row[2:].values.astype("float32"))

    if self.transform:
      image=self.transform(image)

    return image,label