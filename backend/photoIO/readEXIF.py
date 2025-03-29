from PIL import Image
from pillow_heif import register_heif_opener
import backend.fileIO.listFiles

register_heif_opener()

class EXIF:
    def __init__(self, folderPath):
        self.filePathList = backend.fileIO.listFiles(folderPath)
        self.outputDictionary = {}
        
    def runSorts(self):
        """
        Call all the arrange functions to populate outputDictionary
        """
        
        for imagePath in self.filePathList:
            image = Image.open(imagePath)
            exif_data = img._getexif()
            
            arrangeTime(exif_data)
    
    def arrangeTime(self, exif_data):
        """
        Returns a "key"
        Options for key:
        "Morning": [0500 - 1200)
        "Afternoon": [1200 - 1700)
        "Night": [1700 - 0000)
        "Late Night": [0000 - 0500)
        """
        
        try: 
            print(exif_data)
        except: 
            pass
        
        