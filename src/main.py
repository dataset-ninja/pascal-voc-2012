import json
import os

import supervisely as sly
from dotenv import load_dotenv

import dataset_tools as dtools

if sly.is_development():
    load_dotenv(os.path.expanduser("~/ninja.env"))
    load_dotenv("local.env")

os.makedirs("./stats/", exist_ok=True)
api = sly.Api.from_env()

# 1. api way
project_id = sly.env.project_id()
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))

# 2. localdir way
# project_path = os.environ["LOCAL_DATA_DIR"]
# sly.download(api, project_id, project_path, save_image_info=True, save_images=False)
# project_meta = sly.Project(project_path, sly.OpenMode.READ).meta


def main():
    stats = [
        dtools.ClassBalance(project_meta),
        dtools.ClassesPerImage(project_meta),
        dtools.ClassCooccurrence(project_meta),
        dtools.ObjectsDistribution(project_meta),
        dtools.ObjectSizes(project_meta),
        dtools.ClassSizes(project_meta),
    ]
    dtools.count_stats(
        project_id,
        stats=stats,
        sample_rate=1,
    )
    print("Saving stats...")
    for stat in stats:
        with open(f"./stats/{stat.json_name}.json", "w") as f:
            json.dump(stat.to_json(), f)
        stat.to_image(f"./stats/{stat.json_name}.png")


# @TODO: dataset-ninja/pascal-voc-2012 github repo in custom data
# assk -object detection
# licence
# tags
# industies
# ...


if __name__ == "__main__":
    main()
