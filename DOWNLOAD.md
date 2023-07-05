Dataset **PASCAL VOC 2012** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/u/b/Jr/HptPk5MskgkmFnoIWTSYoJqiAXuLClnUIT1Ae5Dy03cpVfQQHXXspNvYucpKFDxXIfXSPzd3T40yDbcGnMkeuC15wSLqzKBVSsf8LfVugx6aVhlkQAurOVVmLof5.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='PASCAL VOC 2012', dst_path='~/dtools/datasets/PASCAL VOC 2012.tar')
```
The data in original format can be downloaded here:

- 🔗[Training/validation data](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar)
- 🔗[Development kit code and documentation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCdevkit_18-May-2011.tar)
- 🔗[PDF documentation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/devkit_doc.pdf)
- 🔗[HTML documentation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)
- 🔗[Guidelines used for annotating the database (VOC2011)](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/guidelines.html)
- 🔗[Action guidelines used for annotating the action task images](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/action_guidelines/index.html)
