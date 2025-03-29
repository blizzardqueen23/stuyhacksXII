import os
from PIL import Image


def generate_pdf_from_directory(directory, output_pdf):
    image_paths = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(".jpg")
    ]

    image_paths.sort()

    if not image_paths:
        print("No JPG images found in the directory.")
        return

    images = [Image.open(image_path).convert("RGB") for image_path in image_paths]

    images[0].save(
        output_pdf, save_all=True, append_images=images[1:], resolution=100.0
    )

    print(f"PDF saved as {output_pdf}")
