
# PixClassifier

PixClassifier is a minimalist tool for classifying images based on their quality, size, and noise levels. The tool provides both a graphical user interface (GUI) and support for advanced image processing.

## Features

- **Image Quality Classification**: Categorizes images into high, medium, or low quality based on resolution and DPI.
- **Size Classification**: Classifies images into small, medium, or large size categories.
- **Noise Analysis**: Identifies high, medium, or low noise levels using Laplacian variance.
- **Real-time Progress**: Updates the progress bar as images are processed.
- **Folder Management**: Removes empty folders automatically after processing.

## Installation

### Prerequisites
- Python 3.8 or later
- Required libraries:
  - `Pillow`
  - `opencv-python`
  - `tkinter` (comes pre-installed with Python on most systems)

### Install Dependencies
Run the following command to install the required dependencies:
```bash
pip install Pillow opencv-python
```

## Usage

### GUI Mode
1. Run the script:
   ```bash
   python PixClassifier.py
   ```
2. Select input and output folders using the GUI.
3. Click **Start Processing** to classify images. The progress bar will update as processing completes.

### Output
Images are organized into categorized folders in the output directory:
```
output_folder/
├── High_Quality/
├── Medium_Quality/
├── Low_Quality/
├── Small_Size/
├── Medium_Size/
├── Large_Size/
├── High_Noise/
├── Medium_Noise/
└── Low_Noise/
```

### Example
Drag and drop your images into the input folder and watch as they are sorted based on quality, size, and noise.

## Icon
![PixClassifier Icon](assets/icon.png)

## License
This project is open source and available under the [GPL v3](LICENSE).
