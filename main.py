import os
import uuid
import shutil
import argparse
import platform

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from moviepy.video.fx.resize import resize
from moviepy.config import change_settings

# Path to your ImageMagick binary
if platform.system() == "Windows":
    change_settings(
        {
            "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        }
    )

# Video configuration
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920


def generate_reels_parts(
    input_video: str,
    background_image: str = None,
    logo_image: str = None,
    username: str = "@username",
    video_title: str = "Video Title",
    part_duration: int = 30,
    username_font: str = "Arial-Bold",
    title_font: str = "Arial-Bold",
    part_font: str = "Arial-Bold",
    username_color: str = "white",
    title_color: str = "yellow",
    part_color: str = "white",
    output_base: str = "output",
):
    clip = VideoFileClip(input_video)
    duration = clip.duration

    project_id = str(uuid.uuid4())[:8]
    output_folder = os.path.join(output_base, f"{video_title}_{project_id}")
    os.makedirs(output_folder, exist_ok=True)

    temp_dir = os.path.join("temp", f"video_split_{project_id}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for i, start in enumerate(range(0, int(duration), part_duration), 1):
            end = min(start + part_duration, duration)
            subclip = clip.subclip(start, end)

            # --- Background ---
            if background_image and os.path.exists(background_image):
                bg = ImageClip(background_image).set_duration(subclip.duration)
                bg = resize(bg, height=VIDEO_HEIGHT, width=VIDEO_WIDTH)
            else:
                bg = (
                    subclip.resize(height=VIDEO_HEIGHT, width=VIDEO_WIDTH)
                    .resize(0.3)
                    .resize(1 / 0.3)
                ).set_duration(subclip.duration)

            # --- Scale video ---
            aspect_ratio = subclip.w / subclip.h
            if aspect_ratio > (9 / 16):
                scaled_video = subclip.resize(width=VIDEO_WIDTH)
            else:
                scaled_video = subclip.resize(height=VIDEO_HEIGHT)
            scaled_video = scaled_video.set_position(("center", "center"))

            # --- Logo overlay ---
            logo_clip = None
            logo_x, logo_y = 50, VIDEO_HEIGHT - 80
            if logo_image and os.path.exists(logo_image):
                logo_clip = ImageClip(logo_image).set_duration(subclip.duration)
                logo_clip = logo_clip.resize(height=50)
                logo_clip = logo_clip.set_position((logo_x, logo_y))

            # --- Username overlay ---
            username_text = TextClip(
                f"/{username[1:]}",
                fontsize=30,
                font=username_font,
                color=username_color,
            ).set_duration(subclip.duration)
            if logo_clip:
                # Align vertical center of username text with logo
                username_x = logo_x + logo_clip.w + 10
                username_y = logo_y + (logo_clip.h - username_text.h) / 2
                username_text = username_text.set_position((username_x, username_y))
            else:
                username_text = TextClip(
                    username, fontsize=30, font=username_font, color=username_color
                ).set_duration(subclip.duration)
                username_text = username_text.set_position(
                    (VIDEO_WIDTH - username_text.w - 50, VIDEO_HEIGHT - 50)
                )

            # --- Title and part overlays ---
            title_text = (
                TextClip(video_title, fontsize=70, font=title_font, color=title_color)
                .set_duration(subclip.duration)
                .set_position(("center", 200))
            )
            part_text = (
                TextClip(f"Part {i}", fontsize=60, font=part_font, color=part_color)
                .set_duration(subclip.duration)
                .set_position(("center", VIDEO_HEIGHT - 170))
            )

            # --- Compose all clips ---
            clips_to_compose = [bg, scaled_video]
            if logo_clip:
                clips_to_compose.append(logo_clip)  # logo above video
            clips_to_compose.extend(
                [title_text, part_text, username_text]
            )  # all texts on top

            final = CompositeVideoClip(
                clips_to_compose, size=(VIDEO_WIDTH, VIDEO_HEIGHT)
            ).set_audio(subclip.audio)

            # --- Export ---
            temp_audiofile = os.path.join(temp_dir, f"temp_audio_part{i}.m4a")
            output_path = os.path.join(output_folder, f"part_{i}.mp4")
            final.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=30,
                threads=4,
                preset="ultrafast",
                temp_audiofile=temp_audiofile,
                remove_temp=True,
                logger="bar",
            )

            print(f"✅ Saved {output_path}")

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🧹 Cleaned up temp folder: {temp_dir}")

    print(f"\n🎉 All parts saved in {output_folder}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Instagram Reels style video parts."
    )
    parser.add_argument(
        "--input-video", type=str, default=None, required=True, help="Input video"
    )
    parser.add_argument(
        "--background-image",
        type=str,
        default="background.png",
        help="Optional background",
    )
    parser.add_argument(
        "--logo-image", type=str, default="logo.png", help="Optional logo"
    )
    parser.add_argument(
        "--username", type=str, default="@username", help="Overlay username text"
    )
    parser.add_argument(
        "--video-title", type=str, default="Video Title", help="Title text"
    )
    parser.add_argument(
        "--part-duration", type=int, default=30, help="Duration of each part in seconds"
    )
    parser.add_argument(
        "--username-font",
        type=str,
        default="fonts/Montserrat-Italic.ttf",
        help="Font for username",
    )
    parser.add_argument(
        "--title-font",
        type=str,
        default="fonts/Philosopher-Bold.ttf",
        help="Font for title",
    )
    parser.add_argument(
        "--part-font",
        type=str,
        default="fonts/MarckScript-Regular.ttf",
        help="Font for part text",
    )
    parser.add_argument(
        "--username-color", type=str, default="#0b789a", help="Username text color"
    )
    parser.add_argument(
        "--title-color", type=str, default="#0b789a", help="Title text color"
    )
    parser.add_argument(
        "--part-color", type=str, default="#0b789a", help="Part text color"
    )
    parser.add_argument(
        "--output-base", type=str, default="output", help="Base output folder"
    )

    args = parser.parse_args()

    generate_reels_parts(
        input_video=args.input_video,
        background_image=args.background_image,
        logo_image=args.logo_image,
        username=args.username,
        video_title=args.video_title,
        part_duration=args.part_duration,
        username_font=args.username_font,
        title_font=args.title_font,
        part_font=args.part_font,
        username_color=args.username_color,
        title_color=args.title_color,
        part_color=args.part_color,
        output_base=args.output_base,
    )
