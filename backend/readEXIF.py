import json
from PIL import Image
from pillow_heif import register_heif_opener
from listFiles import get_image_files
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
from geopy.geocoders import Nominatim
from datetime import time

import exiftool

register_heif_opener()


class EXIF:
    def __init__(self, folderPath):
        self.filePathList = get_image_files(folderPath)
        self.outputDictionary = {}
        self.outputDictionary["Time"] = {
            "Late Night": [],
            "Morning": [],
            "Afternoon": [],
            "Evening": [],
        }
        self.outputDictionary["Season"] = {
            "Spring": [],
            "Summer": [],
            "Fall": [],
            "Winter": [],
        }
        self.outputDictionary["Camera"] = {}
        self.outputDictionary["Lens"] = {
            "Ultrawide": [],
            "Standard": [],
            "Telephoto": [],
        }
        self.outputDictionary["Resolution"] = {
            "sub-4K": [],
            "4K": [],
            "6K": [],
            "8K": [],
        }
        self.outputDictionary["Aspect"] = []
        self.outputDictionary["State"] = {}
        self.outputDictionary["Country"] = {}

    def get_exif_data(self, image_path):
        PILimage = Image.open(image_path)
        width, height = PILimage.size

        with exiftool.ExifTool() as et:
            raw_metadata = et.execute(
                b"-json", image_path.encode()
            )  # Run ExifTool and get JSON output
            metadata = json.loads(raw_metadata)[0]

        # Extract metadata fields
        time_original = metadata.get("EXIF:DateTimeOriginal") or metadata.get(
            "EXIF:CreateDate"
        )
        camera_model = metadata.get("EXIF:Model", "Unknown")
        lens_model = metadata.get("EXIF:LensModel", "Unknown")
        flash_fired = metadata.get("EXIF:Flash", "No Flash") != "No Flash"
        aspect_ratio = round(width / height, 2) if height != 0 else "Unknown"

        # Convert time to Python datetime object
        time_obj = (
            datetime.strptime(time_original, "%Y:%m:%d %H:%M:%S")
            if time_original
            else None
        )

        # Extract GPS coordinates
        latitude = metadata.get("EXIF:GPSLatitude")
        longitude = metadata.get("EXIF:GPSLongitude")

        # Convert GPS to decimal format if available
        def convert_gps(value, ref):
            if value is None:
                return None
            return round(value * (-1 if ref in ["S", "W"] else 1), 6)

        latitude = convert_gps(latitude, metadata.get("EXIF:GPSLatitudeRef"))
        longitude = convert_gps(longitude, metadata.get("EXIF:GPSLongitudeRef"))

        # Find nearest city (if GPS is available)
        state = "Unknown"
        country = "Unknown"
        if latitude and longitude:
            geolocator = Nominatim(user_agent="geo_locator")
            location = geolocator.reverse(str(latitude) + "," + str(longitude))
            state = (
                location.raw.get("address", {}).get("state", "Unknown")
                if location
                else "Unknown"
            )
            country = (
                location.raw.get("address", {}).get("country", "Unknown")
                if location
                else "Unknown"
            )

        return {
            "Date": time_obj.date() if time_obj else "Unknown",
            "Time": time_obj.time() if time_obj else "Unknown",
            "Camera": camera_model,
            "Lens": lens_model,
            "Flash": not flash_fired,
            "Width": width,
            "Height": height,
            "Resolution (x, y)": (width, height),
            "Aspect": aspect_ratio,
            "GPS": ((latitude, longitude) if latitude and longitude else "Unknown"),
            "State": state,
            "Country": country,
        }

    def runSorts(self):
        """
        Call all the arrange functions to populate outputDictionary
        """

        for imagePath in self.filePathList:
            print("Processing " + imagePath)
            # image = Image.open(imagePath)
            # exif_data = image.getexif()

            exif_data = self.get_exif_data(imagePath)

            self.arrangeTime(exif_data["Time"], imagePath)
            self.arrangeSeason(exif_data["Date"], imagePath)
            self.arrangeCamera(exif_data["Camera"], imagePath)
            # self.arrangeLens(exif_data["Lens"], imagePath)
            self.arrangeResolution(
                max(exif_data["Width"], exif_data["Height"]), imagePath
            )
            self.arrangeLocation(exif_data["State"], exif_data["Country"], imagePath)

    def arrangeTime(self, imgTime, imagePath):
        """
        Returns a "key"
        Options for key:
        "Morning": [0500 - 1200)
        "Afternoon": [1200 - 1700)
        "Evening": [1700 - 0000)
        "Late Night": [0000 - 0500)
        """

        if imgTime < time(5, 0, 0):
            # late night
            self.outputDictionary["Time"]["Late Night"].append(imagePath)
        elif imgTime < time(12, 0, 0):
            # morning
            self.outputDictionary["Time"]["Morning"].append(imagePath)
        elif imgTime < time(17, 0, 0):
            # afternoon
            self.outputDictionary["Time"]["Afternoon"].append(imagePath)
        else:
            # evening
            self.outputDictionary["Time"]["Evening"].append(imagePath)

    def arrangeSeason(self, imgDate, imagePath):
        """
        Returns a "key"
        Options for key:
        "Spring": [0301 - 0601)
        "Summer": [0601 - 0901)
        "Fall": [0901 - 1201)
        "Winter": [1201 - 0301)
        """

        if (
            datetime(2025, 3, 1).month <= imgDate.month
            and imgDate.month < datetime(2025, 6, 1).month
        ):
            # spring
            self.outputDictionary["Season"]["Spring"].append(imagePath)
        elif (
            datetime(2025, 6, 1).month <= imgDate.month
            and imgDate.month < datetime(2025, 9, 1).month
        ):
            # summer
            self.outputDictionary["Season"]["Summer"].append(imagePath)
        elif (
            datetime(2025, 9, 1).month <= imgDate.month
            and imgDate.month < datetime(2025, 12, 1).month
        ):
            # fall
            self.outputDictionary["Season"]["Fall"].append(imagePath)
        else:
            # winter
            self.outputDictionary["Season"]["Winter"].append(imagePath)

    def arrangeCamera(self, model, imagePath):
        if model in self.outputDictionary["Camera"]:
            self.outputDictionary["Camera"][model].append(imagePath)
        else:
            self.outputDictionary["Camera"][model] = []
            self.outputDictionary["Camera"][model].append(imagePath)

    def arrangeResolution(self, width, imagePath):
        if width > 8000:
            self.outputDictionary["Resolution"]["8K"].append(imagePath)
        elif width > 6000:
            self.outputDictionary["Resolution"]["6K"].append(imagePath)
        elif width > 4000:
            self.outputDictionary["Resolution"]["4K"].append(imagePath)
        else:
            self.outputDictionary["Resolution"]["sub-4K"].append(imagePath)

    def arrangeLocation(self, state, country, imagePath):
        if country == "United States":
            if state not in self.outputDictionary["State"]:
                self.outputDictionary["State"][state] = []
            self.outputDictionary["State"][state].append(imagePath)

        if country not in self.outputDictionary["Country"]:
            self.outputDictionary["Country"][country] = []

        self.outputDictionary["Country"][country].append(imagePath)

    # def arrangeLens(self, model, imagePath):
    #     if (model )
