import os

import cv2
import numpy as np
import pytest

from mygenerator.utils import log, log2, loge
from mygenerator.validate import image_padding_load, image_padding_get


# @pytest.mark.parametrize('seq_width', (('1234', 90)))
def test_run_cli(tmp_path):
    # sequence, width = seq_width
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

    n_success_case = 3
    pars = [
        ### Successs
        ["45", 1, 1, 2 * 30 + 1, output_path, str(config_file)],  ### 2 digit, min padding
        ["123", 50, 50, 3 * 200 + 2 * 50, output_path, str(config_file)],  ### 3 digits, max size
        [
            "0123456789",
            1,
            1,
            10 * 5 + 9 * 1,
            output_path,
            str(config_file),
        ],  ## 10 digits, min size, min padding
        ### Failed
        ["123", 50, 50, 3 * 201 + 2 * 50, output_path, str(config_file)],  ### 50
        ["", 0, 16, 120, output_path, str(config_file)],
        ["1", 0, 16, 10, output_path, str(config_file)],
        ["1", 0, 16, 20, output_path, str(config_file)],
    ]

    cmdref = """generate-numbers-sequence --sequence {} \
        --min_spacing {} \
        --max_spacing {} \
        --image_width {} \
        --output_path {} \
        --config_file {}
    """.strip()

    for i, p in enumerate(pars):
        seq = p[0]
        min_pad = p[1]
        max_pad = p[2]
        width = p[3]
        cmd = cmdref.format(p[0], p[1], p[2], p[3], p[4], p[5])
        log(cmd)
        os.system(cmd)

        if i < n_success_case:
            img_path = output_path / f"img_{seq}_0.png"
            assert img_path.exists()
            assert img_path.is_file()

            img = cv2.imread(str(img_path))
            assert img.shape[1] == width

            assert np.mean(img) > 5, "image is mostly black"
            assert np.mean(img) < 250, "image is mostly white"

            char_list, pad_list = image_padding_get(img, threshold=0)
            log2("padding", pad_list)
            assert sum([t >= min_pad and t <= max_pad for t in pad_list]) == len(
                pad_list
            ), "Wrong padding range"
            # assert False

        #### TODO : Failed cases to handle better !
