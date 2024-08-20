import os

def save_dataframes_to_csv(dataframes, output_dir):
    """
    Saves multiple DataFrames to separate CSV files.

    Args:
        dataframes (dict): A dictionary where keys are DataFrame names and values are DataFrames.
        output_dir (str): The path to the directory where the files will be saved.
    """

    for df_name, df in dataframes.items():
        file_path = os.path.join(output_dir, f"{df_name}.csv")
        df.to_csv(file_path, index=False)