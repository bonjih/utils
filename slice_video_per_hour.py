import os
import cv2
from datetime import datetime, timedelta
import re


videos
  - SCTASK2150645
    - Footage
    - IncidentDB


import os
import cv2
from datetime import datetime, timedelta
import re


def create_output_filename(filename, start_time_str):
    # Extract the relevant parts from the filename
    filename_parts = filename.split('.')
    prefix = '_'.join(filename_parts[:-1])  # Exclude the extension
    extension = filename_parts[-1]

    # Construct the output filename
    output_filename = f"{prefix}_{start_time_str}.{extension}"
    return output_filename


def slice_video(video_path, output_directory):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    # Use regex to extract the time part from the filename
    match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', video_path)
    if match:
        start_time_str = match.group(0)
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d_%H-%M-%S')

        # Align start time to the nearest hour
        start_time = start_time.replace(minute=0, second=0, microsecond=0)
        current_hour = start_time.hour
        segment_index = 1

        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_duration = total_frames / frame_rate  # in seconds

        while True:
            # Calculate the start and end times for the 5-minute segment
            frame_time = start_time + timedelta(hours=current_hour - start_time.hour)
            end_time = frame_time + timedelta(minutes=5)

            # Check if end time exceeds total duration
            if end_time > start_time + timedelta(seconds=total_duration):
                break

            # Create output directory based on start time
            output_dirname = os.path.join(output_directory, start_time_str)
            os.makedirs(output_dirname, exist_ok=True)

            # Create output filename
            output_filename = create_output_filename(os.path.basename(video_path),
                                                     frame_time.strftime('%Y-%m-%d_%H-%M-%S'))

            output_filepath = os.path.join(output_dirname, output_filename)

            # Write 5-minute segment to a new video file
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_video = cv2.VideoWriter(output_filepath, fourcc, frame_rate, (
                int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

            while frame_time < end_time:
                ret, frame = cap.read()
                if not ret:
                    break
                output_video.write(frame)
                frame_time += timedelta(seconds=1 / frame_rate)

            output_video.release()

            current_hour += 1
            segment_index += 1

    cap.release()


def slice_videos(directory):
    # Create output directory if it doesn't exist
    output_directory = os.path.join(directory, "videos-out")
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through subdirectories in the given directory
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "Footage":
                footage_dir = os.path.join(root, dir_name)
                for filename in os.listdir(footage_dir):
                    if filename.endswith((".mp4", ".mkv", ".avi")):
                        video_path = os.path.join(footage_dir, filename)
                        slice_video(video_path, output_directory)


videos_directory = "videos"
slice_videos(videos_directory)
 
