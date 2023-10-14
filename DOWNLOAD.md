Dataset **PASCAL VOC 2012** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/m/j/kM/4goa4bfl6Po3DVte1f28pgguTaG9pCizUN7r4SrNqEj4TgmUW5JIuzwR4a2IwPKL8VR6pbJJZZHEWyzUQ1DIz0xf80W5f5ZM2uU6ZxEmZSZIiS64V2WEkqiviqfZ.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='PASCAL VOC 2012', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [Training/validation data](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar)
- [Development kit code and documentation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCdevkit_18-May-2011.tar)
- [PDF documentation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/devkit_doc.pdf)
- [HTML documentation](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/index.html)
- [Guidelines used for annotating the database (VOC2011)](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/guidelines.html)
- [Action guidelines used for annotating the action task images](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/action_guidelines/index.html)
