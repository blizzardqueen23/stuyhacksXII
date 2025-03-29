from PIL import Image, ImageDraw, ImageFont
import sys
import os

# given a dictionary
# key goes into text for creating collage
# 4 images r chosen from list for value to key to create collage
# can create_collage make a new folder each time or does it have to go into an already created foler


# inputs 4 images
# change to input dictionary
def create_collage(
    images, output_folder="photo_output", collage_size=(900, 1600), text=""
):
    # images is a list of 4 file paths
    # returns the path of the saved collage image

    if len(images) != 4:
        raise ValueError("4 images are required")

    os.makedirs(output_folder, exist_ok=True)

    resized_images = [Image.open(img).resize((495, 330)) for img in images]

    collage = Image.new("RGB", collage_size, (0, 0, 0))

    collage.paste(resized_images[0], (202, 30))
    collage.paste(resized_images[1], (202, 390))
    collage.paste(resized_images[2], (202, 880))
    collage.paste(resized_images[3], (202, 1240))

    # need to add text
    draw = ImageDraw.Draw(collage)
    font = ImageFont.truetype("Courier New Bold", 60)
    new_text = "Top 4 " + text + " Photos"
    text_width = draw.textlength(new_text, font)
    left = (collage_size[0] - text_width) // 2
    text_position = (left, 760)
    draw.text(text_position, new_text, font=font, fill="white")

    collage_filename = (
        f"{output_folder}/collage_{text}{len(os.listdir(output_folder)) + 1}.jpg"
    )
    collage.save(collage_filename)

    return collage_filename


# test = ["../TestImages/00016096_DxO.jpg","../TestImages/00016147_DxO.jpg","../TestImages/00016152_DxO.jpg","../TestImages/00016225_DxO.jpg"]
# collage_path = create_collage(test, text="Spring")
# print(f"Collage saved at: {collage_path}")

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)
from readEXIF import EXIF

reader = EXIF("TestImages")

reader.runSorts()
out = reader.outputDictionary
categories = out.keys()
list_sub = out.values()

final = []

for category, category_data in out.items():
    # print(f"Category: {category}")
    for subcategory, images in category_data.items():
        collage_path = create_collage(images, text=subcategory)
        final.append(collage_path)


def generate_pdf_from_directory(image_paths):
    image_paths.sort()

    images = [Image.open(image_path).convert("RGB") for image_path in image_paths]

    images[0].save(
        output_pdf, save_all=True, append_images=images[1:], resolution=100.0
    )

    print(f"PDF saved as {output_pdf}")


output_pdf = "outputcollage.pdf"
generate_pdf_from_directory(output_pdf)
