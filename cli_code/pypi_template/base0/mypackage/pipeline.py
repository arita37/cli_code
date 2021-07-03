import pathlib

import pandas as pd

import mygenerator.dataset as dataset
import mygenerator.transform as transform
from mygenerator.utils import config_load, dataset_get_path


##############################################################
def run_generate_numbers_sequence(
    sequence: str,
    min_spacing: int = 1,
    max_spacing: int = 10,
    image_width: int = 280,  ### image_width
    output_path: str = "./",
    config_file: str = "config/config.yaml",
):
    #### Boundaries  #######################################################
    n = len(sequence)
    min_size = 5  ### min size image individual
    max_size = 200  ### max size image invidiual
    assert min_spacing >= 1 and min_spacing <= 50, "min_spacing"
    assert max_spacing >= min_spacing and max_spacing <= 50, "max_spacing"
    assert image_width >= max_spacing * (
        n - 1
    ) + n * min_size and image_width <= n * max_size + max_spacing * (n - 1), "image_width"
    assert n >= 1 and n <= 100, "sequence"
    assert image_width / len(sequence) > 2.0, "image_width"

    config = config_load(config_file)

    #### Load and get image dataset path  ################################
    img_dir = pathlib.Path(dataset_get_path(config))

    #### Text dataset
    ds_text = dataset.NlpDataset(pd.DataFrame({"label": [sequence]}))

    #### Transform into Image dataset
    tf = transform.TextToImage(
        font_dir=img_dir,
        spacing_range=(min_spacing, max_spacing),
        image_width=image_width,
    )

    ds_img = tf.fit_transform(ds_text)

    #### Only export 1st element
    ds_img.save(output_path, prefix=f"img_{sequence}", suffix="png", nrows=1)


def run_generate_phone_numbers(
    num_images: int = 10,
    min_spacing: int = 1,
    max_spacing: int = 10,
    image_width: int = 280,
    output_path: str = "./",
    config_file: str = "config/config.yaml",
):
    #### Boundaries  #######################################################
    nmin = 8  ### min digits in phone number
    nmax = 15  ### max digitis in phone number  0081
    min_size = 5
    max_size = 200
    assert min_spacing >= 1 and min_spacing <= 50, "min_spacing"
    assert max_spacing >= min_spacing and max_spacing <= 50, "max_spacing"
    assert (
        image_width >= nmin * min_size + (nmin - 1) * max_spacing
        and image_width <= nmax * max_size + (nmax - 1) * max_spacing
    ), "image_width"
    assert num_images > 0, "num_images"

    #######################################################################
    config = config_load(config_file)
    img_dir = pathlib.Path(dataset_get_path(config))

    ds_text = dataset.PhoneNlpDataset(size=num_images)

    tf = transform.TextToImage(
        font_dir=img_dir,
        spacing_range=(min_spacing, max_spacing),
        image_width=image_width,
    )
    ds_img = tf.fit_transform(ds_text)

    #### Serialize ######################################################
    ds_img.save(output_path, prefix="img", suffix="png", nrows=-1)
