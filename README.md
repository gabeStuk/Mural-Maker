# Mural Maker

Simple Python program that takes in a series of source images and uses them to build a composite image

## Usage
- Place source images in a source-images folder in the same directory as `maker.py`
- Install dependencies from `requirements.txt`
- Run `maker.py`
- Select the image to form from the file dialog
- Wait for probably a long time depending on how big the images are and how large you configure the resizes (below)
- The resultant image can be found at `<PROJECT_DIRECTORY>\output.png` (or `<PROJECT_DIRECTORY>/output.png` for POSIX enjoyers) and will display upon completion


## Config
- The color of the image can be tinted to be closer to the pixel it replaces, this can be enabled via the `autotune` variable on line 9 of [`maker.py`](./maker.py)
    - `autotune_intensity` below it will set the opacity of the tint

- `input_width` (line 53) defines the width to scale to of the image selected to make into a mural
- `src_resize` (line 55) does the same for the source images