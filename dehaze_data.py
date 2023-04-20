import os
import cv2
import numpy as np

def dehaze(image: np.array):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    f = np.fft.fft2(image_gray)
    f_shift = np.fft.fftshift(f)

    rows, cols = image_gray.shape
    crow, ccol = rows//2, cols//2
    radius = 50
    mask = np.full((rows, cols), 1, np.uint8)
    cv2.circle(mask, (crow, ccol), radius, 0, -1)
    mask = np.fft.fftshift(mask)

    f_shift_filtered = f_shift * mask
    f_filtered = np.fft.ifftshift(f_shift_filtered)
    image_dehazed_gray = np.abs(np.fft.ifft2(f_filtered))
    image_dehazed_gray = cv2.normalize(image_dehazed_gray, None, 0, 255, cv2.NORM_MINMAX)  
    image_dehazed_gray = np.uint8(image_dehazed_gray)

    image_dehazed = cv2.cvtColor(image_dehazed_gray, cv2.COLOR_GRAY2BGR)

    sigma_color = 10  
    sigma_space = 10  
    image_dehazed = cv2.bilateralFilter(image_dehazed, -1, sigma_color, sigma_space)

    image_dehazed_gray = cv2.cvtColor(image_dehazed, cv2.COLOR_BGR2GRAY)

    image_dehazed_gray = cv2.normalize(image_dehazed_gray, None, 0, 255, cv2.NORM_MINMAX)

    return image_dehazed_gray

source = "./dataset/hazy_images/"
dest = "./dataset/dehazed_images/"
images = os.listdir(source)
for image in images:
    img = cv2.imread(source+image)
    destination = (dest+image[:-4]+"_dehazed"+image[-4:])
    cv2.imwrite(destination,dehaze(img))