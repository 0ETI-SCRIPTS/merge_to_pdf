import os
import numpy
from typing import List, Tuple
from PIL.Image import Image as ImageType
from PIL import Image

CURRENT_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(CURRENT_DIR, "_pdf")


def ensure_out_dir_exists(OUT_DIR: str):
    if not os.path.exists(OUT_DIR) and not os.path.isdir(OUT_DIR):
        os.mkdir(OUT_DIR)


def filter_files(files: List[str]) -> List[str]:
    return list(filter(
        lambda file: file.endswith(".png") or file.endswith(".jpg"),
        files
    ))


def sort_files(files: List[str]) -> List[str]:
    return list(sorted(
        files,
        key=lambda file: int(file.split(".")[0])
    ))


def map_files_to_paths(files: List[str]) -> List[str]:
    return list(map(
        lambda file: os.path.join(CURRENT_DIR, file),
        files
    ))


def map_paths_to_images(paths: List[str]) -> List[ImageType]:
    return list(map(
        lambda path: Image.open(path),
        paths
    ))


def get_min_shape(images: List[ImageType]):
    min_shape = sorted([(numpy.sum(i.size), i.size) for i in images])[0][1]
    return min_shape


def resize_images(images: List[ImageType], min_shape: Tuple[int, int]) -> List[ImageType]:
    resized_images = [numpy.asarray(i.resize(min_shape)) for i in images]
    return resized_images


def horz_combine_images(images: List[ImageType]) -> ImageType:
    min_shape = get_min_shape(images)
    resized_images = resize_images(images, min_shape)
    horz_image_arr = numpy.hstack(resized_images)
    horz_image = Image.fromarray(horz_image_arr)
    return horz_image


def save_image(image: ImageType, image_name: str) -> None:
    image.save(os.path.join(OUT_DIR, image_name))


ensure_out_dir_exists(OUT_DIR)
image_dirs = os.listdir(CURRENT_DIR)

images = map_paths_to_images(
    map_files_to_paths(
        sort_files(
            filter_files(image_dirs)
        )
    )
)

save_image(horz_combine_images([images[0]]), "0.jpg")
for i in range(1, len(images), 2):
    save_image(
        horz_combine_images(images[i:i+2]),
        f"{i}.jpg"
    )
