# Expert commentary

https://www.linkedin.com/in/maxim-kolomeychenko-phd-9075b4125/

Pascal VOC 2012 dataset is widely used as a benchmark for different computer vision tasks like semantic segmentation, instance segmentation and object detection. However, according to the [Leaderboards for the Evaluations on PASCAL VOC Data](http://host.robots.ox.ac.uk:8080/leaderboard/main_bootstrap.php) the most popular and traditional competition is on the task of semantic segmentation (authors name it as object segmentation task). In addition, the most common benchmark for object detection and instance segmentation is [COCO dataset](datasetninja.com/datasets/coco). 

Another interesting aspect of this dataset is the presence of a neutral class. The boundary (internal and external pixels nearby the object edge) of every segmentation mask is marked with the special neutral class. It is worth noting that the neutral mask is presented as a single mask for all objects on the image (i.e. authors of the dataset do not provide separate neutral masks for every object). 

<img src="https://github.com/dataset-ninja/pascal-voc-2012/assets/12828725/38251d98-ac07-4d90-9233-b84ca759b625" alt="example of the neutral object in the Pascal VOC" width="250px">

Traditionally, a neutral class is used during neural network training - all pixels marked with this class do not take into account in training loss calculation. It allows to manually label object boundaries with less precision. Nowadays, this approach is not so popular thanks to the development of interactive tools that significantly speed up manual labeling and provide high-quality pixel-level segmentations. 


