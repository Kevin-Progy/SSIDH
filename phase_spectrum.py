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
phase_spectrum = np.angle(fshift)

# Normalize the pixel values of the phase spectrum
phase_spectrum = cv2.normalize(phase_spectrum, None, 0, 255, cv2.NORM_MINMAX)
phase_spectrum = np.uint8(phase_spectrum)

# Display the phase spectrum
cv2.imshow('Phase Spectrum', phase_spectrum)
cv2.waitKey(0)
cv2.destroyAllWindows()

