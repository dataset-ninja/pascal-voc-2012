import json
import os

import supervisely as sly
from dotenv import load_dotenv

import dataset_tools as dtools

if sly.is_development():
    load_dotenv(os.path.expanduser("~/ninja.env"))
    load_dotenv("local.env")

os.makedirs("./stats/", exist_ok=True)
os.makedirs("./visualizations/", exist_ok=True)
api = sly.Api.from_env()

# 1a initialize sly api way
project_id = sly.env.project_id()
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
datasets = api.dataset.get_list(project_id)


# 1b initialize sly localdir way
# project_path = os.environ["LOCAL_DATA_DIR"]
# sly.download(api, project_id, project_path, save_image_info=True, save_images=False)
# project_meta = sly.Project(project_path, sly.OpenMode.READ).meta
# datasets = None

# 2. upload dataset custom data
project_info = api.project.get_info_by_id(project_id)
if len(project_info.custom_data):
    info = {
        "name": "PASCAL VOC",
        "fullname": "PASCAL Visual Object Classes Challenge",
        "cv_tasks": ["semantic segmentation", "object detection", "instance segmentation"],
        "annotation_types": ["instance segmentation"],
        "release_year": "2012",
        "organization": "University of Oxford",
        "organization_link": "http://host.robots.ox.ac.uk/pascal/VOC/",
    }
    api.project.update_custom_data(project_id, info)

# 3. get download link

# download_link = dtools.prepare_download_link(project_info)
# dtools.update_links_dict({project_id: download_link})


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
    ]
    animators = [
        dtools.HorizontalGrid(project_id, project_meta),
        dtools.VerticalGrid(project_id, project_meta),
    ]
    dtools.prepare_renders(
        project_id,
        renderers=renderers + animators,
        sample_cnt=40,
    )
    print("Saving visualization results...")
    for r in renderers + animators:
        r.to_image(f"./visualizations/{r.basename_stem}.png")
    for a in animators:
        a.animate(f"./visualizations/{a.basename_stem}.webp")
    print("Visualizations done")


def build_summary():
    summary_data = dtools.get_summary_data_sly(project_info)
    summary_content = dtools.generate_summary_content(
        summary_data,
        gif_url="https://github.com/dataset-ninja/pascal-voc-2012/raw/main/visualizations/classes_preview.webm",
    )

    with open("SUMMARY.md", "w") as summary_file:
        summary_file.write(summary_content)


def main():
    pass
    # build_stats()
    # build_visualizations()
    build_summary()


# @TODO: dataset-ninja/pascal-voc-2012 github repo in custom data
# assk -object detection
# licence
# tags
# industies
# year
# authors
# ....
# ...
# default image preview id

# auto summary.md


if __name__ == "__main__":
    main()
