import os
import shutil
import zipfile

# Move zip files into correct locations
zip1 = "Only_sequence.zip"
dest1 = os.path.join("Models","Exclude_Refined_TrueOT","GRU-EMB","Ensemble")

os.makedirs(dest1, exist_ok=True)
shutil.move(zip1, os.path.join(dest1, zip1))

with zipfile.ZipFile(os.path.join(dest1, zip1), 'r') as zip_ref:
    zip_ref.extractall(dest1)




source_dir = "path/to/your/zip_folder"
dest2 = os.path.join("Models","Exclude_Refined_TrueOT","GRU-EMB","Ensemble","With_features_by_columns","10_ensembels","50_models","Binary_epigenetics")
os.makedirs(dest2, exist_ok=True)

for fname in os.listdir(source_dir):
    if fname.endswith(".zip") and not fname == "Only_sequence.zip":
        src_path = os.path.join(source_dir, fname)
        dest_path = os.path.join(dest2, fname)

        shutil.move(src_path, dest_path)
        with zipfile.ZipFile(dest_path, 'r') as zip_ref:
            zip_ref.extractall(dest2)
        