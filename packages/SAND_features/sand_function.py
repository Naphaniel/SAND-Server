# ---Stdlib---
import sys
import os
from pathlib import Path
from typing import List

# ---Dependencies---
import torch
from imageio import imread
import matplotlib.pyplot as plt
import image_slicer
import subprocess

from packages.SAND_features.utils import ops
from packages.SAND_features.models import Sand


def split_image(image_name: str) -> None:
    print(f'Splitting {image_name}')
    tiles = image_slicer.slice(image_name, 4)
    image_slicer.save_tiles(tiles)

def combine_images(output_path: str, img: str, model_name: str) -> None:
    print(f'Combining {img}')
    subprocess.run(["magick", "convert", img + "_01_01.png", img + "_01_02.png", "+append" ,"temp.png"], cwd=output_path, shell=True)
    subprocess.run(["magick", "convert", img + "_02_01.png", img + "_02_02.png", "+append" ,"temp1.png"], cwd=output_path, shell=True)
    if model_name == '':
        subprocess.run(["magick", "convert", "temp.png", "temp1.png", "-append" , img + ".png"], cwd=output_path, shell=True)
    else:
        subprocess.run(["magick", "convert", "temp.png", "temp1.png", "-append" , model_name + "_" + img + ".png"], cwd=output_path, shell=True)
    os.remove(output_path + "/" + img + "_01_01.png")
    os.remove(output_path + "/" + img + "_01_02.png")
    os.remove(output_path + "/" + img + "_02_01.png")
    os.remove(output_path + "/" + img + "_02_02.png")
    os.remove(output_path + "/" + "temp.png")
    os.remove(output_path + "/" + "temp1.png")



def sand_function(model_name: str, image_path: str, output_path: str, img_index_range: List[int] = None) -> None:
    root = Path(__file__) .parent  # Path to repo
    if root not in sys.path:
        sys.path.insert(0, root)  # Prepend to path so we can use these modules

    model_path = root/'ckpts'

    device = ops.get_device()

    ckpt_file = Path(model_path, model_name).with_suffix('.pt')

    model_name_trim = ''


    if model_name == '3/ckpt_G':
        model_name_trim = '3G'
    if model_name == '3/ckpt_L':
        model_name_trim = '3L'
    if model_name == '3/ckpt_GL':
        model_name_trim = '3GL'
    if model_name == '10/ckpt_G':
        model_name_trim = '10G'
    if model_name == '10/ckpt_L':
        model_name_trim = '10L'
    if model_name == '10/ckpt_GL':
        model_name_trim = '10GL'
    if model_name == '32/ckpt_G':
        model_name_trim = '32G'
    if model_name == '32/ckpt_L':
        model_name_trim = '32L'
    if model_name == '32/ckpt_GL':
        model_name_trim = '32GL'


    images = []
    for filename in os.listdir(image_path):

        if filename.endswith('.jpg'):

            split_image(image_path+filename)
            os.remove(image_path + filename)
      
   
    for filename in os.listdir(image_path):
        if filename.endswith('.png'):
            images.append(filename)

    images.sort()

    start_point = 0
    end_point = len(images) - 1
    if img_index_range:
        start_point = img_index_range[0]
        end_point = img_index_range[1]

    for i in range(start_point, end_point + 1):
        print(f'Processing {images[i]}.')
        img_file = Path(image_path + '/' + images[i])

        # Load image & convert to torch format
        img_np = imread(img_file)
        img_torch = ops.img2torch(img_np, batched=True).to(device)

        # Create & load model (single branch)
        model = Sand.from_ckpt(ckpt_file).to(device)
        model.eval()

        # Run inference
        with torch.no_grad():
            features_torch = model(img_torch)

        # Convert features into an images we can visualize (by PCA or normalizing)
        features_np = ops.fmap2img(features_torch).squeeze(0)
        plt.imsave(output_path + '/' + images[i], features_np)

        curr_img = ''.join(images[i].split())[:-10]

        if (i + 1) % 4 == 0:
            combine_images(output_path, curr_img, model_name_trim)
            combine_images(image_path, curr_img, model_name_trim)




