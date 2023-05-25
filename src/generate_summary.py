import json
import os

from dotenv import load_dotenv
import operator


import supervisely as sly
import pandas as pd

import inflect

if sly.is_development():
    load_dotenv(os.path.expanduser("~/ninja.env"))
    load_dotenv("local.env")

api = sly.Api.from_env()
p = inflect.engine()

def get_expert_commentary():
    content = "This is a very good dataset. I enjoy it every day in my life.\n\n"
    
    content += """
![Cooking at 3am](https://raw.githubusercontent.com/dataset-ninja/pascal-voc-2012/main/gordon-ramsay.jpg?v=1)

Some features of this dataset are:

1. high quality images and annotations (~4.6 bounding boxes per image)
1. real-life images unlike any current such dataset
1. majority of non-iconic images (allowing easy deployment to real-world environments)
    """
    
    return content

def generate_meta_from_sly(name:str, fullname:str, cv_tasks:list, release_year:str, organization:str, organization_link:str, industry:str=None):

    project_id = sly.env.project_id()
    # project_meta = sly.ProjectMeta.from_json(api.project.get_meta(project_id))
    # datasets = api.dataset.get_list(project_id)

    project_info = api.project.get_info_by_id(project_id)

    stats = api.project.get_stats(project_id)

    notsorted = [[cls['objectClass']['name'], cls['total']] for cls in stats['images']['objectClasses']]
    totals_dct = {
       "total_assets": stats['images']['total']['imagesInDataset'],
       "total_objects": stats['objects']['total']['objectsInDataset'],
       "total_classes": len(stats['images']['objectClasses']),
       "top_classes": list(map(operator.itemgetter(0), sorted(notsorted, key=operator.itemgetter(1), reverse=True)))
    }

    unlabeled_num = stats['images']['total']['imagesNotMarked']
    unlabeled_percent = round(unlabeled_num / totals_dct['total_assets'] * 100) 

    splits_list = [{'name': item['name'], 'split_size': item['imagesCount']} for item in stats['datasets']['items']]


    fields = {
        "name": name,
        "fullname": fullname,
        "cv_tasks": cv_tasks,
        "modality": project_info.type,
        "release_year": release_year,
        "organization": organization,
        "organization_link": organization_link,
        "totals": totals_dct,
        "unlabeled_assets_num": unlabeled_num,
        "unlabeled_assets_percent": unlabeled_percent,
        "splits": splits_list
    }

    if industry is not None:
        fields['industry'] = industry

    return fields

def generate_summary(data):
    name = data.get("name")
    fullname = data.get("fullname")
    industry = data.get("industry")
    modality = data.get("modality")
    totals = data.get("totals", {})
    top_classes = totals.get("top_classes", [])

    cv_tasks = data.get("cv_tasks", [])
    annotations = []
    for cv_task in cv_tasks:
        if cv_task == "semantic-segmentation":
            annotations.append("pixel-level segmentation annotations")
        if cv_task == "object-detection":
            annotations.append("boundary boxes")
    annotations = " annotations,".join(annotations)
    cv_tasks = ",".join(cv_tasks)

    unlabeled_assets_num = data.get("unlabeled_assets_num")
    unlabeled_assets_percent = data.get("unlabeled_assets_percent")
    release_year = data.get("release_year")
    organization = data.get("organization")
    organization_link = data.get("organization_link")

    splits = data.get("splits", [])
    splits_ = ", ".join([f'*{split["name"]}* ({split["split_size"]} {modality})' for split in splits])


    content = f"# {name} dataset summary\n\n"
    content += f"**{name}** ({fullname}) is a dataset for {cv_tasks} tasks. "

    content += (
        f"It is used in {industry} industry(ies). "
        if industry is not None
        else "It is used for general-purpose tasks. "
    )
    content += f"Dataset contains a total of {totals.get('total_assets', 0)} {modality} with {totals.get('total_objects', 0)} \
        labeled objects of {totals.get('total_classes', 0)} classes including top-3: *{', '.join(top_classes[:3])}*; \
            and other: *{', '.join(top_classes[3:])}*.\n\n"
    content += f"Each {p.singular_noun(modality)} in {name} dataset has {annotations}. "
    content += f"There are {unlabeled_assets_num} ({unlabeled_assets_percent}% of the total) unlabeled {modality} (i.e. without annotations).\n"
    content += f"There are {len(splits)} splits in the dataset: {splits_}. "
    content += (
        f"The dataset was released in {release_year} by [{organization}]({organization_link}).\n"
    )
    content += f"\n# Expert Commentary \n\n {get_expert_commentary()}"


    return content


if __name__ == "__main__":

    kwargs = {
        'name': "PASCAL VOC",
        "fullname": "PASCAL Visual Object Classes Challenge",
        "cv_tasks": ["semantic-segmentation"],
        "release_year": "2012",
        "organization": "Dong et al",
        "organization_link": "https://arxiv.org/pdf/2012.07131v2.pdf",
    }
    with open("src/metadata.json", "w") as json_file:
        json.dump(generate_meta_from_sly(**kwargs), json_file, indent=4)
    
    with open("src/metadata.json") as json_file:
        data = json.load(json_file)

    summary_content = generate_summary(data)

    with open("SUMMARY.md", "w") as summary_file:
        summary_file.write(summary_content)


# def generate_meta_from_local():

#     modality ="images"

#     with open("./stats/class_balance.json") as f:
#         json_data = json.load(f)
#     df = pd.DataFrame(data=json_data["data"], columns=json_data["columns"])

#     with open("./stats/classes_per_image.json") as f:
#         json_data = json.load(f)
#     df_img = pd.DataFrame(data=json_data["data"], columns=json_data["columns"])


#     totals_dct = {
#        "total_modality_files": df_img.shape[0],
#        "total_objects": df["Objects"].sum(),
#        "total_classes": df["Class"].count(),
#        "top_classes": df.sort_values('Objects', ascending=False)['Class'].tolist()
#     }

#     unlabeled_num = df_img.shape[0] - sum(df_img.drop(columns=["Image","Split", "Height", "Width", "Unlabeled"]).sum(axis=1)==0)
#     unlabeled_percent = unlabeled_num / df_img.shape[0]
#     splits_list = [
#         {
#         "name": "training",
#         "split_size": 800
#         },
#         {
#         "name": "validation",
#         "split_size": 200
#         }
#     ]

#     return {
#         "name": "PASCAL VOC",
#         "fullname": "PASCAL Visual Object Classes Challenge",
#         "cv_tasks": ["semantic-segmentation"],
#         "modality": modality,
#         "release_year": "2012",
#         "organization": "Dong et al",
#         "organization_link": "https://arxiv.org/pdf/2012.07131v2.pdf",
#         "totals": totals_dct,
#         "unlabeled_assets_num": unlabeled_num,
#         "unlabeled_assets_percent": unlabeled_percent,
#         "splits": splits_list
#     }

