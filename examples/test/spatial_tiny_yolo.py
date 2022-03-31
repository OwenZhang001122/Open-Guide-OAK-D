# #!/usr/bin/env python3
# #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

# from pathlib import Path
# import sys
# import cv2
# import depthai as dai
# import numpy as np
# import time
# from datetime import datetime
# import open3d as o3d
# # import RPi.GPIO as GPIO
# from subprocess import Popen
# import asyncio
# # import socket


# #start_time=now.strftime("%H:%M:%S")

# cmd_start='espeak '
# cmd_end=' 2>/dev/null'
# '''
# Spatial Tiny-yolo example
#   Performs inference on RGB camera and retrieves spatial location coordinates: x,y,z relative to the center of depth map.
#   Can be used for tiny-yolo-v3 or tiny-yolo-v4 networks
# '''

# # setup socket
# # HOST = '155.41.122.253'
# # PORT = 2000
# # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # s.connect((HOST,PORT))

# #setup PI
# # GPIO.setmode(GPIO.BOARD)
# # #motor1
# # GPIO.setup(8,GPIO.OUT)
# # pwm2 = GPIO.PWM(8, 100)
# # pwm2.start(0)
# # #motor2
# # GPIO.setup(10,GPIO.OUT)
# # pwm3 = GPIO.PWM(10, 100)
# # pwm3.start(0)

# # GPIO.setup(12,GPIO.OUT)
# # pwm1=GPIO.PWM(12,100)
# # pwm1.start(0)
# # Get argument first



# # def yolo_task(labelMap):

# start=datetime.now()

# nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
# if 1 < len(sys.argv):
#     arg = sys.argv[1]
#     if arg == "yolo3":
#         nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v3-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
#     elif arg == "yolo4":
#         nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
#     else:
#         nnBlobPath = arg
# else:
#     print("Using Tiny YoloV4 model. If you wish to use Tiny YOLOv3, call 'tiny_yolo.py yolo3'")

# if not Path(nnBlobPath).exists():
#     import sys
#     raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# labelMap = [
#         "person",         "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
#         "truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
#         "bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
#         "bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
#         "suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
#         "baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
#         "fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
#         "orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
#         "chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
#         "laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
#         "toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
#         "teddy bear",     "hair drier", "toothbrush"
#     ]

# syncNN = True

# # Create pipeline
# pipeline = dai.Pipeline()

# # Define sources and outputs
# camRgb = pipeline.create(dai.node.ColorCamera)
# monoLeft = pipeline.create(dai.node.MonoCamera)
# monoRight = pipeline.create(dai.node.MonoCamera)
# stereo = pipeline.create(dai.node.StereoDepth)



# # xoutRgb.setStreamName("rgb")
# # xoutDepth.setStreamName("depth")


# # Properties
# camRgb.setPreviewSize(416, 416)
# camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
# camRgb.setInterleaved(False)
# camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
# monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
# monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
# monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# # setting node configs
# stereo.initialConfig.setConfidenceThreshold(255)




# xoutRgb = pipeline.create(dai.node.XLinkOut)
# xoutNN = pipeline.create(dai.node.XLinkOut)
# xoutDepth = pipeline.create(dai.node.XLinkOut)

# spatialDetectionNetwork = pipeline.create(dai.node.YoloSpatialDetectionNetwork)
# xoutBoundingBoxDepthMapping = pipeline.create(dai.node.XLinkOut)
# xoutNN.setStreamName("detections")
# xoutRgb.setStreamName("rgb")
# xoutDepth.setStreamName("depth")
# xoutBoundingBoxDepthMapping.setStreamName("boundingBoxDepthMapping")

# spatialDetectionNetwork.setBlobPath(nnBlobPath)
# spatialDetectionNetwork.setConfidenceThreshold(0.5)
# spatialDetectionNetwork.input.setBlocking(False)
# spatialDetectionNetwork.setBoundingBoxScaleFactor(0.5)
# spatialDetectionNetwork.setDepthLowerThreshold(100)
# spatialDetectionNetwork.setDepthUpperThreshold(5000)

