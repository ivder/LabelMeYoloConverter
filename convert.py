# -*- coding: utf-8 -*-

'''
This code serves to convert LabelMe JSON files to YOLO format files. It works for both polygons as well as squares. <\br>
The code was executed on Google Colab (Jupyter Notebook). The folders were located on Google drive. <\br>
LabelMe saves both Images and json files to one folder, in this case ../images/train. <\br>
The code saves those JSON files to '.../json_backup' folder, deletes them from the original<\br>
'../images/train' folder and finally adds the YOLO txt format files to the '../labels/train' folder. <\br>
Make sure to change the directory paths.
'''
from google.colab import drive
drive.mount('/content/drive', force_remount=True)


import os
from os import walk, getcwd
from PIL import Image

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
mypath = '/content/drive/My Drive/microplasticos/images/train'
outpath = "/content/drive/My Drive/microplasticos/labels/train"
json_backup ="/content/drive/My Drive/microplasticos/json_backup"

wd = getcwd()
#list_file = open('%s_list.txt'%(wd), 'w')


'''correct .JPG to .jpg'''
#os.rename(old_name, new_name)


""" Get input json file list """
json_name_list = []
for file in os.listdir(mypath):
    if file.endswith(".json"):
        json_name_list.append(file)
    if '.JPG' in file:
        os.rename(mypath+'/'+file, mypath+'/'+file.strip('.JPG')+'.jpg')
    




""" Process """
for json_name in json_name_list:
    txt_name = json_name.rstrip(".json") + ".txt"
    """ Open input text files """
    txt_path = mypath +'/' + json_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    
    """ Open output text files """
    txt_outpath = outpath + '/'+ txt_name
    print("Output:" + txt_outpath)
    txt_outfile = open(txt_outpath, "a+")

    """ Create a label dictionary."""
    label_dic={'fragment': 0, 'line': 1, 'organic': 2, 'pellet': 3, 'tar': 4}

    """ Convert the data to YOLO format """ 
    lines = txt_file.read().split() #'\r\n'  #for ubuntu, use "\r\n" instead of "\n"
    for idx, line in enumerate(lines):
        if ("lineColor" in line):
            break     #skip reading after find lineColor
        if ("label" in line):
            idxlist=[element for element in range(5,90,4)] #[5,9,13,17,21,25,29,33,37,41,45...]
            pl=list() #list of polygon points
            try:
                for i in idxlist:
                    pl.append((float(lines[idx+i].rstrip(',')), float(lines[idx+i+1])))
                    cls = label_dic[lines[idx+1].rstrip(',').strip('"')]
            except:
                pass
            #print('pl: ',pl)

            #in case when labelling, points are not in the right order
            xmin=9999999
            xmax=0
            ymin=9999999
            ymax=0
            for (x,y) in pl:
              if x<xmin:
                xmin=x
              if x>xmax:
                xmax=x
              if y<ymin:
                ymin=y
              if y>ymax:
                ymax=y
            img_path = str('%s/%s.jpg'%(mypath, os.path.splitext(json_name)[0]))

            im=Image.open(img_path)
      
            w= int(im.size[0])
            h= int(im.size[1])
        
            

            print(w, h)
            print(xmin, xmax, ymin, ymax)
            b = (xmin, xmax, ymin, ymax)
            bb = convert((w,h), b)
            print('CLASS', cls)
            print(bb)
            txt_outfile.write(str(cls) + " " + " ".join([str(a) for a in bb]) + '\n')
           
       
    os.rename(txt_path,json_backup+'/'+json_name)    #move json file to backup folder
  
