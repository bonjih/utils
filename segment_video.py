import time

import cv2
import datetime


def extract_segment(input_file, output_file, start_sec, end_sec):
    cap = cv2.VideoCapture(input_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

    while True:
        ret, frame = cap.read()
        if not ret or cap.get(cv2.CAP_PROP_POS_FRAMES) >= end_frame:
            break
        out.write(frame)

    cap.release()
    out.release()


def main():
    input_file = "videos_to_split/ PC2 ROM Bin North West_urn-uuid-00075fbe-4138-3841-be5f-0700075fbe5f_2024-05-05_00-00-00(2).mp4"
    output_file = "videos_to_split/output_video_segment.mp4"

    t0 = time.strptime('00:45:00,000'.split(',')[0], '%H:%M:%S')
    start_sec = datetime.timedelta(hours=t0.tm_hour, minutes=t0.tm_min, seconds=t0.tm_sec).total_seconds()

    t1 = time.strptime('00:55:00,000'.split(',')[0], '%H:%M:%S')
    end_sec = datetime.timedelta(hours=t1.tm_hour, minutes=t1.tm_min, seconds=t1.tm_sec).total_seconds()
     
    extract_segment(input_file, output_file, start_sec, end_sec)


if __name__ == "__main__":
    main()
