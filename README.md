# Moving Blobs Generator

This repository contains the code for simple generator of artificial moving object samples for YOLO developed for Master Thesis: "Automatic analysis of images from camera-traps" by Michal Nazarczuk from Imperial College London

The code creates series of 3 images with moving objects along with bounding box descriptions in YOLO format.

## Prerequisites

The following libraries are required to be installed for the proper code evaluation:

1. Matplotlib
2. NumPy
3. OpenCV

The code was written and tested on Python 3.4.1

## Installation and usage

### Installation

Just copy the repository to your local folder:
```
git clone https://github.com/michaal94/Moving-Blobs-Generator
```

### Use of the algortihm

In order use the code just run it with your python distribution you installed libraries for (Anaconda, Virtualenv, etc.). In general type:

```
cd Moving-Blobs-Generator
python3 blobs.py
```
The example will run sample clustering with MNIST-train dataset.

## How does it work?

The program in the beginning takes the random pairs from your ```/blob_generation/backgrounds``` and ```/blob_generation/textures``` directories. Then, it crops a random blob from the texture and puts it in random place in the background. Further, based on this object (see class Blob) the shifted and rotated objects are generated and put into same background completing the series of 3 images. Finally, the rectangles for bounding boxes are generated and transleted to YOLO format.

## Options

Along the code you can play with the following:

1. plotting - set to ```True``` if you want to plot images while generating (not advisable for bigger data volumes)
2. rotation and translation parameters in Blob class (as for now the blob was intended to run out of background)
3. number of genarated blobs (for now it is from one to four, one occuring 66% of the time, rest 11% each)

In addition the program generates validation image with all generated samples for series with the bounding boxes marked in red.

## Sample
Below the sample output of the code is shown (for the provided sample images). Firstly, the generated images:

<img src="/blob_generation/generated_sample_0002_1.jpg" alt="Sample #1" width="640"/>
<img src="/blob_generation/generated_sample_0002_2.jpg" alt="Sample #2" width="640"/>
<img src="/blob_generation/generated_sample_0002_3.jpg" alt="Sample #3" width="640"/>

and the verification image:

<img src="/blob_generation/generated_sample_0002_verif.jpg" alt="Verification" width="640"/>

