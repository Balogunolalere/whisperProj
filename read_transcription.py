import pandas as pd
import os

# Specify the directory path and filename (replace with your actual path)
path = "/home/doombuggy_/Projects/whisperProj/"
filename = "transcription.json"

# Load the JSON file into a pandas DataFrame
df = pd.read_json(os.path.join(path, filename))

# Display the DataFrame
print(df)