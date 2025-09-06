# VideoSplitter 🎬

A powerful Python tool for splitting long videos into Instagram Reels-style segments with customizable overlays, backgrounds, and branding elements.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Video Splitting**: Automatically splits long videos into customizable duration segments
- **Instagram Reels Format**: Optimized for 9:16 aspect ratio (1080x1920)
- **Custom Branding**: Add logos, usernames, and titles to each segment
- **Background Support**: Use custom background images or blurred video backgrounds
- **Font Customization**: Support for custom fonts with full styling control
- **Color Theming**: Customizable text colors and styling
- **Batch Processing**: Process multiple videos with consistent branding
- **Clean Output**: Organized output folders with unique project IDs

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **ImageMagick**: Required for text rendering
- **FFmpeg**: Required for video processing (installed with MoviePy)

### ImageMagick Installation

#### Windows
```bash
# Download and install from: https://imagemagick.org/script/download.php#windows
# Or use Chocolatey:
choco install imagemagick
```

#### macOS
```bash
# Using Homebrew:
brew install imagemagick
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install imagemagick
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/VideoSplitter.git
cd VideoSplitter
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python main.py --help
```

## 🎯 Quick Start

### Basic Usage
```bash
# Split video into 30-second parts with default settings
python main.py --input-video input.mp4

# Custom duration and branding
python main.py --input-video input.mp4 --part-duration 60 --username "@mybrand" --video-title "My Amazing Video"
```

### With Custom Assets
```bash
python main.py \
  --input-video input.mp4 \
  --background-image background.png \
  --logo-image logo.png \
  --username "@mybrand" \
  --video-title "Epic Content Series" \
  --part-duration 45
```

## 📖 Usage

### Command Line Interface

```bash
python main.py [OPTIONS]
```

#### Required Arguments
- `--input-video`: Path to input video file

#### Optional Arguments
- `--background-image`: Background image path (default: `background.png`)
- `--logo-image`: Logo image path (default: `logo.png`)
- `--username`: Username text overlay (default: `@username`)
- `--video-title`: Video title text (default: `Video Title`)
- `--part-duration`: Duration of each part in seconds (default: `30`)
- `--output-base`: Base output folder (default: `output`)

#### Font Customization
- `--username-font`: Font file for username (default: `fonts/Montserrat-Italic.ttf`)
- `--title-font`: Font file for title (default: `fonts/Philosopher-Bold.ttf`)
- `--part-font`: Font file for part text (default: `fonts/MarckScript-Regular.ttf`)

#### Color Customization
- `--username-color`: Username text color (default: `#0b789a`)
- `--title-color`: Title text color (default: `#0b789a`)
- `--part-color`: Part text color (default: `#0b789a`)

### Programmatic Usage

```python
from main import generate_reels_parts

# Basic usage
generate_reels_parts(
    input_video="input.mp4",
    part_duration=30
)

# Advanced usage with custom styling
generate_reels_parts(
    input_video="input.mp4",
    background_image="custom_bg.png",
    logo_image="brand_logo.png",
    username="@mybrand",
    video_title="Amazing Content Series",
    part_duration=45,
    username_font="fonts/Montserrat-Bold.ttf",
    title_font="fonts/Philosopher-Bold.ttf",
    part_font="fonts/MarckScript-Regular.ttf",
    username_color="#FF6B6B",
    title_color="#4ECDC4",
    part_color="#45B7D1",
    output_base="my_output"
)
```

## ⚙️ Configuration

### Video Settings
- **Resolution**: 1080x1920 (9:16 aspect ratio)
- **Frame Rate**: 30 FPS
- **Codec**: H.264 (libx264)
- **Audio Codec**: AAC

### Supported Formats
- **Input**: MP4, MOV, AVI, MKV, WMV
- **Output**: MP4
- **Images**: PNG, JPG, JPEG

### Font Requirements
- Place custom fonts in the `fonts/` directory
- Supported formats: TTF, OTF
- Ensure fonts support the characters you plan to use

## 📁 Project Structure

```
VideoSplitter/
├── main.py                 # Main application script
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── background.png         # Default background image
├── logo.png              # Default logo image
├── input.mp4             # Sample input video
├── fonts/                # Custom fonts directory
│   ├── Montserrat-*.ttf  # Montserrat font family
│   ├── Philosopher-*.ttf # Philosopher font family
│   └── MarckScript-*.ttf # MarckScript font family
├── output/               # Generated video parts
├── temp/                 # Temporary processing files
└── env/                  # Python virtual environment
```

## 💡 Examples

### Example 1: Basic Video Splitting
```bash
python main.py --input-video "tutorial.mp4" --part-duration 60
```
**Output**: Creates 60-second segments with default styling

### Example 2: Branded Content Series
```bash
python main.py \
  --input-video "content_series.mp4" \
  --background-image "brand_bg.png" \
  --logo-image "company_logo.png" \
  --username "@mycompany" \
  --video-title "Tutorial Series" \
  --part-duration 45 \
  --title-color "#FF6B6B" \
  --part-color "#4ECDC4"
```
**Output**: Professional branded segments with custom colors

### Example 3: Minimalist Style
```bash
python main.py \
  --input-video "minimal_video.mp4" \
  --username "@minimalist" \
  --video-title "Clean Design" \
  --username-color "white" \
  --title-color "white" \
  --part-color "white"
```
**Output**: Clean, minimalist segments with white text

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Format code
black main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔧 Troubleshooting

### Common Issues

#### ImageMagick Not Found
```
Error: ImageMagick not found
```
**Solution**: Install ImageMagick and update the path in `main.py`:
```python
change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
})
```

#### Font Not Found
```
Error: Font file not found
```
**Solution**: Ensure font files exist in the `fonts/` directory and use correct paths.

#### Memory Issues
```
Error: Out of memory during processing
```
**Solution**: 
- Reduce video resolution
- Process shorter segments
- Close other applications
- Use `preset="ultrafast"` for faster processing

#### Video Codec Issues
```
Error: Unsupported codec
```
**Solution**: Convert video to MP4 format using FFmpeg:
```bash
ffmpeg -i input.mov -c:v libx264 -c:a aac output.mp4
```

### Performance Tips

1. **Use SSD storage** for faster I/O operations
2. **Close unnecessary applications** to free up RAM
3. **Use appropriate preset** (`ultrafast` for speed, `medium` for quality)
4. **Process shorter videos** if memory is limited

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/deepaksahani877/video-splitter-for-shorts-reel/issues)
- **Email**: deepaksahani877@gmail.com

---

**Made with ❤️ for content creators**
