import os
import cv2
import math

def split_video(input_file, output_dir, duration):
    cap = cv2.VideoCapture(input_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_duration = total_frames / fps

    num_segments = math.ceil(total_duration / duration)

    segment_duration = total_duration / num_segments

    for i in range(num_segments):
        start_frame = int(i * segment_duration * fps)
        end_frame = int((i + 1) * segment_duration * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_file))[0]}_{i+1}.mp4")
        out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

        while True:
            ret, frame = cap.read()
            if not ret or cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_frame:
                break
            out.write(frame)

        out.release()

    cap.release()

def main():
    input_dir = "videos"
    output_dir = "output_videos"
    duration = 5 * 60  # 5 minutes in seconds

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".mp4") or file.endswith(".avi") or file.endswith(".mkv"):
            input_file = os.path.join(input_dir, file)
            split_video(input_file, output_dir, duration)

if __name__ == "__main__":
    main()
