import json

import inflect


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
            annotations.append("pixel-level")
        if cv_task == "object-detection":
            annotations.append("boundary boxes")
    annotations = " annotations,".join(annotations)
    cv_tasks = ",".join(cv_tasks)

    unlabeled_images = data.get("unlabeled_images")
    unlabeled_images_percent = data.get("unlabeled_images_percent")
    release_year = data.get("release_year")
    organization = data.get("organization")
    organization_link = data.get("organization_link")

    splits = data.get("splits", [])
    splits_ = ", ".join([f'{split["name"]} ({split["split_size"]} {modality})' for split in splits])

    # content
    p = inflect.engine()

    content = f"# {name} dataset summary\n\n"
    content += f"**{name}** ({fullname}) is a dataset for {cv_tasks}. "

    content += (
        f"It is used in {industry} industry(ies). "
        if industry is not None
        else "It is used for general-purpose tasks. "
    )
    content += f"Dataset contains a total of {totals.get('total_files', 0)} {modality} with {totals.get('total_objects', 0)} \
        labeled objects of {totals.get('total_classes', 0)} classes including top-3: *{', '.join(top_classes[:3])}*; \
            and other: *{', '.join(top_classes[3:])}*.\n\n"
    content += f"Each {p.singular_noun(modality)} in {name} dataset has {annotations}. "
    content += f"There are {unlabeled_images} ({unlabeled_images_percent}% of the total) unlabeled {modality} in the dataset (i.e. without annotations).\n"
    content += f"There are {len(splits)} splits in the dataset: {splits_}. "
    content += (
        f"The dataset was released in {release_year} by [{organization}]({organization_link}).\n"
    )

    return content


if __name__ == "__main__":
    with open("meta-pascal-voc.json") as json_file:
        data = json.load(json_file)

    summary_content = generate_summary(data)

    with open("SUMMARY_.md", "w") as summary_file:
        summary_file.write(summary_content)
