# -*- coding: utf-8 -*-
# pylint: disable=C0415
def test_import():
    import pandas
    import numpy
    import cv2
    import skimage
    import scipy
    import loguru
    import phone_gen
    import matplotlib
    import validators
    import tifffile
    import yaml

    assert True, "import failed"


#############################################################################
if __name__ == "__main__":
    test_import()
