import pandas as pd
from pathlib import Path
from tqdm import tqdm

speech_metadata = pd.read_csv("speeches_metadata.csv", low_memory=False)
speech_metadata.rename(columns={"index": "speech_id"}, inplace=True)
print("speech metadata table:")
print(speech_metadata.head())

speeches = list((Path().cwd() / "speeches").glob("*.txt"))

speech_data: list[dict[str, int | str]] = []
for speech_file in tqdm(speeches):
    file_name = speech_file.stem
    with open(speech_file, "r") as f:
        file_contents = f.read()
    speech_data.append({
        "speech_id": int(file_name),
        "speech_text": file_contents
    })

speeches_df = pd.DataFrame(speech_data)
print("speech text table:")
print(speeches_df.head())


merged = pd.merge(
    left=speech_metadata,
    right=speeches_df,
    on="speech_id",
    how="left",
    validate="1:1"
)
print("merged table")
print(merged.head())

merged.to_csv("combined_speech_data.csv", index=False)

