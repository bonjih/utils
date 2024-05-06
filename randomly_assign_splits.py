import pandas as pd
import numpy as np

# Assuming your DataFrame is named df
data = {
    'item ID': [1, 2, 3, 4, 5],
    'split': [''] * 5  # Initialize split column
}

df = pd.DataFrame(data)

# List of splits
splits = ['train', 'test', 'val']

# Shuffle the DataFrame
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Calculate split sizes
split_sizes = [len(df) // len(splits)] * len(splits)
remainder = len(df) % len(splits)
split_sizes[:remainder] = [size + 1 for size in split_sizes[:remainder]]

# Assign splits
start = 0
for split, size in zip(splits, split_sizes):
    df.loc[start:start + size - 1, 'split'] = split
    start += size

print(df)
