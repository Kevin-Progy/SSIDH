import argparse
import cv2
import numpy as np

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required=True, help='path to input image')
args = parser.parse_args()

# Load the image in grayscale
image = cv2.imread(args.image, 0)

# Perform Fourier Transform
f = np.fft.fft2(image)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20 * np.log(np.abs(fshift))

# Normalize magnitude spectrum for display
magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# Display original image and its Fourier Transform
cv2.imshow('Input Image', image)
cv2.imshow('Magnitude Spectrum', magnitude_spectrum)
cv2.waitKey(0)
cv2.destroyAllWindows()

