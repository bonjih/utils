import pandas as pd
import re

# Load the Excel file
df = pd.read_excel('bridging_video_list_20240424.xlsx')

# Select the necessary columns
df = df[['video_id', 'camera_name', 'bridged', 'bridged_mouth', 'bridged_mouth_top_bottom', 'ts_start', 'ts_finish',
         'dirty_lens', 'split_name', 'batch_num']]

# Define a function to extract datetime from video_id
def extract_datetime(video_id):
    match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', video_id)
    if match:
        return match.group(0)
    match = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', video_id)
    if match:
        return match.group(0).replace('_', '-')
    return None

# Splits time to convert to object for time addition
def convert_to_timedelta(time_str):
    try:
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return pd.Timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except Exception as e:
        return pd.NaT

# Apply the datetime extraction function to the dataframe
df['datetime'] = df['video_id'].apply(extract_datetime)
df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d-%H-%M-%S')
df = df.sort_values(by='datetime')

# Process rows to add timedelta to datetime
def process_row(data):
    data = data[data['ts_start'].notnull()]
    df = data.copy()
    df['ts_start'] = df['datetime'] + df['ts_start'].astype(str).apply(convert_to_timedelta)
    df['ts_finish'] = df['datetime'] + df['ts_finish'].astype(str).apply(convert_to_timedelta)
    df = df[df['ts_start'].notnull()]

    df['ts_start'] = df['ts_start'].dt.strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'
    df['ts_finish'] = df['ts_finish'].dt.strftime('%Y-%m-%dT%H:%M:%S') + '+08:00'

    return df[['camera_name', 'datetime', 'ts_start', 'ts_finish', 'bridged', 'bridged_mouth', 'bridged_mouth_top_bottom', 'dirty_lens', 'split_name', 'batch_num']]

# Generate JSON data with updated structure
def generate_json(data):
    json_dic = []

    for index, row in data.iterrows():
        jsons = {
            'camera_name': row['camera_name'],
            'ts_start': row['ts_start'],
            'ts_finish': row['ts_finish'],
            'labels': {
                'bridged': bool(row['bridged']),
                'bridged_mouth': row['bridged_mouth'] if pd.notna(row['bridged_mouth']) else '',
                'bridged_mouth_top_bottom': row['bridged_mouth_top_bottom'] if pd.notna(row['bridged_mouth_top_bottom']) else '',
                'dirty_lens': bool(row['dirty_lens']) if pd.notna(row['dirty_lens']) else False,
                'split_name': row['split_name'] if pd.notna(row['split_name']) else '',
                'batch_num': row['batch_num'] if pd.notna(row['batch_num']) else ''
            }
        }
        json_dic.append(jsons)

    return json_dic

# Process data and generate JSON list
processed_data = process_row(df)
json_list = generate_json(processed_data)

# Output the JSON list
print(json_list)
