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


project_info = api.project.get_info_by_id(project_id)
custom_data = project_info.custom_data

# 2. get download link
download_sly_url = dtools.prepare_download_link(project_info)
dtools.update_sly_url_dict({project_id: download_sly_url})


# 3. upload custom data
if len(custom_data) > 0:
    # preset fields
    custom_data = {
        # required fields
        "name": "PASCAL VOC 2012",
        "fullname": "PASCAL Visual Object Classes Challenge",
        "cv_tasks": ["semantic segmentation", "object detection", "instance segmentation"],
        "annotation_types": ["instance segmentation"],
        "industries": ["general domain"],
        "release_year": 2012,
        "homepage_url": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html",
        "license": "custom",
        "license_url": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#rights",
        "preview_image_id": 49551,
        "github_url": "https://github.com/dataset-ninja/pascal-voc-2012",
        "citation_url": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#citation",
        "download_sly_url": download_sly_url,

        # optional fields
        "download_original_url": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#devkit",  
        "paper": "http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham15.pdf",
        # "organization_name": None, 
        # "organization_url": None,
        # "tags": [],
    }
    api.project.update_custom_data(project_id, custom_data)




def build_stats():
    stats = [
        dtools.ClassBalance(project_meta),
        dtools.ClassCooccurrence(project_meta, force=True),
        dtools.ClassesPerImage(project_meta, datasets),
        dtools.ObjectsDistribution(project_meta),
        dtools.ObjectSizes(project_meta),
        dtools.ClassSizes(project_meta),
    ]
    for stat in stats:
        if not sly.fs.file_exists(f"./stats/{stat.basename_stem}.json"):
            stat.force = True
    stats = [stat for stat in stats if stat.force]

    # heatmaps = dtools.ClassesHeatmaps(project_meta)
    # classes_previews = dtools.ClassesPreview(project_meta, project_info.name)
    # vstats = [heatmaps, classes_previews]

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
    # heatmaps.to_image(f"./stats/{heatmaps.basename_stem}.png", draw_style="outside_black")
    # classes_previews.animate(f"./visualizations/{classes_previews.basename_stem}.webm")

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
        a.animate(f"./visualizations/{a.basename_stem}.webm")
    print("Visualizations done")


def build_summary():
    print('Building summary...')
    summary_data = dtools.get_summary_data_sly(project_info)

    if sly.fs.file_exists("./visualizations/classes_preview.webm"):
        classes_preview=f"{custom_data['github_url']}/raw/main/visualizations/classes_preview.webm"

    summary_content = dtools.generate_summary_content(
        summary_data,
        vis_url=classes_preview,
    )

    with open("SUMMARY.md", "w") as summary_file:
        summary_file.write(summary_content)
    print('Done.')

def main():
    pass
    # build_stats()
    # build_visualizations()
    build_summary()


if __name__ == "__main__":
    main()