# # Yolo specific parameters
# spatialDetectionNetwork.setNumClasses(80)
# spatialDetectionNetwork.setCoordinateSize(4)
# spatialDetectionNetwork.setAnchors(np.array([10,14, 23,27, 37,58, 81,82, 135,169, 344,319]))
# spatialDetectionNetwork.setAnchorMasks({ "side26": np.array([1,2,3]), "side13": np.array([3,4,5]) })
# spatialDetectionNetwork.setIouThreshold(0.5)

# # Linking
# monoLeft.out.link(stereo.left)
# monoRight.out.link(stereo.right)

# camRgb.preview.link(spatialDetectionNetwork.input)
# if syncNN:
#     spatialDetectionNetwork.passthrough.link(xoutRgb.input)
# else:
#     camRgb.preview.link(xoutRgb.input)

# spatialDetectionNetwork.out.link(xoutNN.input)
# spatialDetectionNetwork.boundingBoxMapping.link(xoutBoundingBoxDepthMapping.input)

# stereo.depth.link(spatialDetectionNetwork.inputDepth)
# spatialDetectionNetwork.passthroughDepth.link(xoutDepth.input)

# # Connect to device and start pipeline
# with dai.Device(pipeline) as device:

#     # Output queues will be used to get the rgb frames and nn data from the outputs defined above
#     previewQueue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
#     detectionNNQueue = device.getOutputQueue(name="detections", maxSize=4, blocking=False)
#     xoutBoundingBoxDepthMappingQueue = device.getOutputQueue(name="boundingBoxDepthMapping", maxSize=4, blocking=False)
#     depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

#     # #################PC
#     # qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)

#     # try:
#     #     from projector_3d import PointCloudVisualizer
#     # except ImportError as e:
#     #     raise ImportError(f"\033[1;5;31mError occured when importing PCL projector: {e}. Try disabling the point cloud \033[0m ")
#     # calibData = device.readCalibration()
#     # right_intrinsic = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RIGHT, 640, 400))
#     # pcl_converter = PointCloudVisualizer(right_intrinsic, 640, 400)
#     # #################PC

#     startTime = time.monotonic()
#     counter = 0
#     fps = 0
#     color = (255, 255, 255)
#     detcount = 0

#     while True:
#         inPreview = previewQueue.get()
#         inDet = detectionNNQueue.get()
#         depth = depthQueue.get()

#         frame = inPreview.getCvFrame()
#         depthFrame = depth.getFrame()
#         depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
#         depthFrameColor = cv2.equalizeHist(depthFrameColor)
#         depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)

#         counter+=1
#         current_time = time.monotonic()
#         if (current_time - startTime) > 1 :
#             fps = counter / (current_time - startTime)
#             counter = 0
#             startTime = current_time

#         detections = inDet.detections
#         if len(detections) != 0:
#             boundingBoxMapping = xoutBoundingBoxDepthMappingQueue.get()
#             roiDatas = boundingBoxMapping.getConfigData()

#             for roiData in roiDatas:
#                 roi = roiData.roi
#                 roi = roi.denormalize(depthFrameColor.shape[1], depthFrameColor.shape[0])
#                 topLeft = roi.topLeft()
#                 bottomRight = roi.bottomRight()
#                 xmin = int(topLeft.x)
#                 ymin = int(topLeft.y)
#                 xmax = int(bottomRight.x)
#                 ymax = int(bottomRight.y)

#                 cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)


