import cv2
import numpy as np

# threshold = 2
# # Load the image
# img = cv2.imread('solid_color_image.jpg')
#
# # Convert to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Apply thresholding to create a binary image
# thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
# # Find contours in the binary image
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # Loop through all the contours and check if they are artifacts
# average = np.average(gray)
# for contour in contours:
#     # Compute the area of the contour
#     area = cv2.contourArea(contour)
#
#     # If the area is smaller than a threshold, it is an artifact
#     if area > average + threshold or area < average - threshold:
#         # Draw a rectangle around the artifact
#         x, y, w, h = cv2.boundingRect(contour)
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
# # Display the result
# cv2.imshow('Result', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


##################################3

# Load the image
# img = cv2.imread('solid_color_image.jpg')
#
# # Convert the image to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Apply Canny edge detection to detect edges
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)
#
# # Apply Hough transform to detect lines in the image
# lines = cv2.HoughLines(edges, 1, 3.14 / 180, 100)
#
# # Draw the detected lines on the original image
# if lines is not None:
#     for line in lines:
#         rho, theta = line[0]
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 1000 * (-b))
#         y1 = int(y0 + 1000 * (a))
#         x2 = int(x0 - 1000 * (-b))
#         y2 = int(y0 - 1000 * (a))
#         cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
# # Display the result
# cv2.imshow('Result', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#####################################################################

# Let's load a simple image with 3 black squares
image = cv2.imread('solid_color_image.jpg')
cv2.waitKey(0)

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 50, 80)

radius = 111
gray = cv2.GaussianBlur(gray, (radius, radius), 2)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
cv2.rectangle(image, (maxLoc[0] - radius//2, maxLoc[1]-radius//2), (maxLoc[0]+radius//2, maxLoc[1]+radius//2), (0, 255, 0), 1)
cv2.rectangle(image, (minLoc[0] - radius//2, minLoc[1]-radius//2), (minLoc[0]+radius//2, minLoc[1]+radius//2), (0, 255, 0), 1)

# Finding Contours
# Use a copy of the image e.g. edged.copy()
# since findContours alters the image
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

print("Number of Contours found = " + str(len(contours)))

# Draw all contours
# -1 signifies drawing all contours
cv2.drawContours(image, contours, -1, (0, 0, 255), 1)

cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
