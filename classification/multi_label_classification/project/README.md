🎬 Movie Genre Prediction from Posters (PyTorch)

This project predicts multiple movie genres from a movie poster using transfer learning (ResNet-18) and PyTorch.

📁 Project Structure
project/
├── data/
│   ├── raw/              # Kaggle dataset (unzipped)
│   ├── train/            # Training images
│   ├── val/              # Validation images
│   └── labels.csv        # Image → multi-label genres
│
├── prepare_data.py       # Preprocess & split dataset
├── dataset.py            # PyTorch Dataset class
├── model.py              # ResNet-18 model
├── train.py              # Training & validation loops
├── utils.py              # Configs, transforms, constants
├── main.py               # Entry point (run training)
└── README.md

📦 Dataset

Source: Kaggle – Movie Genre Prediction from Posters

Task: Multi-label classification (1 poster → multiple genres)

Images + CSV with genre labels

🚀 How to Run
1️⃣ Upload dataset zip to Google Drive

Unzip it into:

data/raw/

2️⃣ Preprocess dataset
python prepare_data.py


Creates:

data/train/

data/val/

data/labels.csv

3️⃣ Train model
python main.py

🧠 Model

ResNet-18 (pretrained)

Final layer → 9 genres

Loss: BCEWithLogitsLoss

Optimizer: Adam

✅ Why no test set?

For learning projects:

Train + Validation is enough

Test set is optional and can be added later

🧪 Output

Training & validation loss per epoch

Model learns visual genre patterns from posters
