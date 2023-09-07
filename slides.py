#!/usr/bin/env python
# App to present images as a slideshow in a predefined window (not full screen).
# The command line argument must be the folder name containing the images.
# with quotes required only if path includes spaces.
# Last update: Sep. 7 2023
# Author: Perry E. Radau

import tkinter as tk
from PIL import Image, ImageTk
import os
import imghdr
import sys
import argparse
import random

PAUSE = 2000 #pause time in milliseconds between images
SIZE = 500 #width and height of display window. 500 is small, 1280 is large.

class Slideshow:
    #size of the image window (fixed)
    width = SIZE
    height = width

    
    def __init__(self, folder):
        self.folder = folder
        self.bLoop = False #set to true for continuous looping
        self.bFirstTime = True #check if this is the first time through the loop.
        self.window = tk.Tk()
        #indices that have been shown
        self.shown_indices = set()

        # Position the window at coordinates (x, y)
        # get monitor display size
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        #Place the display window in the center of the monitor (can be changed by user)
        # NOTE: x=y=0 means top left corner. 
        # center of monitor
        # x = screen_width // 2 - Slideshow.width // 2
        # y = screen_height // 2 - Slideshow.height // 2
        # bottom right hand corner
        x = screen_width - Slideshow.width
        y = screen_height - Slideshow.height


        self.window.geometry(f"{Slideshow.width}x{Slideshow.height}+{x}+{y}")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Make the canvas fill the window

        self.current_image_index = -1
        self.images = self.get_images()

        self.show_next_image()
        self.window.mainloop()


    def get_images(self):
        # Get list of image file names in folder
        image_folder = self.folder  

        image_files = []
        for file_name in os.listdir(image_folder):
            file_path = os.path.join(image_folder, file_name)
            if os.path.isfile(file_path) and imghdr.what(file_path):
                image_files.append(file_name)
        return image_files
    

    def get_next_image(self):
        # print(f"index={self.current_image_index}")
        # Check if all images have been shown
        if len(self.images) == len(self.shown_indices):
            if not self.bLoop:
                print("DONE!")
                sys.exit(0)
            else:
                # Reset the previously shown image set to start the loop again
                self.shown_indices = set()

        # Create a list of indices excluding the previously shown images
        available_indices = [i for i in range(len(self.images)) if i not in self.shown_indices]

        # Select a random index from the available indices
        self.current_image_index = random.choice(available_indices)

        # Add the current index to the set of shown indices
        self.shown_indices.add(self.current_image_index)

        return self.images[self.current_image_index]


    def load_image(self, path, target_size):
        # print(f"Loading {path}")
        img = Image.open(path)
        # print(f"Original size is {img.size}")

        # Calculate the scaled size to fit into the window
        window_width, window_height = target_size
        scaled_size = self.calculate_scaled_size(img.size, (window_width, window_height))

        # Resize the image
        img = img.resize(scaled_size)
        # print(f"Scaled size is {img.size}")

        return ImageTk.PhotoImage(img)
    

    def show_image(self, img):
        # print(f"Showing image of size {img.width()}x{img.height()}")
        self.canvas.delete("all")  # Clear the canvas before showing a new image
        self.canvas.config(width=img.width(), height=img.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)


    def show_next_image(self):
        name = self.get_next_image()

        try:
            self.current_image = self.load_image(os.path.join(self.folder, name), (Slideshow.width, Slideshow.height))
            self.show_image(self.current_image)
        except Exception as e:
            print(f"Error loading image: {e}")
            self.current_image = None
            print(f"name = {name}")
            sys.exit(0)

        self.window.after(PAUSE, self.show_next_image)


    def calculate_scaled_size(self, original_size, target_size):
        original_width, original_height = original_size
        target_width, target_height = target_size

        width_ratio = target_width / original_width
        height_ratio = target_height / original_height

        # Choose the smaller ratio to ensure the image fits within the target size
        scale_ratio = min(width_ratio, height_ratio)

        scaled_width = int(original_width * scale_ratio)
        scaled_height = int(original_height * scale_ratio)
        # print(f"original {original_size}")
        # print(f"target {target_size}")
        return (scaled_width, scaled_height)


def main():
    parser = argparse.ArgumentParser(description='Image Slideshow')
    parser.add_argument('folder', help='Path to the image folder')
    args = parser.parse_args()

    Slideshow(args.folder)

if __name__ == '__main__':
    main()