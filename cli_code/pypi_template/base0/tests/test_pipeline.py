import random

import numpy as np
import pandas as pd
import cv2

from mygenerator import pipeline


def test_generate_phone_numbers(tmp_path):
    config_file = "default"

    np.random.seed(42)
    random.seed(42)
    output_path = tmp_path
    num_images = 5
    img_width = 5 * 50 + 10 * 4

    pipeline.run_generate_phone_numbers(
        num_images=num_images,
        min_spacing=1,
        max_spacing=10,
        image_width=img_width,
        output_path=str(output_path),
        config_file=config_file,
    )

    # Check meta.csv
    meta_file = output_path / "meta.csv"
    assert meta_file.exists()
    assert meta_file.is_file()

    df = pd.read_csv(meta_file)
    assert len(df) == num_images

    # Check image files are exported
    img_files = [str(f) for f in output_path.glob("*.png")]
    assert len(img_files) == num_images
    for img_file in img_files:
        img = cv2.imread(img_file)
        assert img.shape[1] == img_width
