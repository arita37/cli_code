import numpy as np
import cv2

import mygenerator.util_image as util_image
from mygenerator.utils import log2, log


def create_blank_image(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""

    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))

    # Fill image with color
    image[:] = color

    return image


def test_image_merge():
    imgs = [
        np.asarray(
            [
                [8],
            ]
        ),
        np.asarray(
            [
                [1, 2],
                [3, 4],
            ]
        ),
        np.asarray(
            [
                [1, 0, 0, 2],
                [0, 3, 4, 0],
                [5, 6, 0, 0],
            ]
        ),
    ]

    img, padding_size = util_image.image_merge(
        imgs, n_dim=2, padding_size=(1, 2), max_height=4, total_width=10
    )

    np.testing.assert_array_equal(
        img,
        np.asarray(
            [
                [8, 0, 1, 2, 0, 0, 1, 0, 0, 2],
                [0, 0, 3, 4, 0, 0, 0, 3, 4, 0],
                [0, 0, 0, 0, 0, 0, 5, 6, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        ),
    )
    assert padding_size == (1, 2)


def test_image_remove_extra_padding():
    IMAGE_HEIGHT, IMAGE_WIDTH = 300, 300
    COLOR = (0, 0, 0)
    blank_image = create_blank_image(IMAGE_HEIGHT, IMAGE_WIDTH, rgb_color=COLOR)

    RECTANGLE_HEIGHT, RECTANGLE_WIDTH = 100, 100
    RECTANGLE_COLOR = (0, 255, 0)
    cv2.rectangle(blank_image, (0, 0), (RECTANGLE_HEIGHT, RECTANGLE_WIDTH), RECTANGLE_COLOR, 1)

    no_space_image = util_image.image_remove_extra_padding(blank_image)

    log2("shape", no_space_image.shape)

    assert no_space_image.shape[0] == RECTANGLE_HEIGHT + 1
    assert no_space_image.shape[1] == RECTANGLE_WIDTH + 1


def test_image_resize():
    img = np.asarray(
        [
            [1, 2],
            [3, 4],
        ]
    ).astype(np.uint8)

    img = util_image.image_resize(
        img,
        width=4,
        inter=cv2.INTER_NEAREST,
    )

    np.testing.assert_array_equal(
        img,
        np.asarray(
            [
                [1, 1, 2, 2],
                [1, 1, 2, 2],
                [3, 3, 4, 4],
                [3, 3, 4, 4],
            ]
        ),
    )


def test_image_read(tmp_path):
    expected_img = create_blank_image(5, 10)
    img_path = str(tmp_path / "img.png")
    cv2.imwrite(img_path, expected_img)

    actual_img = util_image.image_read(img_path)

    np.testing.assert_array_equal(actual_img, expected_img)
