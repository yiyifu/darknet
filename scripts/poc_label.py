import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


poc_path = '/data/train_data/poc'

sets=[('2020', 'train'), ('2020', 'val')]
# classes = ["person", "car", "bus", "lamp", "wheel", "licenseplate", "motorcycle", "tricycle"]
classes = ["car", "licenseplate"]


def convert(size, box):
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

def convert_annotation(year, image_id):
    in_file = open('%s/poc%s/annotations/%s.xml'%(poc_path, year, image_id))
    out_file = open('%s/poc%s/labels/%s.txt'%(poc_path, year, image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for year, image_set in sets:
    if not os.path.exists('%s/poc%s/labels/'%(poc_path, year)):
        os.makedirs('%s/poc%s/labels/'%(poc_path, year))
    image_ids = open('%s/poc%s/sets/%s.txt'%(poc_path, year, image_set)).read().strip().split()
    list_file = open('../data/poc/%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/poc%s/images/%s.jpg\n'%(poc_path, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()

os.system("cat ../data/poc/2020_train.txt > ../data/poc/train.txt")
os.system("cat ../data/poc/2020_train.txt ../data/poc/2020_val.txt > ../data/poc/train.all.txt")
