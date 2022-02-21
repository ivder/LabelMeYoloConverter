# -*- coding: utf-8 -*-

'''
LabelMe JSON format -> YOLO txt format
save dataset (학습 자료) in dataset/ 
output will be saved in result/
JSON format will be moved to json_backup/

Finally, please manually copy text file together with image into 1 folder. (Easier to maintain)
마지막으로 txt파일이랑 이미지파일이랑 같은 폴더에 복사하세요 (관리하기 위한 쉬움)
'''

import os
from os import walk, getcwd
from PIL import Image

#Changed the convert function so it can extract the bounding boxes coordinates
#for using it with Yolov5.

def convert(size, box):
    x = round((b[0] + b[1])/2, 5) # b_center_x
    y = round((b[2] + b[3])/2, 5) #b_center_y
    w = round((b[1] - b[0]), 5) #b_width
    h = round((b[3] - b[2]), 5) #b_height

# Normalise the co-ordinates by the dimensions of the image
    image_w, image_h = size
    x /= image_w #b_center_x
    y /= image_h #b_center_y
    w /= image_w #b_width
    h /= image_h #b_height
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath = "./dataset/"
outpath = "./result/"
json_backup ="./json_backup/"

wd = getcwd()
#list_file = open('%s_list.txt'%(wd), 'w')

""" Get input json file list """
json_name_list = []
for file in os.listdir(mypath):
    if file.endswith(".json"):
        json_name_list.append(file)
    

""" Process """
for json_name in json_name_list:
    txt_name = json_name.rstrip(".json") + ".txt"
    """ Open input text files """
    txt_path = mypath + json_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    """ Open output text files """
    txt_outpath = outpath + txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "a")

    """ Convert the data to YOLO format """ 
    lines = txt_file.read().split('\r\n')   #for ubuntu, use "\r\n" instead of "\n"
    for idx, line in enumerate(lines):
        if ("lineColor" in line):
            break 	#skip reading after find lineColor
        if ("label" in line):
            x1 = float(lines[idx+5].rstrip(','))
            y1 = float(lines[idx+6])
            x2 = float(lines[idx+9].rstrip(','))
            y2 = float(lines[idx+10])
            cls = line[16:17]

	    #in case when labelling, points are not in the right order
	    xmin = min(x1,x2)
	    xmax = max(x1,x2)
     	    ymin = min(y1,y2)
	    ymax = max(y1,y2)
            img_path = str('%s/dataset/%s.jpg'%(wd, os.path.splitext(json_name)[0]))

            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])

            print(w, h)
            print(xmin, xmax, ymin, ymax)
            b = (xmin, xmax, ymin, ymax)
            bb = convert((w,h), b)
            print(bb)
            txt_outfile.write(cls + " " + " ".join([str(a) for a in bb]) + '\n')

    os.rename(txt_path,json_backup+json_name)	#move json file to backup folder
  
