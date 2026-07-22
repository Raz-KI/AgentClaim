import cv2
import numpy as np

def crop_to_document(image_path):
    # Load image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to separate the white page from the black background
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Get the largest contour (the white page)
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Crop the image with a tiny 5px padding so text isn't cut off
        cropped = img[max(0, y-5):min(img.shape[0], y+h+5), max(0, x-5):min(img.shape[1], x+w+5)]
        
        # Save it back or return it
        cv2.imwrite(image_path, cropped)