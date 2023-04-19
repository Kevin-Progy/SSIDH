import cv2
import numpy as np
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# Load the hazy image
image = cv2.imread(args["image"], cv2.IMREAD_COLOR)

# Step 1: Convert the image to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Step 2: Perform Fourier transform on the grayscale image
f = np.fft.fft2(image_gray)

# Step 3: Shift the zero frequency component to the center of the spectrum
f_shift = np.fft.fftshift(f)

# Step 4: Design a filter to attenuate high-frequency components (haze)
rows, cols = image_gray.shape
crow, ccol = rows//2, cols//2  # center of the image
radius = 50  # radius of the circular filter
mask = np.full((rows, cols), 1, np.uint8)
cv2.circle(mask, (crow, ccol), radius, 0, -1)  # create a circular mask
mask = np.fft.fftshift(mask)  # shift the mask to match the Fourier spectrum

# Step 5: Apply the filter to the Fourier spectrum
f_shift_filtered = f_shift * mask

# Step 6: Shift the zero frequency component back to the original position
f_filtered = np.fft.ifftshift(f_shift_filtered)

# Step 7: Perform inverse Fourier transform to obtain the dehazed image
image_dehazed_gray = np.abs(np.fft.ifft2(f_filtered))
image_dehazed_gray = cv2.normalize(image_dehazed_gray, None, 0, 255, cv2.NORM_MINMAX)  # Normalize the pixel values
image_dehazed_gray = np.uint8(image_dehazed_gray)

# Step 8: Convert the dehazed grayscale image to color format
image_dehazed = cv2.cvtColor(image_dehazed_gray, cv2.COLOR_GRAY2BGR)

# Step 9: Apply bilateral filtering to the dehazed color image
sigma_color = 10  # Controls the color smoothing strength
sigma_space = 10  # Controls the spatial smoothing strength
image_dehazed = cv2.bilateralFilter(image_dehazed, -1, sigma_color, sigma_space)

# Step 10: Convert the dehazed color image back to grayscale
image_dehazed_gray = cv2.cvtColor(image_dehazed, cv2.COLOR_BGR2GRAY)

# Step 11: Normalize the pixel values of the dehazed grayscale image
image_dehazed_gray = cv2.normalize(image_dehazed_gray, None, 0, 255, cv2.NORM_MINMAX)

# Display the original hazy image and dehazed image
cv2.imshow('Hazy Image', image)
cv2.imshow('Dehazed Image', image_dehazed_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

