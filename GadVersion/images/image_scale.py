# image_scale.py

__version__ = '2.0'
__author__	= 'Prince Oforh Asiedu'
__date__  	= '18/12/19'

import os
import glob
from pygame.examples.headless_no_windows_needed import scaleit as scale_img

global scale_image_list
global scale_image_dir

def scale_image_list(imglist, width=25, height=25):
	"""
	This function takes a list of images
	and resizes all items in the list to 
	the given height and width.
	"""
	empty_list = []
	
	if imglist:

		try:
			for image in imglist:
				img = image
				img_out = str(image)[:-4]
				img_out = img_out+'out.png'
				scale_img(img, img_out, width, height)

		except Exception as error:
			raise error
	else:
		raise


def scale_image_dir(pathname='',img_format='/*.png', width=25, height=25):
	"""
	This function takes a directory and scans 
	for images in a specified format then it 
	resizes all the images in that format.
	"""
	
	if pathname == '':
		pathname = os.getcwd()

	try:
		dir_imgs = glob.glob(pathname+img_format)
		for image in dir_imgs:
			img_out = str(image)[:-4]
			img_out = img_out+'out.png'
			scale_img(image, img_out, width, height)
	
	except Exception as error:
		raise error

def main():
	scale_image_dir('colored', width=25, height=20)

if __name__ == "__main__":
    main()