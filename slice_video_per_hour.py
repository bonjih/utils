import os
import cv2
from datetime import datetime, timedelta


def slice_videos(directory):
    # Create output directory if it doesn't exist
    output_directory = os.path.join(directory, "videos_out")
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.endswith((".mp4", ".mkv", ".avi")):
            file_path = os.path.join(directory, filename)
            cap = cv2.VideoCapture(file_path)
            frame_rate = cap.get(cv2.CAP_PROP_FPS)
            # Use regex to extract the time part from the filename
            match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', filename)
            if match:
                start_time_str = match.group(0)
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d_%H-%M-%S')
               
        

            # Align start time to the nearest hour
            start_time = start_time.replace(minute=0, second=0, microsecond=0)
            current_hour = start_time.hour

            while True:
                # Calculate the start and end times for the 5-minute segment
                frame_time = start_time + timedelta(hours=current_hour - start_time.hour)
                end_time = frame_time + timedelta(minutes=5)

                # Check if end time exceeds video duration
                if end_time > start_time + timedelta(seconds=cap.get(cv2.CAP_PROP_FRAME_COUNT) / frame_rate):
                    break

                # Convert start and end time to string
                start_time_str = frame_time.strftime('%H-%M-%S')
                end_time_str = end_time.strftime('%H-%M-%S')

                # Create output filename
                output_filename = f"{filename.split('.')[0]}_{start_time_str}_{end_time_str}.mp4"
                output_filepath = os.path.join(output_directory, output_filename)

                # Write 5-minute segment to a new video file
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                output_video = cv2.VideoWriter(output_filepath, fourcc, frame_rate, (
                int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
                while frame_time < end_time:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_time.timestamp() * frame_rate))
                    ret, frame = cap.read()
                    if not ret:
                        break
                    output_video.write(frame)
                    frame_time += timedelta(seconds=1 / frame_rate)

                output_video.release()

                current_hour += 1

            cap.release()


videos_directory = "videos"
slice_videos(videos_directory)