#         # If the frame is available, draw bounding boxes on it and show the frame
#         height = frame.shape[0]
#         width  = frame.shape[1]
#         for detection in detections:
#             # Denormalize bounding box
#             if detcount < 51: # check if less than n detections have been made
#                 detcount += 1
#             else:
#                 detcount = 0
#             x1 = int(detection.xmin * width)
#             x2 = int(detection.xmax * width)
#             y1 = int(detection.ymin * height)
#             y2 = int(detection.ymax * height)
#             try:
#                 label = labelMap[detection.label]
                
#                 current=datetime.now()
#                 diff=current-start
#                 if ((diff.seconds%5==0) and (detection.confidence>10)): # send out label after n-1 detections
#                     print(label) # label of object detected
#                     print(detection.confidence)
#                     print(diff.seconds)
                    
                    
#                     vdistance=str(round((detection.spatialCoordinates.z/1000),1))
#                     hdistance=str(abs(round((detection.spatialCoordinates.x/1000),1)))
#                     vd=("m"+"front")
#                     Popen([cmd_start+label+vdistance+vd+cmd_end],shell=True)
#                     if detection.spatialCoordinates.x <=0:
#                         ld=("m"+"left")
#                         Popen([cmd_start+label+vdistance+vd+hdistance+ld+cmd_end],shell=True)
#                     elif detection.spatialCoordinates.x >0:
#                         rd=("m"+"right")
#                         Popen([cmd_start+label+vdistance+vd+hdistance+rd+cmd_end],shell=True)
#                     #print(detection.spatialCoordinates.z / 1000, "m") # z-distance from object in m
            
#             except:
#                 label = detection.label
#             cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
#             cv2.putText(frame, "{:.2f}".format(detection.confidence*100), (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
#             cv2.putText(frame, f"X: {int(detection.spatialCoordinates.x)} mm", (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
#             cv2.putText(frame, f"Y: {int(detection.spatialCoordinates.y)} mm", (x1 + 10, y1 + 65), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
#             cv2.putText(frame, f"Z: {int(detection.spatialCoordinates.z)} mm", (x1 + 10, y1 + 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)

#             cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

#         cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)
#         cv2.imshow("depth", depthFrameColor)
#         cv2.imshow("rgb", frame)

#     #     #########################PC
#     #     corners = np.asarray([[-0.5,-1.0,0.35],[0.5,-1.0,0.35],[0.5,1.0,0.35],[-0.5,1.0,0.35],[-0.5,-1.0,1.7],[0.5,-1.0,1.7],[0.5,1.0,1.7],[-0.5,1.0,1.7]])
        
#     #     bounds = corners.astype("float64")
#     #     bounds = o3d.utility.Vector3dVector(bounds)
#     #     oriented_bounding_box = o3d.geometry.OrientedBoundingBox.create_from_points(bounds)
        
#     #     inRight = qRight.get()
#     #     right = inRight.getFrame()

#     #     frame = depth.getFrame()
#     #     median = cv2.medianBlur(frame, 5)
#     #     median2 = cv2.medianBlur(median,5)

#     #     pcd = pcl_converter.rgbd_to_projection(median, right,False)

#     #     #to get points within bounding box
#     #     num_pts = oriented_bounding_box.get_point_indices_within_bounding_box(pcd.points)


#     #     if not isstarted:
#     #         vis.add_geometry(pcd)
#     #         vis.add_geometry(oriented_bounding_box)
#     #         isstarted = True       
                        
#     #     else:
#     #         vis.update_geometry(pcd)
#     #         vis.update_geometry(oriented_bounding_box)
#     #         vis.poll_events()
#     #         vis.update_renderer()
#     #     if len(num_pts)>5000:
#     #         print("Obstacle")
#     #         # s.send(bytes('1','utf-8'))
#     #     else:
#     #         print("Nothing")
#     #         # s.send(bytes('0','utf-8'))

#     #     if cv2.waitKey(1) == ord('q'):
#     #         break
#     # if pcl_converter is not None:
#     #     pcl_converter.close_window()

# '''
# async def pointCloud_task(pipeline, stereo):

