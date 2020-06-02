import airsim
import cv2
import numpy as np
import os
import sys
from packages.SAND_features.utils import ops
from pathlib import Path
from packages.SAND_features.models import Sand
import torch
import matplotlib.pyplot as plt
from datetime import datetime

def sand_process(model_type):
	client = airsim.CarClient()
	if getattr(sys, 'frozen', False):
		root = Path(sys._MEIPASS)
	else:
		root = Path(os.path.dirname(os.path.abspath(__file__)))
	print(root.parent)

	# Get image from front vehicle camera
	responses = client.simGetImages([
		airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])  
	response = responses[0]

	img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8) 
	img_rgb = img1d.reshape(response.height, response.width, 3)

	# SAND Processing Image
	device = ops.get_device()


	model_path = model_type.split('_')
	if model_path[0] == '3':
		model_path[0] = '3/'
	if model_path[0] == '10':
		model_path[0] = '10/'
	if model_path[0] == '32':
		model_path[0] = '32/'	

	if model_path[1] == 'G':
		model_path[1] = 'ckpt_G'
	if model_path[1] == 'L':
		model_path[1] = 'ckpt_L'
	if model_path[1] == 'GL':
		model_path[1] = 'ckpt_GL'

	test_path = (root/'packages'/'ckpts'/model_path[0]/model_path[1])
	print(test_path)
	ckpt_file = (root/'packages'/'ckpts'/model_path[0]/model_path[1]).with_suffix('.pt')

	img_torch = ops.img2torch(img_rgb, batched=True).to(device)

	model = Sand.from_ckpt(ckpt_file).to(device)
	model.eval()

	with torch.no_grad():
		features_torch = model(img_torch)

	# Convert features into an images we can visualize (by PCA or normalizing)
	features_np = ops.fmap2img(features_torch).squeeze(0)
	trunct_name = model_type.replace('_','')
	image_name = trunct_name + '-' + datetime.now().strftime("%H%M%S%f")[:-3] + '.png'
	# model_folder = ''
	# if trunct_name == '3L' or trunct_name == '3G' or trunct_name == '3GL':
	# 	model_folder = '3'
	# if trunct_name == '10L' or trunct_name == '10G' or trunct_name == '10GL':
	# 	model_folder = '10'
	# if trunct_name == '32L' or trunct_name == '32G' or trunct_name == '32GL':
	# 	model_folder = '32'
	save_path = root/'SAND_Images'/trunct_name/image_name
	plt.imsave(save_path, features_np)

	return str(save_path)



		



