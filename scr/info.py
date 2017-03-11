#!/usr/bin/env python

import image

##dictionary
def make_dict(imagelist,statuslist):
    image_name = ["fstand","bstand","rstand","lstand",
                  "fwalk","bwalk","rwalk","lwalk",
                  "fattack","battack","rattack","lattack"]
    status_name = ["hp","atk","defe","speed","stamina"]

    dict = {}
    image_dict = {}
    status_dict = {}

    for name,img in zip(image_name,imagelist):
        imgobj = image.Images(img[0],img[1])
        image_dict[name] = imgobj
    for name,status in zip(status_name,statuslist):
        status_dict[name] = status
    
    dict = {"imagedict":image_dict,"statusdict":status_dict}
    return dict

mc_imagelist = [["../picture/mc/mc-front.png",1],
                ["../picture/mc/mc-back.png",1],
                ["../picture/mc/mc-right.png",1],
                ["../picture/mc/mc-left.png",1],
                ["../picture/mc/mc-front-walk.png",2],
                ["../picture/mc/mc-back-walk.png",2],
                ["../picture/mc/mc-right-walk.png",2],
                 ["../picture/mc/mc-left-walk.png",2]]
mc_statuslist = [10,1,1,5,10]
mcdict = make_dict(mc_imagelist,mc_statuslist)


enemydict = {}



objdict = {}
objdict["enemy"] = enemydict
