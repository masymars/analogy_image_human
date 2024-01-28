import random

import cv2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def extract_colors(input_image_path, num_clusters=5):
    # Open the image
    image = Image.open(input_image_path)

    # Convert the image to RGB mode (if it's not already)
    image = image.convert("RGB")

    # Convert the image data to a NumPy array
    image_data = np.array(image)

    # Reshape the data to a 2D array of RGB values
    pixels = image_data.reshape(-1, 3)

    # Perform K-means clustering to group similar colors
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(pixels)

    # Get the cluster centers (representative colors)
    cluster_centers = kmeans.cluster_centers_.astype(int)

    # Convert the cluster centers back to RGB format
    unique_colors_list = [tuple(rgb) for rgb in cluster_centers]

    return unique_colors_list
def generate_distinct_colors(n):
    """ Generate n visually distinct colors. """
    colors = []
    for _ in range(n):
        colors.append([random.randint(0, 255) for _ in range(3)])
    return colors
def rebuild_image(input_image_path, representative_colors):
    # Open the image
    image = Image.open(input_image_path)

    # Convert the image to RGB mode (if it's not already)
    image = image.convert("RGB")

    # Convert the image data to a NumPy array
    image_data = np.array(image)

    # Reshape the data to a 2D array of RGB values
    pixels = image_data.reshape(-1, 3)

    # Perform K-means clustering to find the nearest representative color for each pixel
    kmeans = KMeans(n_clusters=len(representative_colors), init=np.array(representative_colors), n_init=1)
    labels = kmeans.fit_predict(pixels)

    # Replace pixel values with the nearest representative colors
    new_pixels = np.array(representative_colors)[labels]

    # Reshape the pixel data back to the original image shape
    new_image_data = new_pixels.reshape(image_data.shape)

    # Create a PIL image from the modified data
    new_image = Image.fromarray(new_image_data.astype('uint8'), 'RGB')

    return new_image

def simplifier(input_image_path, save_path):
    num_clusters = 10  # Number of clusters/colors

    # Generate random, distinct colors
    random_colors = extract_colors(input_image_path,num_clusters)
    print(random_colors)

    rebuilt_image = rebuild_image(input_image_path, random_colors)

    # Save the rebuilt image
    rebuilt_image.save(save_path)

if __name__ == "__main__":
    input_image_path = "dense.png"  # Replace with your input image path
    simplifier(input_image_path , "./denses.png")
