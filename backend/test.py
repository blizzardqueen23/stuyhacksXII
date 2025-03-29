from readEXIF import EXIF

reader = EXIF("TestImages")

reader.runSorts()

print(reader.get_exif_data("TestImages/5M8A4546_DxO-2.jpg"))

# reader.printEXIF("TestImages/00016225_DxO.jpg")
