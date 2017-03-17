#!/usr/bin/env python

import image

##dictionary
def make_dict(imagelist,statuslist):
    image_name = ["stand","stop","walk","attack","hit"]
    dire_name = ["front","back","right","left"]
    status_name = ["hp","atk","defe","speed","stamina"]

    dict = {}
    image_dict = {}
    status_dict = {}

    for name,imgs in zip(image_name,imagelist):
        d = {}
        for dire,img in zip(dire_name,imgs):
            imgobj = image.Images(img[0],img[1])
            d[dire] = imgobj
        image_dict[name] = d
    for name,status in zip(status_name,statuslist):
        status_dict[name] = status
    
    dict = {"imagedict":image_dict,"statusdict":status_dict}
    return dict

mc_imagelist = [[["../picture/mc/mc-front.png",1],
                 ["../picture/mc/mc-back.png",1],
                 ["../picture/mc/mc-right.png",1],
                 ["../picture/mc/mc-left.png",1]],
                [["../picture/mc/mc-front.png",1],
                 ["../picture/mc/mc-back.png",1],
                 ["../picture/mc/mc-right.png",1],
                 ["../picture/mc/mc-left.png",1]],
                [["../picture/mc/mc-front-walk.png",2],
                 ["../picture/mc/mc-back-walk.png",2],
                 ["../picture/mc/mc-right-walk.png",2],
                 ["../picture/mc/mc-left-walk.png",2]],
                [["../picture/mc/mc-front-atk.png",3],
                 ["../picture/mc/mc-back-atk.png",3],
                 ["../picture/mc/mc-right-atk.png",3],
                 ["../picture/mc/mc-left-atk.png",3]],
                [["../picture/mc/mc-front.png",1],
                 ["../picture/mc/mc-back.png",1],
                 ["../picture/mc/mc-right.png",1],
                 ["../picture/mc/mc-left.png",1]]]
mc_statuslist = [10,1,1,5,10]
mcdict = make_dict(mc_imagelist,mc_statuslist)


enemydict = {}

boar_imagelist = [[["../picture/boar/boar-front.png",1],
                   ["../picture/boar/boar-back.png",1],
                   ["../picture/boar/boar-right.png",1],
                   ["../picture/boar/boar-left.png",1]],
                  [["../picture/boar/boar-front.png",1],
                   ["../picture/boar/boar-back.png",1],
                   ["../picture/boar/boar-right.png",1],
                   ["../picture/boar/boar-left.png",1]],
                  [["../picture/boar/boar-front-walk.png",2],
                   ["../picture/boar/boar-back-walk.png",2],
                   ["../picture/boar/boar-right-walk.png",2],
                   ["../picture/boar/boar-left-walk.png",2]],
                  [["../picture/boar/boar-front-walk.png",2],
                   ["../picture/boar/boar-back-walk.png",2],
                   ["../picture/boar/boar-right-walk.png",2],
                   ["../picture/boar/boar-left-walk.png",2]],
                  [["../picture/boar/boar-front.png",1],
                   ["../picture/boar/boar-back.png",1],
                   ["../picture/boar/boar-right.png",1],
                   ["../picture/boar/boar-left.png",1]]]
boar_statuslist = [10,3,3,2]
enemydict["boar"] = make_dict(boar_imagelist,boar_statuslist)


objdict = {}
objdict["enemy"] = enemydict
