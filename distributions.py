import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('df2.csv', usecols=['frame_ts', 'bridged', 'camera_name'])
data['frame_ts'] = pd.to_datetime(data['frame_ts'], unit='ms')
data['day'] = data['frame_ts'].dt.date
data['hour'] = data['frame_ts'].dt.hour
data['hour_group'] = data['frame_ts'].dt.hour

# Function to plot the distribution of frame timestamps per hour for each 24-hour period

def plot_hourly_distribution_per_day(data):
    # Group by day and hour, and then count the number of frames
    grouped_data = data.groupby(['day', 'hour']).size().reset_index(name='frame_count')

    # Pivot the data to have hours as index and days as columns
    pivot_data = grouped_data.pivot(index='hour', columns='day', values='frame_count').fillna(0)

    # Create the stacked bar plot
    pivot_data.plot(kind='bar', stacked=True, figsize=(15, 8), colormap='tab20')

    plt.xlabel('Hour of Day')
    plt.ylabel('Frame Count')
    plt.title('Distribution of Frame Timestamps per Hour for Each 24-Hour Period')
    plt.xticks(range(24), [f'{hour:02d}:00' for hour in range(24)], rotation=45)
    plt.legend(title='Day', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('frame_distribution_per_hour_per_day.png')
    plt.show()

# Function to plot the distribution of frame timestamps per hour for the entire dataset
def plot_overall_hourly_distribution(data):
    frame_counts = data.groupby('hour_group').size().reset_index(name='frame_count')
    plt.figure(figsize=(15, 8))
    sns.barplot(data=frame_counts, x='hour_group', y='frame_count', alpha=0.7)
    plt.xlabel('Hour of Day')
    plt.ylabel('Frame Count')
    plt.title('Distribution of Frame Timestamps per Hour for the Entire Dataset')
    bridged_data = data[data['bridged'] == True]
    bridged_hourly_counts = bridged_data.groupby('hour_group').size().reset_index(name='bridged_count')
    plt.scatter(bridged_hourly_counts['hour_group'], bridged_hourly_counts['bridged_count'], marker='_', color='red', label='Bridged Events')
    plt.xticks(range(24), [f'{hour:02d}:00' for hour in range(24)])
    plt.tight_layout()
    plt.legend()
    plt.savefig('frame_distribution_with_bridged_events_per_hour.png')
    plt.show()

# Function to plot the stacked bar plot for camera usage over 24 hours
def plot_camera_usage_distribution(data):
    camera_hourly_counts = data.groupby(['hour_group', 'camera_name']).size().unstack(fill_value=0)
    plt.figure(figsize=(15, 8))
    camera_hourly_counts.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='tab20')
    plt.xlabel('Hour of Day')
    plt.ylabel('Frame Count')
    plt.title('Distribution of Frame Timestamps per Camera per Hour')
    plt.xticks(range(24), [f'{hour:02d}:00' for hour in range(24)], rotation=45)
    plt.legend(title='Camera Name', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('camera_distribution_stacked_per_hour.png')
    plt.show()

# Call the functions
plot_hourly_distribution_per_day(data)
plot_overall_hourly_distribution(data)
plot_camera_usage_distribution(data)
