from PIL import Image
import numpy as np
from pathlib import Path
import os
import math
import time

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

def get_average_color(image: Image.Image):
    image = image.convert("RGB")
    npimg = np.array(image)
    avg_color = np.mean(npimg, axis=(0,1))
    return tuple(avg_color.astype(int))

def closest_color_index(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color)**2, axis=1))
    idx = np.where(distances == np.amin(distances))[0]
    if len(idx) == 1:
        return idx.item()
    else: return idx[0]
start_time = time.time()
input_image = Image.open("FFp7m8w.jpeg")
image_ar = input_image.height / input_image.width
input_width = 512
input_resize = (input_width, round(input_width * image_ar))
src_resize = (64, 64)
input_image = input_image.resize(input_resize).convert("RGB")
image_sources = get_files_in_dir("source-images")

source_images = []

cursor_hide = '\033[?25l'
cursor_show ='\033[?25h'

for i in image_sources:
    source_images.append(Image.open(i).resize(src_resize).convert("RGB"))

new_img = Image.new("RGBA", (input_resize[0] * src_resize[0], input_resize[1] * src_resize[1]))

width, height = input_image.size
total = new_img.width * new_img.height
last_prog = -1
prog_bar_len = 20
print(cursor_hide)
try:
    for x in range(width):
        for y in range(height):
            p = input_image.getpixel((x, y))
            color_closest_index = closest_color_index([get_average_color(i) for i in source_images], p)
            img_to_paste: Image.Image = source_images[color_closest_index]
            if (autotune):
                img_to_paste = Image.blend(img_to_paste, Image.new('RGB', img_to_paste.size, p), autotune_intensity)
            new_img.paste(img_to_paste, (x * img_to_paste.size[0], y * img_to_paste.size[1]))
        prog = math.floor((x / width) * prog_bar_len)
        if prog != last_prog:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{bcolors.ENDC}# <{bcolors.OKGREEN}{"=" * prog}{bcolors.ENDC}{"-" * (prog_bar_len - prog)}>", end='\r', flush=True)
        last_prog = prog

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