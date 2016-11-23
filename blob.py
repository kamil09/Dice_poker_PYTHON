import cv2

__blobSettings__ = cv2.SimpleBlobDetector_Params()

# Change thresholds
__blobSettings__.minThreshold = 10;
__blobSettings__.maxThreshold = 200;

# Filter by Area.
__blobSettings__.filterByArea = True
__blobSettings__.minArea = 1500

# Filter by Circularity
__blobSettings__.filterByCircularity = True
__blobSettings__.minCircularity = 0.1

# Filter by Convexity
__blobSettings__.filterByConvexity = True
__blobSettings__.minConvexity = 0.87

# Filter by Inertia
__blobSettings__.filterByInertia = True
__blobSettings__.minInertiaRatio = 0.01

