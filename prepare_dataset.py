import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

# Project Root
BASE_DIR = os.getcwd()

metadata_path = os.path.join(BASE_DIR, "HAM10000_metadata.csv")

image_dirs = [
    os.path.join(BASE_DIR, "HAM10000_images_part_1"),
    os.path.join(BASE_DIR, "HAM10000_images_part_2")
]

output_dir = os.path.join(BASE_DIR, "dataset")

os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(metadata_path)

# image_id -> image path
image_dict = {}

for folder in image_dirs:
    for img in os.listdir(folder):
        image_id = img.split(".")[0]
        image_dict[image_id] = os.path.join(folder, img)

df["path"] = df["image_id"].map(image_dict)

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["dx"]
)

def copy_images(dataframe, split_name):

    for _, row in dataframe.iterrows():

        label = row["dx"]

        src = row["path"]

        dst_folder = os.path.join(output_dir, split_name, label)

        os.makedirs(dst_folder, exist_ok=True)

        shutil.copy(src, dst_folder)

copy_images(train_df, "train")
copy_images(test_df, "test")

print("Dataset Prepared Successfully!")