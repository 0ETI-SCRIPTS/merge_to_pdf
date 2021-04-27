from PIL import Image
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
out_dir = os.path.join(current_dir, "pdf_out")

def get_folders_in_current_dir():
  os.chdir(current_dir)
  filtered = list(filter(lambda item: os.path.isdir(item) and item != "pdf_out", os.listdir()))
  return list(map(
    lambda dir: os.path.join(current_dir, dir),
    filtered
  ))

def create_pdf_from_folder(folder_path):
  out_name = os.path.split(folder_path)[1]
  os.chdir(folder_path)

  filtered = list(filter(lambda file: file.endswith(".png") or file.endswith(".jpg"), os.listdir()))
  filtered.sort(key=lambda item: int(item.split(".")[0]))

  images = list(map(
    lambda image_path: Image.open(
      os.path.join(
        folder_path, 
        image_path
      )
    ),
    filtered
  ))

  save_path = os.path.join(out_dir, out_name + ".pdf")

  print(images)

  images[0].save(
    save_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
  )

def main():
  dirs = get_folders_in_current_dir()

  for dir in dirs:
    print(dir)
    create_pdf_from_folder(dir)

main()