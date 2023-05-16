import os, json
from dotenv import load_dotenv

import dataset_tools as dtools
import supervisely as sly


if sly.is_development():
    load_dotenv(os.path.expanduser("~/ninja.env"))
    load_dotenv("local.env")

api = sly.Api.from_env()
project_id = sly.env.project_id()
project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))


def main():
    stats = [
        dtools.ClassesPerImage(project_meta),
        dtools.ClassBalance(project_meta),
        dtools.ClassCooccurrence(project_meta),
        dtools.ObjectsDistribution(project_meta),
        dtools.ObjectSizes(project_meta),
        dtools.ClassSizes(project_meta),
    ]
    dtools.count_stats(
        project_id,
        stats=stats,
        sample_rate=0.01,
    )
    for stat in stats:
        with open(f"./stats/{stat.json_name}.json", "w") as f:
            json.dump(stat.to_json(), f)
        stat.to_image(f"./stats/{stat.json_name}.png")


if __name__ == "__main__":
    main()
