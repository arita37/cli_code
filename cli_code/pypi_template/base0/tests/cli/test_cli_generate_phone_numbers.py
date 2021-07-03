import os
import re
import shutil

import cv2
import numpy as np
import pandas as pd

from mygenerator.utils import log
from mygenerator.validate import image_padding_load


# @pytest.mark.parametrize("size", (1, 5))
def test_run_cli(tmp_path):
    """
      TODO: Use fixtures for hanling all cases
    Args:
        tmp_path:

    Returns:

    """
    output_path = tmp_path / "output"
    output_path.mkdir()

    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
current_dataset: mnist
datasets:
  mnist:
    url: "https://github.com/arita37/mnist_png/raw/master/mnist_png.tar.gz"
    """.strip()
    )
    log("config file:", str(config_file))

    n_success_case = 4
    n = 11
    n2 = n - 1
    pars = [
        #### Successs
        [1, 1, 1, n * 5 + n2 * 1, output_path, str(config_file)],  # 1 phone, min padding
        [1, 50, 50, n * 200 + n2 * 50, output_path, str(config_file)],  # max padding,
        [1, 1, 1, n * 5 + n2 * 50, output_path, str(config_file)],
        [
            4,
            3,
            20,
            n * 200 + n2 * 20,
            output_path,
            str(config_file),
        ],  ## 4 phone, variable padding, max size
        #### Failed
        [0, 0, 16, 11 * 5, output_path, str(config_file)],
        [1, 1, 16, 11 * 5, output_path, str(config_file)],
        [0, 0, 16, 11 * 201, output_path, str(config_file)],
        [1, 0, 16, 10, output_path, str(config_file)],
        [2, 0, 16, 20, output_path, str(config_file)],
    ]

    cmdref = """generate-phone-numbers  --num_images {} \
        --min_spacing {} \
        --max_spacing {} \
        --image_width {} \
        --output_path {} \
        --config_file {}
    """.strip()

    for i, p in enumerate(pars):
        n_image = p[0]
        min_pad = p[1]
        max_pad = p[2]
        width = p[3]
        cmd = cmdref.format(p[0], p[1], p[2], p[3], p[4], p[5])
        log(cmd)

        try:
            shutil.rmtree(output_path)
        except Exception as e:
            pass
        os.makedirs(output_path, exist_ok=True)
        os.system(cmd)

        if i < n_success_case:
            # Check meta.csv
            meta_file = output_path / "meta.csv"
            assert meta_file.exists()
            assert meta_file.is_file()

            df = pd.read_csv(meta_file, dtype={"label": str})
            assert len(df) == n_image

            # Check image files are exported
            label_pattern = re.compile("\\+\\d+$")  # label example: +81931939482
            for idx, row in df.iterrows():
                label = row["label"]
                assert label_pattern.match(label) is not None
                img_path = output_path / f"img_{idx}.png"
                assert img_path.exists()
                assert img_path.is_file()

                img = cv2.imread(str(img_path))
                assert img.shape[1] == width
                assert np.mean(img) > 4, "image is black"
                assert np.mean(img) < 250, "image is white"

                #### Calculate padding manually
                char_list, pad_list = image_padding_load(img_path, threshold=0)

                assert sum([t >= min_pad and t <= max_pad for t in pad_list]) == len(
                    pad_list
                ), f"Wrong padding range, {img_path}, {label}, {min_pad} -{max_pad},  {cmd}"

        #### TODO : Failed cases to handle better !
