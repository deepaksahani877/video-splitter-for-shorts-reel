import os
import uuid
import shutil
import argparse
import platform
import json
from typing import Dict, Any, Optional

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip
from moviepy.video.fx.resize import resize
from moviepy.config import change_settings

# Configure ImageMagick path for Windows (same as original)
if platform.system() == "Windows":
    change_settings(
        {
            "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        }
    )

# Video configuration (same as original)
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920

# Config file in same folder as this script
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

# Defaults: match the original parser defaults (these will be used to create/update config.json)
DEFAULT_CONFIG: Dict[str, Any] = {
    "input_video": None,  # allow config.json to provide this; if missing at runtime, error out
    "background_image": "background.png",
    "logo_image": "logo.png",
    "username": "@username",
    "video_title": "Video Title",
    "part_duration": 30,
    "username_font": "fonts/Montserrat-Italic.ttf",
    "title_font": "fonts/Philosopher-Bold.ttf",
    "part_font": "fonts/MarckScript-Regular.ttf",
    "username_color": "#0b789a",
    "title_color": "#0b789a",
    "part_color": "#0b789a",
    "output_base": "output",
    "start": 0,
    "end": None,
}


# ---------------------- Config utilities ---------------------- #
def ensure_config_file(config_path: str = CONFIG_FILE) -> Dict[str, Any]:
    """
    Ensure config.json exists at config_path.
    - If missing: create it with DEFAULT_CONFIG.
    - If exists: load it, add missing keys from DEFAULT_CONFIG, and write back the updated file.
    Returns the loaded (and possibly updated) config dict.
    """
    defaults = DEFAULT_CONFIG.copy()
    config: Dict[str, Any] = {}

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f) or {}
            # Fill missing keys with defaults (preserve user keys)
            updated = False
            for k, v in defaults.items():
                if k not in config:
                    config[k] = v
                    updated = True
            if updated:
                with open(config_path, "w", encoding="utf-8") as f:
                    json.dump(config, f, indent=4)
                print(f"Updated config.json with missing defaults at: {config_path}")
        except Exception as e:
            # Invalid JSON or read error -> regenerate with defaults
            print(
                f"Invalid config.json ({e}). Recreating with defaults at: {config_path}"
            )
            config = defaults.copy()
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            print(f"Created default config.json at {config_path}")
    else:
        # Create config with defaults
        config = defaults.copy()
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        print(f"Created default config.json at {config_path}")

    return config


