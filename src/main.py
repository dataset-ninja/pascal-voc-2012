import json
import os

import supervisely as sly
from dotenv import load_dotenv

import dataset_tools as dtools

if sly.is_development():
    load_dotenv(os.path.expanduser("~/ninja.env"))
    load_dotenv("local.env")

os.makedirs("./stats/", exist_ok=True)
os.makedirs("./renders/", exist_ok=True)
api = sly.Api.from_env()

# 1. api way
project_id = sly.env.project_id()
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
datasets = api.dataset.get_list(project_id)

# 2. localdir way
# project_path = os.environ["LOCAL_DATA_DIR"]
# sly.download(api, project_id, project_path, save_image_info=True, save_images=False)
# project_meta = sly.Project(project_path, sly.OpenMode.READ).meta
# datasets = None


def build_stats():
    stats = [
        dtools.ClassBalance(project_meta),
        dtools.ClassCooccurrence(project_meta),
        dtools.ClassesPerImage(project_meta, datasets),
        dtools.ObjectsDistribution(project_meta),
        dtools.ObjectSizes(project_meta),
        dtools.ClassSizes(project_meta),
    ]
    vstats = [dtools.ClassesHeatmaps(project_meta)]
    dtools.count_stats(
        project_id,
        stats=stats,
        sample_rate=1,
    )

    print("Saving stats...")
    for stat in stats:
        with open(f"./stats/{stat.basename_stem}.json", "w") as f:
            json.dump(stat.to_json(), f)
        stat.to_image(f"./stats/{stat.basename_stem}.png")
    for vis in vstats:
        vis.to_image(f"./stats/{vis.basename_stem}.png", draw_style="outside_black")

    print("Stats done")


def build_visualizations():
    renderers = [
        dtools.Poster(project_id, project_meta),
        dtools.SideAnnotationsGrid(project_id, project_meta),
        dtools.HorizontalGrid(project_id, project_meta, cols=4),
    ]
    dtools.prepare_renders(
        project_id,
        renderers=renderers,
        sample_cnt=40,
    )
    print("Saving render results...")
    for renderer in renderers:
        renderer.to_image(f"./renders/{renderer.render_name}.png")
    print("Visualizations done")


def main():
    pass
    # build_stats()
    # build_visualizations()


# @TODO: dataset-ninja/pascal-voc-2012 github repo in custom data
# assk -object detection
# licence
# tags
# industies
# ...


if __name__ == "__main__":
    main()
