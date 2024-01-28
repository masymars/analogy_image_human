import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import imageio
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

from ImageAnalogies import do_image_analogies
from colors import simplifier


def browse_image(label, image_display):
    file_path = filedialog.askopenfilename()
    label.config(text=file_path)
    if file_path:
        load_and_display_image(file_path, image_display)


def load_and_display_image(file_path, image_display):
    img = Image.open(file_path)
    img.thumbnail((100, 100))  # Adjust the size as needed
    img = ImageTk.PhotoImage(img)
    image_display.config(image=img)
    image_display.image = img


def browse_folder(label, image_display):
    folder_path = filedialog.askdirectory()
    label.config(text=folder_path)
    if folder_path:
        load_and_display_images_from_folder(folder_path, image_display)


def load_and_display_images_from_folder(folder_path, image_display):
    # Load and display images from the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if image_files:
        # For simplicity, display only the first image in the folder
        first_image_path = os.path.join(folder_path, image_files[0])
        load_and_display_image(first_image_path, image_display)
    else:
        print("No image files found in the selected folder.")


def run_script():
    # Get the paths to the selected images
    image_A_path = label_A.cget("text")
    image_Amask_path = label_Amask.cget("text")
    image_Bmask_path_folder = label_Bmask.cget("text")
    image_Ap_path = label_Ap.cget("text")
    image_background_path = label_background.cget("text")  # Added Background path
    image_B_path_folder = label_B.cget("text")  # Define image_B_path
    height = entry_h_coarse.get() if entry_h_coarse.get() else "128"
    width = entry_w_coarse.get() if entry_w_coarse.get() else "128"

    # Collect the other parameters from the user or use defaults
    kappa = entry_kappa.get() if entry_kappa.get() else "0.1"
    n_levels = entry_n_levels.get() if entry_n_levels.get() else "3"
    k_coarse = entry_k_coarse.get() if entry_k_coarse.get() else "5"
    k_fine = entry_k_fine.get() if entry_k_fine.get() else "5"

    image_B_files = [f for f in os.listdir(image_B_path_folder) if
                     f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_B_files_paths = [os.path.join(image_B_path_folder, f) for f in image_B_files]

    image_Bmask_files = [f for f in os.listdir(image_Bmask_path_folder) if
                         f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_Bmask_files_paths = [os.path.join(image_Bmask_path_folder, f) for f in image_Bmask_files]
    output_folder = "./output/"
    for index, (image_B_path, image_Bmask_path) in enumerate(zip(image_B_files_paths, image_Bmask_files_paths), 1):
        print(f"Processing Image Analogies for pair {index}:")
        print(f"Image_B Path: {image_B_path}")
        print(f"Image_Bmask Path: {image_Bmask_path}")
        output_Bp_path = f"./output_test/output{index}.png"
        image_Bmask = Image.open(image_Bmask_path)

        # Load the image from image_Ap_path
        image_Ap = Image.open(image_Ap_path)

        # Load the mask from image_Amask_path
        image_Amask = Image.open(image_Amask_path)

        # Ensure that the mask and image have the same dimensions
        if image_Ap.size != image_Amask.size:
            print("Error: Image and mask dimensions do not match.")
        else:
            # Apply the mask to the image
            masked_image = Image.composite(image_Ap, Image.new('RGB', image_Ap.size, (0, 0, 0)), image_Amask)

            # Save the masked image as 'masked.png'
            masked_image.save('masked.png')
            image_Ap_path = './masked.png'
            print("Masked image saved as 'masked.png'.")
        # Call the Image Analogies script with the selected image paths and parameters
        simplifier(image_A_path, "image_A.png")
        simplifier(image_B_path, "image_B.png")
        # image_A_path = "./image_A.png"
        # image_B_path = "./image_B.png"

        image_A = Image.open(image_A_path)

        # Load the mask from image_Amask_path
        image_Amask = Image.open(image_Amask_path)

        # Ensure that the mask and image have the same dimensions
        if image_A.size != image_Amask.size:
            print("Error: Image and mask dimensions do not match.")
        else:
            # Apply the mask to the image
            masked_image = Image.composite(image_A, Image.new('RGB', image_A.size, (0, 0, 0)), image_Amask)

            # Save the masked image as 'masked.png'
            masked_image.save(image_A_path)

            print("Masked image saved as 'masked.png'.")

        image_B = Image.open(image_B_path)

        # Load the mask from image_Amask_path
        image_Bmask = Image.open(image_Bmask_path)

        # Ensure that the mask and image have the same dimensions
        if image_B.size != image_Bmask.size:
            print("Error: Image and mask dimensions do not match.")
        else:
            # Apply the mask to the image
            masked_image = Image.composite(image_B, Image.new('RGB', image_B.size, (0, 0, 0)), image_Bmask)

            # Save the masked image as 'masked.png'
            masked_image.save(image_B_path)

            print("Masked image saved as 'masked.png'.")
        do_image_analogies(int(height), int(width), image_A_path, image_Ap_path, image_B_path, output_Bp_path,
                           Kappa=float(kappa), NLevels=int(n_levels), KCoarse=int(k_coarse), KFine=int(k_fine),
                           debugImages=True)
        # Load the image from image_Ap_path
        image_Bp = Image.open(output_Bp_path)
        image_Bmask = Image.open(image_Bmask_path)

        # Load the background image
        background_image = Image.open(image_background_path)
        # Visualize the three images


        # Ensure that the image_Bp and background image have the same dimensions
        if image_Bp.size != background_image.size:
            print("Error: Image_Bp and background image dimensions do not match.")
        else:
            image_Bp = image_Bp.resize(background_image.size, Image.LANCZOS)
            image_Bmask = image_Bmask.resize(background_image.size, Image.LANCZOS)
            replaced_background_image = Image.composite(image_Bp, background_image, image_Bmask)

            # Save the image with the replaced background
            output_image_path = f'{output_folder}masked_with_background{index}.png'
            replaced_background_image.save(output_image_path)
            print(f"Image with replaced background saved: {output_image_path}")



    # Create a GIF from all images in the output folder
    output_gif_path = "./output/output_animation.gif"
    image_paths = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Sort the image paths based on their creation time
    image_paths.sort(key=os.path.getctime)

    # Create the GIF
    images = [imageio.imread(image_path) for image_path in image_paths]
    imageio.mimsave(output_gif_path, images, duration=0.5)  # Set the duration between frames as needed
    print(f"GIF created and saved: {output_gif_path}")


# Create the main window
root = tk.Tk()
root.title("Image Analogies GUI")

# Create a style for a modern look
style = ttk.Style()
style.configure("TButton", padding=5, relief="flat")

# Labels and buttons for image selection
label_A = ttk.Label(root, text="Select Image A:")
label_A.grid(row=0, column=0, padx=10, pady=5, sticky="w")

image_display_A = ttk.Label(root)
image_display_A.grid(row=0, column=2, padx=10, pady=5)

button_A = ttk.Button(root, text="Browse", command=lambda: browse_image(label_A, image_display_A))
button_A.grid(row=0, column=1, padx=10, pady=5)

label_Amask = ttk.Label(root, text="Select Image Amask:")
label_Amask.grid(row=1, column=0, padx=10, pady=5, sticky="w")

image_display_Amask = ttk.Label(root)
image_display_Amask.grid(row=1, column=2, padx=10, pady=5)

button_Amask = ttk.Button(root, text="Browse", command=lambda: browse_image(label_Amask, image_display_Amask))
button_Amask.grid(row=1, column=1, padx=10, pady=5)

#############################
label_Bmask = ttk.Label(root, text="Select Image Bmask:")
label_Bmask.grid(row=2, column=0, padx=10, pady=5, sticky="w")

image_display_Bmask = ttk.Label(root)
image_display_Bmask.grid(row=2, column=2, padx=10, pady=5)

button_Bmask = ttk.Button(root, text="Browse", command=lambda: browse_folder(label_Bmask, image_display_Bmask))
button_Bmask.grid(row=2, column=1, padx=10, pady=5)

label_Ap = ttk.Label(root, text="Select Image Ap:")  # Added Ap label
label_Ap.grid(row=3, column=0, padx=10, pady=5, sticky="w")

image_display_Ap = ttk.Label(root)
image_display_Ap.grid(row=3, column=2, padx=10, pady=5)

button_Ap = ttk.Button(root, text="Browse", command=lambda: browse_image(label_Ap, image_display_Ap))  # Added Ap button
button_Ap.grid(row=3, column=1, padx=10, pady=5)

label_B = ttk.Label(root, text="Select Image B:")
label_B.grid(row=4, column=0, padx=10, pady=5, sticky="w")

image_display_B = ttk.Label(root)
image_display_B.grid(row=4, column=2, padx=10, pady=5)

button_B = ttk.Button(root, text="Browse", command=lambda: browse_folder(label_B, image_display_B))
button_B.grid(row=4, column=1, padx=10, pady=5)

label_background = ttk.Label(root, text="Select Background Image:")  # Added Background label
label_background.grid(row=5, column=0, padx=10, pady=5, sticky="w")

image_display_background = ttk.Label(root)
image_display_background.grid(row=5, column=2, padx=10, pady=5)

button_background = ttk.Button(root, text="Browse", command=lambda: browse_image(label_background,
                                                                                 image_display_background))  # Added Background button
button_background.grid(row=5, column=1, padx=10, pady=5)

# Entry fields for other parameters with default values
label_kappa = ttk.Label(root, text="Enter Kappa:")
label_kappa.grid(row=6, column=0, padx=10, pady=5, sticky="w")

entry_kappa = ttk.Entry(root)
entry_kappa.insert(0, "0.1")  # Default value
entry_kappa.grid(row=6, column=1, padx=10, pady=5)

label_n_levels = ttk.Label(root, text="Enter NLevels:")
label_n_levels.grid(row=7, column=0, padx=10, pady=5, sticky="w")

entry_n_levels = ttk.Entry(root)
entry_n_levels.insert(0, "3")  # Default value
entry_n_levels.grid(row=7, column=1, padx=10, pady=5)

label_k_coarse = ttk.Label(root, text="Enter KCoarse:")
label_k_coarse.grid(row=8, column=0, padx=10, pady=5, sticky="w")

entry_k_coarse = ttk.Entry(root)
entry_k_coarse.insert(0, "5")  # Default value
entry_k_coarse.grid(row=8, column=1, padx=10, pady=5)

label_k_fine = ttk.Label(root, text="Enter KFine:")
label_k_fine.grid(row=9, column=0, padx=10, pady=5, sticky="w")

entry_k_fine = ttk.Entry(root)
entry_k_fine.insert(0, "5")  # Default value
entry_k_fine.grid(row=9, column=1, padx=10, pady=5)

label_h_coarse = ttk.Label(root, text="Enter height:")
label_h_coarse.grid(row=10, column=0, padx=10, pady=5, sticky="w")

entry_h_coarse = ttk.Entry(root)
entry_h_coarse.insert(0, "128")  # Default value
entry_h_coarse.grid(row=10, column=1, padx=10, pady=5)

label_w_coarse = ttk.Label(root, text="Enter width:")
label_w_coarse.grid(row=11, column=0, padx=10, pady=5, sticky="w")

entry_w_coarse = ttk.Entry(root)
entry_w_coarse.insert(0, "128")  # Default value
entry_w_coarse.grid(row=11, column=1, padx=10, pady=5)

# Button to run the script
run_button = ttk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=12, columnspan=3, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
