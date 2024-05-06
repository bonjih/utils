import os
import subprocess


def split_videos(input_dir, split_duration):

    videos = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    for video in videos:
        video_name, video_ext = os.path.splitext(video)
        video_path = os.path.join(input_dir, video)

        output_video_dir = os.path.join(os.path.dirname(input_dir), video_name)
        os.makedirs(output_video_dir, exist_ok=True)
        ffmpeg = './ffmpeg/ffmpeg.exe'
        command = [ffmpeg, '-i', video_path, '-c', 'copy', '-map', '0', '-segment_time', str(split_duration), '-f',
                   'segment', os.path.join(output_video_dir, f'{video_name}_%03d{video_ext}')]

        subprocess.run(command)


if __name__ == "__main__":
    input_dir = 'videos_to_split'
    split_duration = 600
    split_videos(input_dir, split_duration)
