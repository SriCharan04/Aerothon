import cv2
import rospy
import cv_bridge
import sensor_msgs.msg as msg

bridge = cv_bridge.CvBridge()
backSubtractor=cv2.BackgroundSubtractorMOG2

def contour_finder(frame):
    contour,hierarchy=cv2.findContours(frame,1,2)
    count=contour[0]
    epsilon = 0.1*cv2.arcLength(count,True)
    shape_vertices=cv2.approxPolyDP(count,epsilon,True)
    print(len(shape_vertices))

def converter(stream):
    frames=bridge.compressed_imgmsg_to_cv2(stream,'bgr8',"passthrough")
    obj_frames=backSubtractor.apply(frames)
    edge_frames = cv2.Canny(stream,100,200)
    contour_finder(edge_frames)
    cv2.imshow("display",edge_frames)

def display_routine():
    rospy.init_node("stream", anonymous = True)
    rospy.Subscriber("/camera/image_raw",msg.Image,converter)
    cv2.namedWindow("display")
    cv2.resizeWindow("display",1920,1080)
    rospy.spin()

    if _name_ == '_main_':
        display_routine()
