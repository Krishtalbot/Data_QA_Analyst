import pandas as pd
import os
from multiprocessing import Pool

df = pd.read_csv("dataset.csv")

df["post_code"] = df["post_code"].astype(str)

output_directory = "splitted_dataset"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print(f"Created dir: {output_directory}")


def save_to_csv(args):
    post_code, group = args
    output_file = os.path.join(output_directory, f"dataset_{post_code}.csv")
    group.to_csv(output_file, index=False)
    print(f"Saved: {output_file}")


if __name__ == "__main__":
    groups = [(post_code, group) for post_code, group in df.groupby("post_code")]
    with Pool(processes=8) as pool:
        pool.map(save_to_csv, groups)
