from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "PASCAL VOC 2012"
PROJECT_NAME_FULL: str = "PASCAL visual object classes challenge 2012"

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(
    url="http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#rights"
)
APPLICATIONS: List[Union[Domain, Industry, Research]] = [Domain.General()]
CATEGORY: Category = Category.General(benchmark=True, featured=True)

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.ObjectDetection(),
    CVTask.SemanticSegmentation(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = "2012-06-25"  # "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 49551
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/pascal-voc-2012"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "Training/validation data": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar",
    "Development kit code and documentation": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCdevkit_18-May-2011.tar",
    "PDF documentation": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/devkit_doc.pdf",
    "HTML documentation": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html",
    "Guidelines used for annotating the database (VOC2011)": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/guidelines.html",
    "Action guidelines used for annotating the action task images": "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/action_guidelines/index.html",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

PAPER: Optional[str] = "http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham15.pdf"
CITATION_URL: Optional[str] = "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#citation"
AUTHORS: Optional[List[str]] = [
    "Mark Everingham",
    "Luc van Gool",
    "Chris Williams",
    "John Winn",
    "Andrew Zisserman",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = "UK joint research group"
ORGANIZATION_URL: Optional[
    Union[str, List[str]]
] = "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html#organizers"

SLYTAGSPLIT: Dict[str, List[str]] = None
TAGS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME, PROJECT_NAME_FULL]
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }
    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    return settings
