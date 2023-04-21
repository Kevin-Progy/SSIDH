import cv2
from skimage.metrics import structural_similarity
import numpy as np
import os

def metrics(img1_path, img2_path):
    # Load the original and distorted images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Calculate PSNR
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        psnr = 100
    else:
        pixel_max = 255.0
        psnr = 20 * np.log10(pixel_max / np.sqrt(mse))

    gray_image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate SSIM
    ssim = structural_similarity(gray_image1, gray_image2)
    return psnr, ssim


source = "./dataset/hazy_images/"
dest = "./dataset/dehazed_images/"
images = os.listdir(source)

psnr_total = 0
ssim_total = 0

for image in images:
    psnr, ssim = metrics(source+image, dest+image[:-4]+"_dehazed"+image[-4:])
    psnr_total += psnr
    ssim_total += ssim

psnr = psnr_total/len(images)
ssim = ssim_total/len(images)

print("PSNR:", psnr)
print("SSIM:", ssim)
