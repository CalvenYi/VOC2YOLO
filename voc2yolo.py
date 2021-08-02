import xml.etree.ElementTree as ET
import pickle
import os,sys
from os import listdir, getcwd
from os.path import join

classes=["class1","class2","class3"]


def convert(size,box):
	# Conversion from VOC to YOLO format
	dw = 1./(size[0])
	dh = 1./(size[1])
	x = (box[0] + box[1])/2.0 - 1
	y = (box[2] + box[3])/2.0 - 1
	w = box[1] - box[0]
	h = box[3] - box[2]
	x = x*dw
	w = w*dw
	y = y*dh
	h = h*dh
	return (x,y,w,h)

#print ann_file
def converting_annotation(ann_file):
	for ann in ann_file:
		txt_file= ann.split('.')[0]+'.txt'
		in_file=open(os.path.join('Annotations',ann))
		out_file =open(os.path.join('yolo',txt_file), 'w')
		tree=ET.parse(in_file)
		root = tree.getroot()
		size = root.find('size')
		w = int(size.find('width').text)
		h = int(size.find('height').text)
		# 可选固定长宽
		if False:
			if w==481 or  w==641:
				w=641
				h=481
			else:
				w=640
				h=480

		print (ann, w, h)
		for obj in root.iter('object'):
			cls=obj.find('name').text
			if cls not in classes:
				continue
			cls_id=classes.index(cls)
			xmlbox = obj.find('bndbox')
			b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
			
			data = convert((w,h), b)
			out_file.write(str(cls_id) + " " + " ".join([str(a) for a in data]) + '\n')


if __name__ == '__main__': 
	ann_dir=sys.argv[1]
	ann_file=os.listdir(ann_dir)
	ann_file.sort()
	# print(ann_file)
	converting_annotation(ann_file)