# ---------------------- Video generation logic (unchanged features) ---------------------- #
def generate_reels_parts(
    input_video: str,
    start: int = 0,
    end: int = None,
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

    # Validate start/end
    start = max(0, start)
    end = min(duration, end) if end else duration
    if start >= end:
        raise ValueError("Start time must be less than end time.")

    project_id = str(uuid.uuid4())[:8]
    output_folder = os.path.join(output_base, f"{video_title}_{project_id}")
    os.makedirs(output_folder, exist_ok=True)

    temp_dir = os.path.join("temp", f"video_split_{project_id}")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        for i, t in enumerate(range(start, int(end), part_duration), 1):
            subclip_end = min(t + part_duration, end)
            subclip = clip.subclip(t, subclip_end)

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
            if logo_clip:
                username_text = TextClip(
                    f"/{username[1:]}",
                    fontsize=30,
                    font=username_font,
                    color=username_color,
                ).set_duration(subclip.duration)
                username_x = logo_x + logo_clip.w + 10
                username_y = logo_y + (logo_clip.h - username_text.h) / 2
                username_text = username_text.set_position((username_x, username_y))
            else:
                username_text = TextClip(
                    username,
                    fontsize=30,
                    font=username_font,
                    color=username_color,
                ).set_duration(subclip.duration)
                username_text = username_text.set_position(
                    (
                        VIDEO_WIDTH - username_text.w - 50,
                        VIDEO_HEIGHT - username_text.h - 50,
                    )
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
                .set_position(("center", VIDEO_HEIGHT - 250))
            )

            # --- Compose all clips ---
            clips_to_compose = [bg, scaled_video]
            if logo_clip:
                clips_to_compose.append(logo_clip)
            clips_to_compose.extend([title_text, part_text, username_text])

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

            print(f"Saved {output_path}")

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Cleaned up temp folder: {temp_dir}")

    print(f"All parts saved in {output_folder}")


# ---------------------- CLI parsing and merge ---------------------- #
def build_parser() -> argparse.ArgumentParser:
    """
    Build argument parser.
    Note: optional args default to None so we can detect whether the user provided them.
    """
    parser = argparse.ArgumentParser(
        description="Generate Instagram Reels style video parts."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=CONFIG_FILE,
        help="Path to config.json (default: same folder as main.py)",
    )

    # Keep input-video optional here so config.json can provide it; we'll validate later.
    parser.add_argument(
        "--input-video", type=str, help="Input video (CLI overrides config)"
    )

    parser.add_argument(
        "--background-image",
        type=str,
        help="Optional background (CLI overrides config)",
    )
    parser.add_argument(
        "--logo-image", type=str, help="Optional logo (CLI overrides config)"
    )
    parser.add_argument(
        "--username", type=str, help="Overlay username text (CLI overrides config)"
    )
    parser.add_argument(
        "--video-title", type=str, help="Title text (CLI overrides config)"
    )
    parser.add_argument(
        "--part-duration",
        type=int,
        help="Duration of each part in seconds (CLI overrides config)",
    )
    parser.add_argument(
        "--username-font",
        type=str,
        help="Font for username (CLI overrides config)",
    )
    parser.add_argument(
        "--title-font",
        type=str,
        help="Font for title (CLI overrides config)",
    )
    parser.add_argument(
        "--part-font",
        type=str,
        help="Font for part text (CLI overrides config)",
    )
    parser.add_argument(
        "--username-color", type=str, help="Username text color (CLI overrides config)"
    )
    parser.add_argument(
        "--title-color", type=str, help="Title text color (CLI overrides config)"
    )
    parser.add_argument(
        "--part-color", type=str, help="Part text color (CLI overrides config)"
    )
    parser.add_argument(
        "--output-base", type=str, help="Base output folder (CLI overrides config)"
    )
    parser.add_argument(
        "--start",
        type=int,
        help="Start time in seconds to begin splitting (CLI overrides config)",
    )
    parser.add_argument(
        "--end",
        type=int,
        help="End time in seconds to stop splitting (CLI overrides config). Use nothing for video end.",
    )

    return parser


def merge_config_and_cli(
    cli_args: argparse.Namespace, config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge values with priority:
        CLI (if provided) -> config.json -> DEFAULT_CONFIG
    """
    merged: Dict[str, Any] = {}
    for key, default_value in DEFAULT_CONFIG.items():
        # argparse converts --some-arg to attribute some_arg
        cli_val = getattr(cli_args, key, None)
        if cli_val is not None:
            merged[key] = cli_val
        elif key in config:
            merged[key] = config[key]
        else:
            merged[key] = default_value

    # Coerce type-sensible fields to ints if not None
    for int_key in ("part_duration", "start", "end"):
        if merged.get(int_key) is not None:
            try:
                merged[int_key] = int(merged[int_key])
            except Exception:
                # if conversion fails, fallback to default (safe)
                merged[int_key] = DEFAULT_CONFIG[int_key]
    return merged


def main():
    parser = build_parser()
    cli_args = parser.parse_args()

    # Ensure config.json exists and is up-to-date (will write missing keys)
    config = ensure_config_file(cli_args.config)

    # Merge so that CLI overrides config which overrides defaults
    final_args = merge_config_and_cli(cli_args, config)

    # Input video is required either from CLI or config.json
    if not final_args.get("input_video"):
        parser.error(
            "No input video specified. Provide --input-video or set 'input_video' in config.json."
        )

    # Call the original generation logic with merged arguments
    generate_reels_parts(
        input_video=final_args["input_video"],
        start=final_args["start"],
        end=final_args["end"],
        background_image=final_args["background_image"],
        logo_image=final_args["logo_image"],
        username=final_args["username"],
        video_title=final_args["video_title"],
        part_duration=final_args["part_duration"],
        username_font=final_args["username_font"],
        title_font=final_args["title_font"],
        part_font=final_args["part_font"],
        username_color=final_args["username_color"],
        title_color=final_args["title_color"],
        part_color=final_args["part_color"],
        output_base=final_args["output_base"],
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Keep message exactly as requested originally
        print("Video split operation cancelled!")
