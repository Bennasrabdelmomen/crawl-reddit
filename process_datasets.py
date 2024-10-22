import os
import pandas as pd

folder_path = 'datasets_unprocessed'

save_folder = 'no_dups_dataset'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)  

for idx, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith(".csv"):
        dataset_path = os.path.join(folder_path, filename)
        
        df = pd.read_csv(dataset_path)
        
        df_cleaned = df.drop_duplicates()
        
        cleaned_dataset_path = os.path.join(save_folder, filename)
        df_cleaned.to_csv(cleaned_dataset_path, index=False)
        print(f"Cleaned dataset saved to '{cleaned_dataset_path}'.")