#     extended = False
#     out_depth = False
#     out_rectified = True
#     # Better accuracy for longer distance, fractional disparity 32-levels:
#     subpixel = False
#     # Better handling for occlusions:
#     lr_check = True

#     xoutRight = pipeline.create(dai.node.XLinkOut)
#     xoutRight.setStreamName("right")
#     monoRight.out.link(xoutRight.input)


#     # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
#     stereo.initialConfig.setConfidenceThreshold(245)
#     # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
#     stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
#     stereo.setLeftRightCheck(lr_check)
#     stereo.setExtendedDisparity(extended)
#     stereo.setSubpixel(subpixel)

#     right = None
#     pcl_converter = None
#     vis = o3d.visualization.Visualizer()
#     vis.create_window()
#     isstarted = False
    
#     with dai.Device(pipeline) as device:
#         qDepth = device.getOutputQueue(name="depth", maxSize=4, blocking=False)
#         qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)

#         try:
#             from projector_3d import PointCloudVisualizer
#         except ImportError as e:
#             raise ImportError(f"\033[1;5;31mError occured when importing PCL projector: {e}. Try disabling the point cloud \033[0m ")
#         calibData = device.readCalibration()
#         right_intrinsic = numpy.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RIGHT, 640, 400))
#         pcl_converter = PointCloudVisualizer(right_intrinsic, 640, 400)

#         while True:
            
#             #to get prism
#             # was at the border work 0.7 to 2.2 with 1/4 z rotation 
#             corners = numpy.asarray([[-0.5,-1.0,0.35],[0.5,-1.0,0.35],[0.5,1.0,0.35],[-0.5,1.0,0.35],[-0.5,-1.0,1.7],[0.5,-1.0,1.7],[0.5,1.0,1.7],[-0.5,1.0,1.7]])

            
            
#             bounds = corners.astype("float64")
#             bounds = o3d.utility.Vector3dVector(bounds)
#             oriented_bounding_box = o3d.geometry.OrientedBoundingBox.create_from_points(bounds)
            
            

#             inRight = qRight.get()
#             right = inRight.getFrame()

#             # cv2.imshow("right", right)

#             inDepth = qDepth.get()
#             frame = inDepth.getFrame()
#             median = cv2.medianBlur(frame, 5)
#             median2 = cv2.medianBlur(median,5)
#             # cv2.imshow("depth",median2)
        
            
#             pcd = pcl_converter.rgbd_to_projection(median, right,False)
                
#             #to get points within bounding box
#             num_pts = oriented_bounding_box.get_point_indices_within_bounding_box(pcd.points)


#             if not isstarted:
#                 vis.add_geometry(pcd)
#                 vis.add_geometry(oriented_bounding_box)
#                 isstarted = True       
                            
#             else:
#                 vis.update_geometry(pcd)
#                 vis.update_geometry(oriented_bounding_box)
#                 vis.poll_events()
#                 vis.update_renderer()
#             if len(num_pts)>5000:
#                 print("Obstacle")
#                 # s.send(bytes('1','utf-8'))
#             else:
#                 print("Nothing")
#                 # s.send(bytes('0','utf-8'))

#             if cv2.waitKey(1) == ord("q"):
#                 break

#         if pcl_converter is not None:
#             pcl_converter.close_window()


# def main(): 
#     # Tiny yolo v3/4 label texts
    
#     yolo_task(labelMap)

# if __name__ == '__main__':
#     main()
# '''

#!/usr/bin/env python3
#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

from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
import time
from datetime import datetime
import open3d as o3d
# import RPi.GPIO as GPIO
from subprocess import Popen
# import socket
from depthai_setup import DepthAi
from projector_3d import PointCloudVisualizer


start=datetime.now()
#start_time=now.strftime("%H:%M:%S")

cmd_start='espeak '
cmd_end=' 2>/dev/null'
'''
Spatial Tiny-yolo example
  Performs inference on RGB camera and retrieves spatial location coordinates: x,y,z relative to the center of depth map.
  Can be used for tiny-yolo-v3 or tiny-yolo-v4 networks
'''

