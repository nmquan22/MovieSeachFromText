import numpy as np
import pandas as pd
import json 

df = pd.read_csv("imdb_top_1000.csv")
print(df.head())
for index, row in df.iterrows():
    # Convert the row to a dictionary
    row_data = row.to_dict()
    
    # Save the dictionary as a JSON file
    with open(f"Data/movie_{index}.json", "w") as file:
        json.dump(row_data, file)
