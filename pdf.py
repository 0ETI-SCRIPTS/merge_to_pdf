from PIL import Image
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
out_dir = os.path.join(current_dir, "pdf_out")


def ensure_output_dir_exists():
    if(os.path.isdir(out_dir)):
        return
    else:
        os.mkdir(out_dir)


def get_folders_in_current_dir():
    os.chdir(current_dir)
    filtered = list(filter(lambda item: os.path.isdir(item)
                    and item != "pdf_out", os.listdir()))
    return list(map(
        lambda dir: os.path.join(current_dir, dir),
        filtered
    ))


def create_pdf_from_folder(folder_path):
    out_name = os.path.split(folder_path)[1]
    save_path = os.path.join(out_dir, out_name + ".pdf")

    # Uncomment to overwrite
    if(os.path.exists(save_path)):
        print(f"PDF ALREADY EXISTS: {out_name}")
        return

    os.chdir(folder_path)

    filtered = list(filter(lambda file: file.endswith(".png")
                    or file.endswith(".jpg"), os.listdir()))
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

    print(f"PDF CREATED: {out_name}")

    images[0].save(
        save_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )


def main():
    ensure_output_dir_exists()
    dirs = get_folders_in_current_dir()

    for dir in dirs:
        create_pdf_from_folder(dir)


main()
