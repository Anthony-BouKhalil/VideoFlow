import yt_dlp
import os
import shutil

def download_video(url, save_path="Downloads"):

    # Create download directory
    os.makedirs(save_path, exist_ok=True)

    # Check FFmpeg installation
    if not shutil.which("ffmpeg"):
        print("Error: FFmpeg is not installed.")
        print("Install it using: brew install ffmpeg")
        return

    ydl_opts = {
        # Prefer H.264 video and AAC audio
        # Fall back to the best available format
        'format': (
            'bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/'
            'bestvideo[vcodec^=avc1]+bestaudio/'
            'best[vcodec^=avc1]/best'
        ),

        # Save filename
        'outtmpl': os.path.join(
            save_path, '%(title)s.%(ext)s'
        ),

        # Download only one video
        'noplaylist': True,

        # Merge into MP4
        'merge_output_format': 'mp4',

        # Convert video to QuickTime-compatible H.264
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }
        ],

        # Re-encode to H.264 + AAC
        'postprocessor_args': {
            'videoconvertor': [
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '20',
                '-pix_fmt', 'yuv420p',
                '-c:a', 'aac',
                '-b:a', '192k',
                '-movflags', '+faststart'
            ]
        },

        # JavaScript runtime
        'js_runtimes': {
            'deno': {}
        },

        # Show progress
        'progress': True,
    }

    try:
        print("\nStarting YouTube download...\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("\nDownload and conversion completed!")
        print("Format: MP4")
        print("Video codec: H.264")
        print("Audio codec: AAC")
        print("Saved location:", os.path.abspath(save_path))

    except yt_dlp.utils.DownloadError as e:
        print("\nDownload error:", e)

    except Exception as e:
        print("\nUnexpected error:", e)


if __name__ == "__main__":

    video_url = input("Enter YouTube URL: ").strip()

    if video_url:
        download_video(video_url)
    else:
        print("Please enter a valid YouTube URL.")
