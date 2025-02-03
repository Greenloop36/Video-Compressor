"""

Video Compressor ~ gl36
03/02/2025

"""

## Configuration

## Imports
import os
import ffmpeg
import time
from moviepy.editor import VideoFileClip


## Methods
def CompressVideo(InputFilePath: str, OutputFilePath: str, TargetSize: int) -> tuple[bool, Exception | None]:
    # Load the video
    clip = VideoFileClip(InputFilePath)
    duration = clip.duration  # Duration in seconds

    # Calculate target bitrate (in kbps)
    target_bitrate = (TargetSize * 8192) / duration

    # Write the video with the calculated bitrate
    clip.write_videofile(
        output_path,
        bitrate=f"{int(target_bitrate)}k",  # Set bitrate in kbps
        codec="libx264",                    # Use H.264 codec
        preset="medium",                    # Balance speed and compression
        threads=4                           # Use multiple CPU threads
    )
    clip.close()


    # min_audio_bitrate = 32000
    # max_audio_bitrate = 256000

    # ProbeStart = time.time()
    # print(InputFilePath)
    # probe = ffmpeg.probe(InputFilePath)
    # ProbeEnd = time.time()

    # duration = float(probe['format']['duration']) # Video duration in seconds
    # audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate']) # Audio bitrate in bps
    # target_total_bitrate = (TargetSize * 1024 * 8) / (1.073741824 * duration) # Target total bitrate, in bps.

    # # Target audio bitrate, in bps
    # if 10 * audio_bitrate > target_total_bitrate:
    #     audio_bitrate = target_total_bitrate / 10
    #     if audio_bitrate < min_audio_bitrate < target_total_bitrate:
    #         audio_bitrate = min_audio_bitrate
    #     elif audio_bitrate > max_audio_bitrate:
    #         audio_bitrate = max_audio_bitrate
        
    # # Target video bitrate, in bps.
    # video_bitrate = target_total_bitrate - audio_bitrate

    # InputStart = time.time()
    # i = ffmpeg.input(InputFilePath)
    # InputEnd = time.time()
    # try:
    #     FirstPassStart = time.time()
    #     ffmpeg.output(i, os.devnull,
    #               **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
    #               ).overwrite_output().run()
    #     FirstPassEnd = time.time()
    #     ffmpeg.output(i, OutputFilePath,
    #                 **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
    #                 ).overwrite_output().run()
    #     SecondPassEnd = time.time()
    # except Exception as e:
    #     return False, e
    # else:
    #     print(f"Probing: {ProbeEnd - ProbeStart}\nInput: {InputEnd - InputStart}\nFirstPass: {FirstPassEnd - FirstPassStart}\nSecondPass: {SecondPassEnd - FirstPassEnd}\n\nTotal: {SecondPassEnd - ProbeStart}")
    #     return True, None