# setup socket
# HOST = '155.41.122.253'
# PORT = 2000
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST,PORT))

#setup PI
# GPIO.setmode(GPIO.BOARD)
# #motor1
# GPIO.setup(8,GPIO.OUT)
# pwm2 = GPIO.PWM(8, 100)
# pwm2.start(0)
# #motor2
# GPIO.setup(10,GPIO.OUT)
# pwm3 = GPIO.PWM(10, 100)
# pwm3.start(0)

# GPIO.setup(12,GPIO.OUT)
# pwm1=GPIO.PWM(12,100)
# pwm1.start(0)
# Get argument first
# nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
# if 1 < len(sys.argv):
#     arg = sys.argv[1]
#     if arg == "yolo3":
#         nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v3-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
#     elif arg == "yolo4":
#         nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
#     else:
#         nnBlobPath = arg
# else:
#     print("Using Tiny YoloV4 model. If you wish to use Tiny YOLOv3, call 'tiny_yolo.py yolo3'")

# if not Path(nnBlobPath).exists():
#     import sys
#     raise FileNotFoundError(f'Required file/s not found, please run "{sys.executable} install_requirements.py"')

# # Tiny yolo v3/4 label texts
# labelMap = [
#     "person",         "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
#     "truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
#     "bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
#     "bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
#     "suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
#     "baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
#     "fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
#     "orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
#     "chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
#     "laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
#     "toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
#     "teddy bear",     "hair drier", "toothbrush"
# ]

# syncNN = True



# ###################PC
# extended = False
# out_depth = False
# out_rectified = True
# # Better accuracy for longer distance, fractional disparity 32-levels:
# subpixel = False
# # Better handling for occlusions:
# lr_check = True
# ###################PC

# # Create pipeline
# pipeline = dai.Pipeline()

# # Define sources and outputs
# camRgb = pipeline.create(dai.node.ColorCamera)
# spatialDetectionNetwork = pipeline.create(dai.node.YoloSpatialDetectionNetwork)
# monoLeft = pipeline.create(dai.node.MonoCamera)
# monoRight = pipeline.create(dai.node.MonoCamera)
# stereo = pipeline.create(dai.node.StereoDepth)

# xoutRgb = pipeline.create(dai.node.XLinkOut)
# xoutNN = pipeline.create(dai.node.XLinkOut)
# xoutBoundingBoxDepthMapping = pipeline.create(dai.node.XLinkOut)
# xoutDepth = pipeline.create(dai.node.XLinkOut)
# xoutRight = pipeline.create(dai.node.XLinkOut)

# xoutRgb.setStreamName("rgb")
# xoutNN.setStreamName("detections")
# xoutBoundingBoxDepthMapping.setStreamName("boundingBoxDepthMapping")
# xoutDepth.setStreamName("depth")
# xoutRight.setStreamName("right")

# # Properties
# camRgb.setPreviewSize(416, 416)
# camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
# camRgb.setInterleaved(False)
# camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
# monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
# monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
# monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# # setting node configs
# stereo.initialConfig.setConfidenceThreshold(255)

# spatialDetectionNetwork.setBlobPath(nnBlobPath)
# spatialDetectionNetwork.setConfidenceThreshold(0.5)
# spatialDetectionNetwork.input.setBlocking(False)
# spatialDetectionNetwork.setBoundingBoxScaleFactor(0.5)
# spatialDetectionNetwork.setDepthLowerThreshold(100)
# spatialDetectionNetwork.setDepthUpperThreshold(5000)

