import pandas as pd

df = pd.read_csv("dataset.csv")

df["post_code"] = df["post_code"].astype(str)
df["dob"] = df["dob"].astype(str)

manifest_data = (
    df.groupby("post_code")
    .agg(
        {
            "dob": ["nunique", lambda x: ", ".join(sorted(x.unique()))],
            "post_code": "count",
        }
    )
    .reset_index()
)

manifest_data.columns = [
    "post_code",
    "total_unique_dob",
    "unique_dobs",
    "total_records",
]

with open("manifest.txt", "w") as f:
    for _, row in manifest_data.iterrows():
        f.write(f"post_code: {row['post_code']}\n")
        f.write(f"dob: {row['unique_dobs']}\n")
        f.write(f"total_unique_dob: {row['total_unique_dob']}\n")
        f.write(f"total_records: {row['total_records']}\n\n")

print("Manifest file created: manifest.txt")
