import numpy as np
import pandas as pd

import mygenerator.dataset as dataset


def test_image_dataset_get_label_list():
    ds = dataset.ImageDataset(meta=pd.DataFrame({"label": ["a", "b", "a", "a"]}))

    indices = ds.get_label_list("a")

    np.testing.assert_array_equal(indices, np.asarray([0, 2, 3]))


def test_image_dataset_len():
    ds = dataset.ImageDataset(meta=pd.DataFrame({"label": ["a", "b", "a", "a"]}))

    l = len(ds)

    assert l == 4


def test_image_dataset_get_sampe():
    def _dummy_get_image_fn(idx):
        return "image from {} index".format(idx)

    ds = dataset.ImageDataset(
        meta=pd.DataFrame(
            {"label": ["a", "b", "a", "a"], "uri": ["0.png", "1.png", "2.png", "3.png"]}
        ),
        get_image_fn=_dummy_get_image_fn,
    )

    el = ds.get_sample(1)

    assert el[0] == "image from 1 index"
    assert el[1].to_dict() == {"label": "b", "uri": "1.png"}


def test_image_dataset_get_image_only():
    uris = ["1.png", "2.png", "3.png"]

    def _get_image_fn(idx):
        uri = uris[idx]
        return {
            "1.png": np.asarray([0, 1, 2]),
            "2.png": np.asarray([3, 4, 5]),
            "3.png": np.asarray([6, 4, 5]),
        }[uri]

    ds = dataset.ImageDataset(
        meta=pd.DataFrame({"uri": uris}),
        get_image_fn=_get_image_fn,
    )

    actual_img = ds.get_image_only(1)

    np.testing.assert_array_equal(actual_img, np.asarray([3, 4, 5]))


def test_nlp_dataset_len():
    ds = dataset.NlpDataset(pd.DataFrame({"label": [f"label_{idx}" for idx in range(4)]}))

    assert len(ds) == 4