# # Yolo specific parameters
# spatialDetectionNetwork.setNumClasses(80)
# spatialDetectionNetwork.setCoordinateSize(4)
# spatialDetectionNetwork.setAnchors(np.array([10,14, 23,27, 37,58, 81,82, 135,169, 344,319]))
# spatialDetectionNetwork.setAnchorMasks({ "side26": np.array([1,2,3]), "side13": np.array([3,4,5]) })
# spatialDetectionNetwork.setIouThreshold(0.5)

# # Linking
# monoLeft.out.link(stereo.left)
# monoRight.out.link(stereo.right)
# monoRight.out.link(xoutRight.input)

# camRgb.preview.link(spatialDetectionNetwork.input)
# if syncNN:
#     spatialDetectionNetwork.passthrough.link(xoutRgb.input)
# else:
#     camRgb.preview.link(xoutRgb.input)

# spatialDetectionNetwork.out.link(xoutNN.input)
# spatialDetectionNetwork.boundingBoxMapping.link(xoutBoundingBoxDepthMapping.input)

# stereo.depth.link(spatialDetectionNetwork.inputDepth)
# spatialDetectionNetwork.passthroughDepth.link(xoutDepth.input)

# ###################PC
# # Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
# stereo.initialConfig.setConfidenceThreshold(245)
# # Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
# stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
# stereo.setLeftRightCheck(lr_check)
# stereo.setExtendedDisparity(extended)
# stereo.setSubpixel(subpixel)

# right = None
# pcl_converter = None
# vis = o3d.visualization.Visualizer()
# vis.create_window()
# isstarted = False
# ###################PC



# Connect to device and start pipeline
# with dai.Device() as device:
#     device.startPipeline(pipeline.pipeline)
#     # Output queues will be used to get the rgb frames and nn data from the outputs defined above
#     previewQueue = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
#     detectionNNQueue = device.getOutputQueue(name="detections", maxSize=4, blocking=False)
#     xoutBoundingBoxDepthMappingQueue = device.getOutputQueue(name="boundingBoxDepthMapping", maxSize=4, blocking=False)
#     depthQueue = device.getOutputQueue(name="depth", maxSize=4, blocking=False)

#     # #################PC
#     # qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)

#     # try:
#     #     from projector_3d import PointCloudVisualizer
#     # except ImportError as e:
#     #     raise ImportError(f"\033[1;5;31mError occured when importing PCL projector: {e}. Try disabling the point cloud \033[0m ")
#     # calibData = device.readCalibration()
#     # right_intrinsic = np.array(calibData.getCameraIntrinsics(dai.CameraBoardSocket.RIGHT, 640, 400))
#     # pcl_converter = PointCloudVisualizer(right_intrinsic, 640, 400)
#     # #################PC

#     startTime = time.monotonic()
#     counter = 0
#     fps = 0
#     color = (255, 255, 255)
#     detcount = 0

#     while True:
#         inPreview = previewQueue.get()
#         inDet = detectionNNQueue.get()
#         depth = depthQueue.get()

#         frame = inPreview.getCvFrame()
#         depthFrame = depth.getFrame()
#         depthFrameColor = cv2.normalize(depthFrame, None, 255, 0, cv2.NORM_INF, cv2.CV_8UC1)
#         depthFrameColor = cv2.equalizeHist(depthFrameColor)
#         depthFrameColor = cv2.applyColorMap(depthFrameColor, cv2.COLORMAP_HOT)

#         counter+=1
#         current_time = time.monotonic()
#         if (current_time - startTime) > 1 :
#             fps = counter / (current_time - startTime)
#             counter = 0
#             startTime = current_time

#         detections = inDet.detections
#         if len(detections) != 0:
#             boundingBoxMapping = xoutBoundingBoxDepthMappingQueue.get()
#             roiDatas = boundingBoxMapping.getConfigData()

