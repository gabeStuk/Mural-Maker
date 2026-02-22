from PIL import Image
import numpy as np
from pathlib import Path
import os
import math
import time
from tkinter.filedialog import askopenfilename
import hashlib

autotune = False
autotune_intensity = 0.5

# https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def get_files_in_dir(dir):
    return [f.absolute() for f in Path(dir).iterdir() if f.is_file()]

def get_image():
    return askopenfilename()

color_cache = {}
colors_cached = 0

def get_average_color(image: Image.Image):
    global colors_cached
    key = hashlib.sha256(image.tobytes()).hexdigest()
    if key in color_cache:
        return color_cache[key]
    image = image.convert("RGB")
    npimg = np.array(image)
    avg_color = np.mean(npimg, axis=(0,1))
    color_cache[key] = tuple(avg_color.astype(int))
    colors_cached += 1
    print(f"Parsed colors of image {colors_cached}")
    return tuple(avg_color.astype(int))

color_closest_cache = {}

def closest_color_index(colors, color):
    if color in color_closest_cache:
        return color_closest_cache[color]
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color)**2, axis=1))
    idx = np.where(distances == np.amin(distances))[0]
    if len(idx) == 1:
        color_closest_cache[tuple(color)] = idx.item()
        return idx.item()
    else:
        color_closest_cache[tuple(color)] = idx[0]
        return idx[0]
start_time = time.time()
input_image = Image.open(get_image())
image_ar = input_image.height / input_image.width
# input_width = 512
# input_resize = (input_width, round(input_width * image_ar))
src_resize = (128, 128)
# input_image = input_image.resize(input_resize).convert("RGB")
input_image = input_image.convert("RGB")
image_sources = get_files_in_dir("source-images")

source_images = []

cursor_hide = '\033[?25l'
cursor_show ='\033[?25h'

image_num = len(image_sources)

# ram eater
for i in range(image_num):
    source_images.append(Image.open(image_sources[i]).resize(src_resize).convert("RGB"))
    print(f"Loaded Image {i}/{image_num} ({math.floor((float(i) / image_num) * 100)}%)")

# new_img = Image.new("RGBA", (input_resize[0] * src_resize[0], input_resize[1] * src_resize[1]))
new_img = Image.new("RGBA", (input_image.width * src_resize[0], input_image.height * src_resize[1]))
num_iters = input_image.width * input_image.height
width, height = input_image.size
total = new_img.width * new_img.height
prog_bar_len = 20
print(cursor_hide)
try:
    for x in range(width):
        prog = math.floor((x / width) * prog_bar_len)
        for y in range(height):
            p = input_image.getpixel((x, y))
            color_closest_index = closest_color_index([get_average_color(i) for i in source_images], p)
            img_to_paste: Image.Image = source_images[color_closest_index]
            if (autotune):
                img_to_paste = Image.blend(img_to_paste, Image.new('RGB', img_to_paste.size, p), autotune_intensity)
            new_img.paste(img_to_paste, (x * img_to_paste.size[0], y * img_to_paste.size[1]))
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{bcolors.ENDC}# <{bcolors.OKGREEN}{"=" * prog}{bcolors.ENDC}{"-" * (prog_bar_len - prog)}> ({x * height + y}/{num_iters})", end='\r', flush=True)

    new_img.save("output.png")
    new_img.show("Result")
except Exception as e:
    print(cursor_show)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{bcolors.ENDC}# <{bcolors.FAIL}{"=" * prog}{bcolors.ENDC}{"-" * (prog_bar_len - prog)}>")
    print(f"{bcolors.FAIL}Error encountered: {bcolors.ENDC}{e}")
    exit(1)

print(cursor_show)
os.system('cls' if os.name == 'nt' else 'clear')
print(f"{bcolors.ENDC}# <{bcolors.OKGREEN}{"=" * prog_bar_len}{bcolors.ENDC}>", flush=True)
print(f"{bcolors.OKGREEN}Process finished in {time.time() - start_time} seconds.{bcolors.ENDC}")