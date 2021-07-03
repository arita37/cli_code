import argparse
from mygenerator.validate import image_padding_load, run_image_padding_validate


def run_cli():
    """
    Validate images output
    """
    p = argparse.ArgumentParser(description="Generate dataset of phone number images")
    add = p.add_argument
    add("--min_spacing", type=int, default=0, help="Min spacing between digits on the image")
    add("--max_spacing", type=int, default=14, help="Max spacing between digits on the image")
    add("--image_width", type=int, default=256, help="Width of generated images")
    add(
        "--input_path",
        type=str,
        default="./",
        help="Output dir: images and meta.csv ",
    )
    add(
        "--config_file",
        type=str,
        default="default",
        help="config.yaml file, by default in %USER%/.mygenerator/config.yaml or default",
    )

    a = p.parse_args()

    run_image_padding_validate(
        min_spacing=a.min_spacing,
        max_spacing=a.max_spacing,
        image_width=a.image_width,
        input_path=a.input_path,
        config_file=a.config_file,
    )


#############################################################################
if __name__ == "__main__":
    run_cli()
