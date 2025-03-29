from PIL import Image, ImageDraw, ImageFont
import random
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

from readEXIF import EXIF


def draw_centered_text(draw, text, y, font, image_width=900, fill="white"):
    text_width, _ = draw.textsize(text, font=font)
    x = (image_width - text_width) // 2
    draw.text((x, y), text, font=font, fill=fill)


def create_wrapped_slide(
    output_path, photo_count, camera, season, time, location, locList, resolution
):

    font_large = ImageFont.truetype("wrapped/Roboto-SemiBold.ttf", 140)
    font_medium = ImageFont.truetype("wrapped/Roboto-SemiBold.ttf", 100)
    font_small = ImageFont.truetype("wrapped/Roboto-SemiBold.ttf", 75)

    bg_color = random.choice(["#1DB954", "#191414", "#FFAA33", "#FF5733", "#800080"])
    image = Image.new("RGB", (900, 1600), color=bg_color)
    draw = ImageDraw.Draw(image)

    draw.text((50, 200), "Your\n2025\nPhoto\nWrapped", font=font_large, fill="white")

    image.save(output_path + "slide1" + ".jpg")
    print(f"Slide saved: {output_path}")

    bg_color = random.choice(["#1DB954", "#191414", "#FFAA33", "#FF5733", "#800080"])
    image = Image.new("RGB", (900, 1600), color=bg_color)
    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 200),
        "You\ntook\n" + str(photo_count) + "\nphotos",
        font=font_large,
        fill="white",
    )

    image.save(output_path + "slide2" + ".jpg")
    print(f"Slide saved: {output_path}")

    bg_color = random.choice(["#1DB954", "#191414", "#FFAA33", "#FF5733", "#800080"])
    image = Image.new("RGB", (900, 1600), color=bg_color)
    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 200),
        "You took\nthe most\nphotos in\n"
        + location
        + "\nwith a\ntotal of\n"
        + str(len(locList[location])),
        font=font_large,
        fill="white",
    )

    image.save(output_path + "slide3" + ".jpg")
    print(f"Slide saved: {output_path}")

    bg_color = random.choice(["#1DB954", "#191414", "#FFAA33", "#FF5733", "#800080"])
    image = Image.new("RGB", (900, 1600), color=bg_color)
    draw = ImageDraw.Draw(image)

    counter = 0
    freq = ""
    for c in camera:
        if len(camera[c]) > counter:
            freq = c
            counter = len(c)

    draw.text(
        (50, 150),
        "...and you\nused the\n"
        + c
        + "\nwith "
        + str(int(100 * counter / photo_count))
        + "\npictures taken\non it",
        font=font_small,
        fill="white",
    )

    image.save(output_path + "slide4" + ".jpg")
    print(f"Slide saved: {output_path}")

    bg_color = random.choice(["#1DB954", "#191414", "#FFAA33", "#FF5733", "#800080"])
    image = Image.new("RGB", (900, 1600), color=bg_color)
    draw = ImageDraw.Draw(image)

    counter = 0
    freq = ""
    for s in season:
        if len(season[s]) > counter:
            freq = s
            counter = len(s)

    draw.text(
        (50, 200),
        "You took\npictures\nmost\nfrequently in\nthe " + str(s),
        font=font_large,
        fill="white",
    )

    image.save(output_path + "slide5" + ".jpg")
    print(f"Slide saved: {output_path}")

    bg_color = random.choice(["#1DB954", "#191414", "#FFAA33", "#FF5733", "#800080"])
    image = Image.new("RGB", (900, 1600), color=bg_color)
    draw = ImageDraw.Draw(image)

    counter = 0
    freq = ""
    for t in time:
        if len(time[t]) > counter:
            freq = t
            counter = len(t)

    draw.text(
        (50, 200),
        "And lastly,\nyou usually\ntook pictures\nin the \n" + str(t).lower(),
        font=font_medium,
        fill="white",
    )

    image.save(output_path + "slide6" + ".jpg")
    print(f"Slide saved: {output_path}")


reader = EXIF("TestImages")

reader.runSorts()

out = reader.outputDictionary

mC = ""
counter = 0
for country, list in out["Country"].items():
    if len(list) > counter:
        counter = len(list)
        mC = country

countryList = out["Country"]
if mC == "United States":
    countryList = out["State"]
    mS = ""
    counter = 0
    for state, list in out["State"].items():
        if len(list) > counter:
            counter = len(list)
            mS = state
    mC = mS

create_wrapped_slide(
    "wrapped/testout/wrapped_slide",
    photo_count=len(reader.filePathList),
    camera=out["Camera"],
    season=out["Season"],
    time=out["Time"],
    location=mC,
    locList=countryList,
    resolution=out["Resolution"],
)


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


directory = "wrapped/testout"
output_pdf = "output.pdf"
generate_pdf_from_directory(directory, output_pdf)
