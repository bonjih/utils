import cv2
import datetime

def extract_segment(input_file, output_file, start_time, end_time):
    cap = cv2.VideoCapture(input_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    start_frame = int(start_time.timestamp() * fps)
    end_frame = int(end_time.timestamp() * fps)

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
    input_file = "TV404C PC2 ROM Bin North West_urn-uuid-00075fbe-4138-3841-be5f-0700075fbe5f_2024-05-02_16-00-00.mp4"
    output_file = "output_video_segment.mp4"

    start_time = datetime.datetime.strptime("16:45:00", "%H:%M:%S")  # Start time of the segment
    end_time = datetime.datetime.strptime("16:55:00", "%H:%M:%S")    # End time of the segment

    extract_segment(input_file, output_file, start_time, end_time)

if __name__ == "__main__":
    main()
 
