Dataset **PASCAL VOC 2012** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzIyM19QQVNDQUwgVk9DIDIwMTIvcGFzY2FsLXZvYy0yMDEyLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogInZZWWNDQ0p1d3hLMXhTeGhjU2VMUEZCRXk0MnVTRFVWMEJhT3NqVXlRTlE9In0=)

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
