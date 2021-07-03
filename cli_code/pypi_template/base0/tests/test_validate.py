import numpy as np
import cv2

from mygenerator.utils import log2, log
from mygenerator.validate import image_padding_get


def test_image_padding_get():

    img = np.zeros((5, 30, 3), dtype=np.uint8)

    img[:, 0:3, :] = 10
    img[1, 10, :] = 10
    img[:, 12:15, :] = 10

    img[1, 17, :] = 10
    img[:, 22:23, :] = 10

    ### Inverser
    img = 255 - img
    charlist, padlist = image_padding_get(img, threshold=0, inverse=True)

    np.testing.assert_array_equal(charlist, [3, 5, 1, 1])
    np.testing.assert_array_equal(padlist, [7, 2, 4, 7])