class Main:
    depthai_class = DepthAi

    def __init__(self):
        self.nnBlobPath = nnBlobPath = str((Path(__file__).parent / Path('../models/yolo-v4-tiny-tf_openvino_2021.4_6shave.blob')).resolve().absolute())
        self.depthai = self.depthai_class(self.nnBlobPath)
        self.labelMap = [
            "person",         "bicycle",    "car",           "motorbike",     "aeroplane",   "bus",           "train",
            "truck",          "boat",       "traffic light", "fire hydrant",  "stop sign",   "parking meter", "bench",
            "bird",           "cat",        "dog",           "horse",         "sheep",       "cow",           "elephant",
            "bear",           "zebra",      "giraffe",       "backpack",      "umbrella",    "handbag",       "tie",
            "suitcase",       "frisbee",    "skis",          "snowboard",     "sports ball", "kite",          "baseball bat",
            "baseball glove", "skateboard", "surfboard",     "tennis racket", "bottle",      "wine glass",    "cup",
            "fork",           "knife",      "spoon",         "bowl",          "banana",      "apple",         "sandwich",
            "orange",         "broccoli",   "carrot",        "hot dog",       "pizza",       "donut",         "cake",
            "chair",          "sofa",       "pottedplant",   "bed",           "diningtable", "toilet",        "tvmonitor",
            "laptop",         "mouse",      "remote",        "keyboard",      "cell phone",  "microwave",     "oven",
            "toaster",        "sink",       "refrigerator",  "book",          "clock",       "vase",          "scissors",
            "teddy bear",     "hair drier", "toothbrush"
        ]
        self.isstarted = None
        self.pcl_converter = None


    def run_yolo_pc(self):
        color = (255, 255, 255)
        # isstarted = False
        # pcl_converter = None
        # vis = o3d.visualization.Visualizer()
        # vis.create_window()
        for frame, depthFrameColor, fps, depthFrame, pcFrame in self.depthai.yolo_det():
            for roiData in self.depthai.roiDatas:
                roi = roiData.roi
                roi = roi.denormalize(depthFrameColor.shape[1], depthFrameColor.shape[0])
                topLeft = roi.topLeft()
                bottomRight = roi.bottomRight()
                xmin = int(topLeft.x)
                ymin = int(topLeft.y)
                xmax = int(bottomRight.x)
                ymax = int(bottomRight.y)

                cv2.rectangle(depthFrameColor, (xmin, ymin), (xmax, ymax), color, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX)


            # If the frame is available, draw bounding boxes on it and show the frame
            height = frame.shape[0]
            width  = frame.shape[1]
            for detection in self.depthai.detections:
                # Denormalize bounding box
                # if detcount < 51: # check if less than n detections have been made
                #     detcount += 1
                # else:
                #     detcount = 0
                x1 = int(detection.xmin * width)
                x2 = int(detection.xmax * width)
                y1 = int(detection.ymin * height)
                y2 = int(detection.ymax * height)
                try:
                    label = self.labelMap[detection.label]
                    
                    current=datetime.now()
                    diff=current-start
                    if ((diff.seconds%5==0) and (detection.confidence>10)): # send out label after n-1 detections
                        print(label) # label of object detected
                        print(detection.confidence)
                        print(diff.seconds)
                        
                        
                        vdistance=str(round((detection.spatialCoordinates.z/1000),1))
                        hdistance=str(abs(round((detection.spatialCoordinates.x/1000),1)))
                        vd=("m"+"front")
                        Popen([cmd_start+label+vdistance+vd+cmd_end],shell=True)
                        if detection.spatialCoordinates.x <=0:
                            ld=("m"+"left")
                            Popen([cmd_start+label+vdistance+vd+hdistance+ld+cmd_end],shell=True)
                        elif detection.spatialCoordinates.x >0:
                            rd=("m"+"right")
                            Popen([cmd_start+label+vdistance+vd+hdistance+rd+cmd_end],shell=True)
                        #print(detection.spatialCoordinates.z / 1000, "m") # z-distance from object in m
                    
                except:
                    label = detection.label
                cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, "{:.2f}".format(detection.confidence*100), (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, f"X: {int(detection.spatialCoordinates.x)} mm", (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, f"Y: {int(detection.spatialCoordinates.y)} mm", (x1 + 10, y1 + 65), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                cv2.putText(frame, f"Z: {int(detection.spatialCoordinates.z)} mm", (x1 + 10, y1 + 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

            cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)
            cv2.imshow("depth", depthFrameColor)
            cv2.imshow("rgb", frame)
            if cv2.waitKey(1) == ord('q'):
                break

            
            corners = np.asarray([[-0.5,-1.0,0.35],[0.5,-1.0,0.35],[0.5,1.0,0.35],[-0.5,1.0,0.35],[-0.5,-1.0,1.7],[0.5,-1.0,1.7],[0.5,1.0,1.7],[-0.5,1.0,1.7]])

            bounds = corners.astype("float64")
            bounds = o3d.utility.Vector3dVector(bounds)
            oriented_bounding_box = o3d.geometry.OrientedBoundingBox.create_from_points(bounds)

            # inRight = qRight.get()
            right = pcFrame
 
            frame = depthFrame
            median = cv2.medianBlur(frame, 5)
            # median2 = cv2.medianBlur(median,5)

            
            self.pcl_converter = PointCloudVisualizer(self.depthai.right_intrinsic, 640, 400)

            pcd = self.pcl_converter.rgbd_to_projection(median, right,False)

            #to get points within bounding box
            num_pts = oriented_bounding_box.get_point_indices_within_bounding_box(pcd.points)


            if not self.isstarted:
                self.depthai.vis.add_geometry(pcd)
                self.depthai.vis.add_geometry(oriented_bounding_box)
                self.isstarted = True       
                        
            else:
                self.depthai.vis.update_geometry(pcd)
                self.depthai.vis.update_geometry(oriented_bounding_box)
                self.depthai.vis.poll_events()
                self.depthai.vis.update_renderer()
            if len(num_pts)>5000:
                print("Obstacle")
                # s.send(bytes('1','utf-8'))
            else:
                print("Nothing")
                # s.send(bytes('0','utf-8'))

        if self.pcl_converter is not None:
            self.pcl_converter.close_window()

    # def run_pointcloud(self): 

        
    #     corners = np.asarray([[-0.5,-1.0,0.35],[0.5,-1.0,0.35],[0.5,1.0,0.35],[-0.5,1.0,0.35],[-0.5,-1.0,1.7],[0.5,-1.0,1.7],[0.5,1.0,1.7],[-0.5,1.0,1.7]])

    #     bounds = corners.astype("float64")
    #     bounds = o3d.utility.Vector3dVector(bounds)
    #     oriented_bounding_box = o3d.geometry.OrientedBoundingBox.create_from_points(bounds)

    #     inRight = qRight.get()
    #     right = inRight.getFrame()

    #     frame = depth.getFrame()
    #     median = cv2.medianBlur(frame, 5)
    #     median2 = cv2.medianBlur(median,5)

    #     pcd = pcl_converter.rgbd_to_projection(median, right,False)

    #     #to get points within bounding box
    #     num_pts = oriented_bounding_box.get_point_indices_within_bounding_box(pcd.points)


    #     if not isstarted:
    #         vis.add_geometry(pcd)
    #         vis.add_geometry(oriented_bounding_box)
    #         isstarted = True       
                    
    #     else:
    #         vis.update_geometry(pcd)
    #         vis.update_geometry(oriented_bounding_box)
    #         vis.poll_events()
    #         vis.update_renderer()
    #     if len(num_pts)>5000:
    #         print("Obstacle")
    #         # s.send(bytes('1','utf-8'))
    #     else:
    #         print("Nothing")
    #         # s.send(bytes('0','utf-8'))

    #     if cv2.waitKey(1) == ord('q'):
    #         break
    # if pcl_converter is not None:
    #     pcl_converter.close_window()

if __name__ == '__main__':
    Main().run_yolo_pc()