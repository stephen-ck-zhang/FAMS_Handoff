# FAMS_Handoff

---

This is the project for NYU Tandon School of Engineering, Flexible AI-enabled Mechatronic Systems Lab - VIP. All rights reserved.


**Task Description**
----
A voice-controlled robotic arm is implemented with the speech recognition and computer vision modules to listen for voice commands and to look for the target object to catch & carry & hand off to target position/person. The code here is only the implementation for the handoff part. For other works, please look at the [FAMS Lab](https://github.com/famsvip/JetsonNanoFall2022).


**Installation**
----
1. Clone the repository
2. Install the dependencies
3. Run the code

*Run the `./yoloDetection.ipynb` first to set up all the dependencies and the environment. This file also helps you to test the referencing on sample image. Make sure you put the `./example.jpeg` into the cloned repository for referencing.* 


**Usage**
----
The main file is located at `./move_and_handoff.py`. For the usage, put the files `./move_and_handoff.py` and `./search.py` into the cloned repository and just run the file with the following command in the directory:

```
python3 move_and_handoff.py
```


**Reference**
----
The implementation of the YOLOv5 is based on the [ultralytics/yolov5](https://github.com/ultralytics/yolov5) repository. The code is modified to fit the needs of this project. The following is the citation for the YOLOv5:

```
@misc{glennjocher2020yolov5,
    title   = {YOLOv5},
    author  = {Glenn Jocher},
    year    = {2020},
    eprint  = {1910.04612},
    archivePrefix = {arXiv},
    primaryClass = {cs.CV}
}
```


**Contributors**
----
People contributed to this, Stephen Zhang (stephen.zhang@nyu.edu) & XinYan Chen (xinyan.chen@nyu.edu).
