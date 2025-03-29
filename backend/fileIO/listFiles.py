import os

def get_image_files(folder_path):

  image_files = []
  for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.heic')):
      file_path = os.path.join(folder_path, filename)
      image_files.append(file_path)
  return image_files
