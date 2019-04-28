
import base64
import io as cStringIO
import sys
import tempfile
from flask import jsonify
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
import tensorflow as tf
from object_detection.utils import label_map_util
import sys






PATH_TO_CKPT = r'E:\inference\frozen_inference_graph.pb'
PATH_TO_LABELS =r'E:\Projects\numbers_fyp\data\object_det.pbtxt'

content_types = {'jpg': 'image/jpeg',
                 'jpeg': 'image/jpeg',
                 'png': 'image/png'}
extensions = sorted(content_types.keys())


class ObjectDetector(object):

  def __init__(self):
    self.detection_graph = self._build_graph()
    self.sess = tf.Session(graph=self.detection_graph)

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True)
    self.category_index = label_map_util.create_category_index(categories)

  def _build_graph(self):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    return detection_graph

  def _load_image_into_numpy_array(self, image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

  def detect(self, image):
    image_np = self._load_image_into_numpy_array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)

    graph = self.detection_graph
    image_tensor = graph.get_tensor_by_name('image_tensor:0')
    boxes = graph.get_tensor_by_name('detection_boxes:0')
    scores = graph.get_tensor_by_name('detection_scores:0')
    classes = graph.get_tensor_by_name('detection_classes:0')
    num_detections = graph.get_tensor_by_name('num_detections:0')

    (boxes, scores, classes, num_detections) = self.sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})

    boxes, scores, classes, num_detections = map(
        np.squeeze, [boxes, scores, classes, num_detections])

    return boxes, scores, classes.astype(int), num_detections





def detect_objects(image_path):
  image = Image.open(image_path).convert('RGB')
  im =cv2.imread(image_path,0)
  result = {}
  im_width, im_height = image.size
  boxes, scores, classes, num_detections = client.detect(image)
  image.thumbnail((480, 480), Image.ANTIALIAS)

  new_images = {}
  for i in range(int(num_detections)):
    #print([i])
    if scores[i] < 0.5: continue
    cls = classes[i]
    #if cls not in new_images.keys():
      #new_images[cls] = image.copy()
    #draw_bounding_box_on_image(new_images[cls], boxes[i],
                               #thickness=int(4))
    ymin, xmin, ymax, xmax = boxes[i]
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
    result[left]={'category':client.category_index[cls]['name'],'left':left,'right':right,'top':top,'bottom':bottom}
  #result['original'] = encode_image(image.copy(),'og')

  """for cls, new_image in new_images.items():
    category = client.category_index[cls]['name']
    result[category] = encode_image(new_image,'detc')"""
  #print(result)
  bill=cal_bill(result,im)
  result['bill']=bill

  return result

def cal_bill(result,im):
  c=0.01
  unit=0
  
  
  keys=sorted(result,reverse=True)
  print(keys)
  for i in keys:
    im=cv2.rectangle(im,(int(result[i]['left']),int(result[i]['top'])),(int(result[i]['right']),int(result[i]['bottom'])),(0,255,0),3)
    cv2.imshow("im",im)
    print(result[i]['category'])
    unit=unit+ (int(result[i]['category'])*c)
    #print(unit)
    c=c*10
    cv2.imwrite(r"E:\Projects\desktop_app\app\result\bound.jpg",im)
    cv2.waitKey(0) 
  bill=unit*1.5
  return bill
	  



client = ObjectDetector()
path = r"E:\CATDOG\fyp_push\images\test\20180806_141433.jpg"
result=detect_objects(path)
#print(result)


