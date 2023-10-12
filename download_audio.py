import requests
import json
import os
from pathlib import Path

audio_dir = Path("audio")

os.makedirs(audio_dir, exist_ok=True)

max_retries = 3

with open("metadata.jsonl", "r") as data_file:
    for i, line in enumerate(data_file.readlines()):
        data = json.loads(line)
        download_link = data.get("download_link", "")

        # Initialize the retry counter
        retries = 0

        while retries < max_retries:
            try:
                # Attempt to download the file
                result = requests.get(download_link)
                result.raise_for_status()  # Raise an exception for HTTP errors

                # If successful, write the file and break the loop
                with open(audio_dir / f"{i}.mp3", 'wb+') as f:
                    f.write(result.content)
                break
            except requests.RequestException as e:
                print(f"An error occurred while downloading {download_link}: {e}")
                retries += 1  # Increment the retry counter

        # If retries are exhausted, print an error message
        if retries == max_retries:
            print(f"Failed to download {download_link} after 1 retry.")
