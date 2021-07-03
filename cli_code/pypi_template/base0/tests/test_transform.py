import random

import numpy as np
import pandas as pd
import cv2

import mygenerator.dataset as dataset
import mygenerator.transform as transform
from mygenerator.utils import log, log2


###############################################################################################
def test_chars_to_images_transform():
    uris = ["a.png", "b.png", "c.png"]

    def _get_image_fn(idx):
        uri = uris[idx]
        return {
            "a.png": np.asarray([0, 1, 2]),  # letter a
            "b.png": np.asarray([3, 4, 5, 6]),  # letter b
            "c.png": np.asarray([7, 8]),  # letter c
        }[uri]

    font_ds = dataset.ImageDataset(
        meta=pd.DataFrame(
            {
                "label": ["a", "b", "c"],
                "uri": uris,
            }
        ),
        get_image_fn=_get_image_fn,
    )
    text_ds = dataset.NlpDataset(pd.DataFrame({"label": ["caba"]}))
    tr = transform.CharToImages(font=font_ds)

    ds = tr.fit_transform(text_ds)

    assert len(ds) == 1
    imgs, meta = ds.get_sample(0)
    assert meta.to_dict() == {
        "label": "caba",
    }
    assert len(imgs) == len("caba")
    np.testing.assert_array_equal(imgs[0], np.asarray([7, 8]))  # c
    np.testing.assert_array_equal(imgs[1], np.asarray([0, 1, 2]))  # a
    np.testing.assert_array_equal(imgs[2], np.asarray([3, 4, 5, 6]))  # b
    np.testing.assert_array_equal(imgs[3], np.asarray([0, 1, 2]))  # a


def test_combine_images_horizontally_transform():
    np.random.seed(42)

    def _get_image_fn(idx):
        m1 = np.zeros((28, 20), dtype=np.uint8)
        m1[:, 3:] = 10

        m2 = np.zeros((28, 20), dtype=np.uint8)
        m2[:, :] = 20

        return [m1, m2]

    ds = dataset.ImageDataset(
        meta=pd.DataFrame(
            {
                "label": ["dummy"],
            }
        ),
        get_image_fn=_get_image_fn,
    )

    ds = transform.CombineImagesHorizontally(
        padding_range=(1, 1),
        combined_width=20 + 20 + 1,
    ).fit_transform(ds)

    assert len(ds) == 1
    img, meta = ds.get_sample(0)

    me = np.zeros((28, 20 + 20 + 1), dtype=np.uint8)
    me[:, 3:20] = 10
    me[:, 21:] = 20
    me = 255 - me  ### Inversion

    np.testing.assert_array_equal(img, me)
    assert meta.to_dict() == {"label": "dummy"}


def test_scale_image_transform():
    def _get_image_fn(idx):
        img = [
            np.asarray(
                [  # a.png
                    [8],
                ]
            ).astype(np.uint8),
            np.asarray(
                [  # b.png
                    [1, 2],
                    [3, 4],
                ]
            ).astype(np.uint8),
        ][idx]
        return img

    ds = dataset.ImageDataset(
        meta=pd.DataFrame(
            {
                "label": ["a", "b"],
                "uri": ["a.png", "b.png"],
            }
        ),
        get_image_fn=_get_image_fn,
    )

    ds = transform.ScaleImage(
        width=3,
        inter=cv2.INTER_NEAREST,
    ).fit_transform(ds)

    assert len(ds) == 2
    np.testing.assert_array_equal(
        ds.get_image_only(0),
        np.asarray(
            [
                [8, 8, 8],
                [8, 8, 8],
                [8, 8, 8],
            ]
        ),
    )
    np.testing.assert_array_equal(
        ds.get_image_only(1),
        np.asarray(
            [
                [1, 2, 2],
                [2, 3, 3],
                [3, 4, 4],
            ]
        ),
    )


def create_font_files(font_dir):
    """
    Args:
        font_dir:  image directory
    Returns:

    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottom_left_corner_of_text = (0, 24)
    font_scale = 1.0
    font_color = (255, 255, 255)
    line_type = 2
    img_size = (24, 24, 3)

    for dig in range(10):
        dig = str(dig)
        dig_folder = font_dir / dig
        dig_folder.mkdir(parents=True)
        img = np.zeros(img_size, np.uint8)
        cv2.putText(img, dig, bottom_left_corner_of_text, font, font_scale, font_color, line_type)
        img_path = str(dig_folder / "{}.png".format(dig))
        cv2.imwrite(img_path, img)

    return img_size


def test_text_to_image_transform(tmp_path):
    text_0 = "012345678901"
    text_1 = "123456789012"
    image_width = 250

    np.random.seed(42)
    random.seed(42)
    font_dir = tmp_path / "font"
    digit_image_size = create_font_files(font_dir)
    digit_image_height = 28  # specs
    text_ds = dataset.NlpDataset(pd.DataFrame({"label": [text_0, text_1]}))

    ds = transform.TextToImage(
        font_dir=font_dir,
        spacing_range=(0, 10),
        image_width=image_width,
    ).fit_transform(text_ds)

    assert len(ds) == 2

    # check sample #0
    img, meta = ds.get_sample(0)
    assert img.shape[1] == image_width
    assert img.shape[0] <= digit_image_height
    assert np.mean(img) > 10  # image is not blank
    assert meta.to_dict() == {"label": text_0}

    # check sample #1
    img, meta = ds.get_sample(1)
    assert img.shape[1] == image_width
    assert img.shape[0] <= digit_image_height
    assert np.mean(img) > 10  # image is not blank
    assert meta.to_dict() == {"label": text_1}
