# Senior Design 2021 - 2022
# OpenGuide-Assist: Guided Vision for the Visually Impaired
A wearable solution for visually impaired individuals to feel more confident navigating their environment. 

special thanks to BU Senior Design Team 2021-2022 (https://github.com/amg1998/BUSeniorDesign-Opticle-21-22)

### Table of Contents:
* [Project Overview](#projectoverview)
* [Engineering Addendum](#eng_add)
* [Documentation](#documentation)
* [Sources](#sources)

<a name="projectoverview"></a> 
## Project Overview

**Problem:** Visual impairment impacts millions of people all over the world, affecting their quality of life, independence and mobility. Current mobility aid solutions are limited in detecting off ground obstacles, do not provide semantic information, and are not always suitable for all age groups.

**Solution:** Our solution is to create a wearable technology that detects obstacles in indoor and outdoor environments with a depth-sensing AI camera. OpenGuide-Assist alerts users with haptic feedback and auditory output when obstacles are detected. The user will wear a chest mount with a camera and a linear resonant actuator mounted to it, as well as bone conducting headphones. Our hope is that our solution allows visually impaired individuals to feel more confident being independent when navigating unknown environments.

<a name="eng_add"></a> 
## Engineering Addendum

### Current Functionality of Device
Our device is currently made to detect obstacles that are directly in the user's path and identify where specific objects are based on the object the user tells the system to find. In order to give the user options, the device has two modes that can be toggled between using a switch on the device. In mode 1, the user can choose just to detect obstacles directly in their path and have the device provide them haptic feedback through the wrist mount when obstacles are detected. This mode is intended to identify immediate obstacles that are less than 1.7 meters in front of the user. In mode 2, the device will allow the user to instruct through the microphone in the headphones an object they would like to look for in addition to the features provided in mode 1. If said object is detected, the device will then provide, through audio feedback, the distance and relative clock position of the object from the user.
The device can be worn around the chest of the user and can be used portably as long as the device is connected to the internet. It can be used for up to 90 minutes as this is the maximum battery life of the wrist mount. Both the chest mount and wrist mount can also be adjusted to fit most sizes.

### Technical Background Summary

#### Immediate Obstacle Detection
In order to detect immediate obstacles in front of the user, the device uses point cloud based detection to determine if there is an obstacle in the user’s path. Point cloud data is generated by combining RGB and depth data. Using the OAK-D camera, a 3-D point cloud is generated where objects in the camera’s view appear as points with 3-D coordinates. A bounding box, 1 meter wide, 2 meters tall, and 1.7 meters deep, is used to represent the 3-D space that would be directly in front of the user so the device only checks for points in this box. If our device detects at least 5000 points inside this box, it determines that there is an obstacle in front of the user.

#### Object Identification
In order to identify particular objects and their positioning, a neural network is run in parallel on both the left and right stereo cameras to produce 3-D position data that can be read by the Pi 4. This allows the device to give 3-D results for detections when running a 2-D trained model by fusing neural networks with the stereo depth cameras. Our device currently runs the pre-trained YOLO model on the COCO dataset which has over 80 object labels. The YOLO model produces a confidence value for each detected object where the object with the highest confidence value in each frame is saved into a queue of 30 detections, which are all taken in the previous second. With the use of the depth camera cameras on the OAK-D, the device is able to pull the 3-D coordinates of detected objects allowing it to produce the approximate distance and clock position from the user. The distance of the median detection in the queue is used as the distance the device announces to the user when it has found the correct object and the distance of the object changes by a given threshold.

### Limitations of Project
* Audio
	* For audio input, we are currently converting speech to text using an API powered by Google's AI technology. If the user is on mode 2 (guidance to objects of interest) and would like to tell our system what obstacle they want to detect, they will need to say the object out loud into the microphone on the headphones so that the system can register this. With this comes limitations on what kinds of environments the device can function properly in mode 2. If the environment the user is in is too loud, it will be difficult for the user input to be recognized properly, if at all.
* Response time for Feedback
	* Given the number of different processes running on our project at once, sometimes it takes a longer time for the speech to text conversion to happen and for the haptic feedback to happen. It can take a few tries for the speech to text converter to finally register the correct user input.
* Diversity of test subjects/ Time Constraint
	* This project was completed over the course of seven months and we were able to test twice with a visually impaired male from The Carroll Center for the Blind located in Newton, Massachusetts. The first time we tested with the visually impaired individual was after completing our initial prototype that was not yet portable. After taking his feedback into consideration, we modified the goals of our project accordingly. One thing we wish we did was test with a more diverse pool of subjects so that we could get more feedback. However, due to the time constraint of our project deadlines, we were unable to do so.
* Durability
	* Our system is not the most durable under different weather conditions, such as rain or snow. Wires are exposed, as well as the Raspberry Pi. With more time, we would like to produce better encasing for the hardware components of the system.

### Future Scope
* Uber
    * A functionality that we hope our device could eventually integrate is the integration with the Uber App to assist visually impaired people in finding their Uber. When the user orders an Uber, our device would have access to the Uber API to pull ride information connected to the user's account. Information such as the car license plate, make, model, and color would be pulled from the API and set as the object the device should look for. Currently the device is not capable of identifying specific car make and models, however, would be able to once given the necessary model that has identified different make and models. Once the device finds a car that matches the Uber description, it would alert the user in a similar fashion to how it does now. This feature could help visually impaired  people more easily find an Uber without the assistance of another person as well as improve their safety so they do not get into the wrong car.
* Product Design
    * Our product is still in a prototype form and we would like to make the design more durable and better looking. We would hope to reduce the size of the wrist mount so it is not as bulky and looks closer to the size of a smart watch or fitness band. We also would want a more secure casing for our electrical components on the chest mount so everything is covered and looks more like one cohesive device instead of an assembly of different components attached to the chest mount.


### Extra Development Notes from Team Members
##### Blockers that were Resolved
* Camera calibration - Point Cloud
	* The first time we generated the point cloud, the axes within it were oriented at an angle compared to the axes within the depth map. This was problematic as movement in the real world was mapped incorrectly within the point cloud. We initially believed that recalibrating the OAK-D would solve this issue, however, it resulted in the OAK-D not being able to run code that was using a different version of the depthai library. Both issues were solved by updating the point cloud code to use the newest version of the depthai library.

* Dependencies
	* Sometimes, the incorrect versions of the dependencies needed to run certain code would cause a lot of issues. By making sure that each dependency was properly upgraded or downgraded to run with everything else, we were able to fix this.
* Various package installations when running on new device
	* When running our project on a new Raspberry Pi, we needed to make sure that the proper numpy packages were installed accordingly in order to run the code.

<a name="documentation"></a> 
## Documentation
Documentation for setup and installation is available at [DepthAI API Docs](https://docs.luxonis.com/projects/api/en/latest/install/).

<a name="sources"></a> 
## Sources
[Spatial Tiny Yolo Example of the Luxonis repository](https://github.com/luxonis/depthai-python/tree/main/examples/SpatialDetection) was used as an example on how to run a YOLO model on the OAK-D.<br/>
Source material on socket programming used in our project can be found [here](https://docs.python.org/3/howto/sockets.html). <br/>
Source for generating a point cloud from RGB and Depth data can be found [here](https://github.com/luxonis/depthai-experiments/tree/master/gen2-pointcloud/rgbd-pointcloud).
