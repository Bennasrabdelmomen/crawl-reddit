import pandas as pd
import os

folder_path = 'datasets_unprocessed'
df_final = pd.DataFrame()
save_folder = 'no_dups_dataset'

if not os.path.exists(save_folder):
    os.makedirs(save_folder)

for idx, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith(".csv"):
        dataset_path = os.path.join(folder_path, filename)

        try:
            df = pd.read_csv(dataset_path)

            if df.empty or len(df.columns) == 0:
                print(f"Skipping dataset '{filename}' because it has no columns.")
                continue

            df_cleaned = df.drop_duplicates()
            df_final = pd.concat([df_final, df_cleaned], axis=0)

            cleaned_dataset_path = os.path.join(save_folder, filename)
            df_cleaned.to_csv(cleaned_dataset_path, index=False)

            df_final.to_csv("total_datasets_ite1.csv", index=False)
            print(f"Dataset '{filename}' cleaned and saved to '{cleaned_dataset_path}'.")
            print("Dataset containing all the datasets is saved.")

            print("The total info of the combined dataframe (with duplicates):")
            df_final.info()

            df_cleaned_without_dups = df_cleaned.drop_duplicates()
            df_cleaned_without_dups.to_csv("Total_dataset_nodups.csv", index=False)
            print("The total info of the dataframe without duplicates:")
            df_cleaned_without_dups.info()
            print("Dataset without duplicates saved.")

        except pd.errors.EmptyDataError:
            print(f"Skipping dataset '{filename}' because it contains no data or columns.")
            continue
