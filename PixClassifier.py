
import os
from tkinter import Tk, Label, Button, filedialog, messagebox, ttk, PhotoImage
from PIL import Image
import cv2
import shutil
import gc  # Garbage collection

# Function to calculate noise using Laplacian variance
def calculate_noise(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        variance = cv2.Laplacian(img, cv2.CV_64F).var()
        del img  # Explicitly delete the image from memory
        return variance
    except Exception as e:
        print(f"Error calculating noise for {image_path}: {e}")
        return None

# Function to classify noise level
def classify_noise(variance, quality_category):
    if variance is None:
        return None
    if quality_category in ["High_Quality", "Medium_Quality"]:
        # Prioritize quality over noise for good-quality images
        return None
    if variance > 100:
        return "High_Noise"
    elif 50 <= variance <= 100:
        return "Medium_Noise"
    else:
        return "Low_Noise"

# Function to classify image size
def classify_size(width, height):
    if width < 800 and height < 600:
        return "Small_Size"
    elif 800 <= width < 1920 and 600 <= height < 1080:
        return "Medium_Size"
    else:
        return "Large_Size"

# Function to classify image quality
def classify_image(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            dpi = img.info.get("dpi", (72, 72))[0]
            resolution = width * height
            
            # Classify size
            size_category = classify_size(width, height)

            # Ensure the file is closed before calculating noise
            noise_variance = calculate_noise(image_path)

            # Classify quality
            if dpi >= 300 and resolution > 6000000:
                quality_category = "High_Quality"
            elif dpi >= 150 and resolution > 2000000:
                quality_category = "Medium_Quality"
            else:
                quality_category = "Low_Quality"

            # Classify noise, but only override for low-quality images
            noise_category = classify_noise(noise_variance, quality_category)
            
            return quality_category, size_category, noise_category
    except Exception as e:
        print(f"Error analyzing {image_path}: {e}")
        return None, None, None

# Function to process images
def process_images(input_folder, output_folder, progress_bar, total_files):
    # Create subfolders
    quality_folders = {
        "High_Quality": os.path.join(output_folder, "High_Quality"),
        "Medium_Quality": os.path.join(output_folder, "Medium_Quality"),
        "Low_Quality": os.path.join(output_folder, "Low_Quality"),
        "Small_Size": os.path.join(output_folder, "Small_Size"),
        "Medium_Size": os.path.join(output_folder, "Medium_Size"),
        "Large_Size": os.path.join(output_folder, "Large_Size"),
        "High_Noise": os.path.join(output_folder, "High_Noise"),
        "Medium_Noise": os.path.join(output_folder, "Medium_Noise"),
        "Low_Noise": os.path.join(output_folder, "Low_Noise"),
    }
    for folder in quality_folders.values():
        os.makedirs(folder, exist_ok=True)

    processed_files = 0

    # Analyze and sort images
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(input_folder, file_name)
            quality, size, noise = classify_image(image_path)
            
            # Handle duplicates: prioritize quality > noise > size
            try:
                target_folder = None
                if quality == "High_Quality":
                    target_folder = quality_folders["High_Quality"]
                elif quality == "Medium_Quality":
                    target_folder = quality_folders["Medium_Quality"]
                elif noise == "High_Noise":
                    target_folder = quality_folders["High_Noise"]
                elif noise == "Medium_Noise":
                    target_folder = quality_folders["Medium_Noise"]
                elif noise == "Low_Noise":
                    target_folder = quality_folders["Low_Noise"]
                elif quality == "Low_Quality":
                    target_folder = quality_folders["Low_Quality"]
                
                # Copy to the chosen target folder
                if target_folder:
                    shutil.copy(image_path, os.path.join(target_folder, file_name))
                    print(f"{file_name} -> {os.path.basename(target_folder)}")

                # Update progress
                processed_files += 1
                progress = int((processed_files / total_files) * 100)
                progress_bar["value"] = progress
                progress_bar.update()

                # Explicitly clear resources
                gc.collect()
            except Exception as e:
                print(f"Error copying {file_name}: {e}")

    # Remove empty folders
    for folder, path in quality_folders.items():
        if not os.listdir(path):  # Check if folder is empty
            os.rmdir(path)  # Remove empty folder
            print(f"Removed empty folder: {path}")

    messagebox.showinfo("Processing Completed", "Images have been successfully processed and sorted!")

# Tkinter GUI
def select_input_folder():
    folder = filedialog.askdirectory(title="Select Input Folder")
    if folder:
        input_folder_label.config(text=f"Input Folder: {folder}")
        input_folder_label.folder = folder

def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_folder_label.config(text=f"Output Folder: {folder}")
        output_folder_label.folder = folder

def start_processing():
    input_folder = getattr(input_folder_label, "folder", None)
    output_folder = getattr(output_folder_label, "folder", None)

    if not input_folder or not output_folder:
        messagebox.showerror("Error", "Please select both input and output folders!")
        return

    # Check if output folder exists and contains data
    if os.path.exists(output_folder) and os.listdir(output_folder):
        response = messagebox.askyesno(
            "Warning",
            "The destination folder contains data. Do you want to delete it and proceed?"
        )
        if response:  # User agrees to delete
            shutil.rmtree(output_folder)  # Remove the folder and its contents
            os.makedirs(output_folder)  # Recreate the empty folder
        else:  # User cancels
            messagebox.showinfo("Operation Cancelled", "Please choose another output folder.")
            return
    elif not os.path.exists(output_folder):  # If folder doesn't exist, create it
        os.makedirs(output_folder)

    # Count total files
    total_files = sum(1 for file in os.listdir(input_folder) if file.lower().endswith((".jpg", ".jpeg", ".png")))
    if total_files == 0:
        messagebox.showwarning("No Images", "No images found in the selected input folder.")
        return

    # Start processing with progress bar
    progress_bar["value"] = 0
    process_images(input_folder, output_folder, progress_bar, total_files)

# Create Tkinter window
root = Tk()
root.title("PixClassifier")
root.geometry("500x300")

# Set the window icon
try:
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon_clean.png")
    icon = PhotoImage(file=icon_path)
    root.iconphoto(True, icon)
except Exception as e:
    print(f"Error loading icon: {e}")

# Labels and Buttons
Label(root, text="Select folders to analyze and classify images").pack(pady=10)

Button(root, text="Select Input Folder", command=select_input_folder).pack(pady=5)
input_folder_label = Label(root, text="Input Folder: Not selected", wraplength=400)
input_folder_label.pack(pady=5)

Button(root, text="Select Output Folder", command=select_output_folder).pack(pady=5)
output_folder_label = Label(root, text="Output Folder: Not selected", wraplength=400)
output_folder_label.pack(pady=5)

Button(root, text="Start Processing", command=start_processing, bg="green", fg="white").pack(pady=20)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

root.mainloop()
