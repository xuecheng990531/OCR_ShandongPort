import re
from tkinter import E
from cv2 import RNG_NORMAL
from paddleocr import PaddleOCR

province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']


def match_fahuodanwei(pos,value,save_path):
    for i in range(len(pos)):
        if '计量单' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width*2<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-height*2<pos[i][0][1]<shr_pos[0][1] and '有限公司' in value[i]:
                    return value[i]
    else:
        return '日照中联港口水泥有限公司'     
def match_shouhuodanwei(pos,value,save_path):
    for i in range(len(pos)):
        if '客户' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+width*4 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]:
                    return value[i]


def match_jinchangzhongliang(pos,value,save_path):
    for i in range(len(pos)):
        if '进' in value[i] and '重' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][0][0]<shr_pos[0][0]+width/2 and shr_pos[0][1]+height/2<pos[i][0][1]<shr_pos[3][1]+height+height/2:
                    return value[i]

def match_chuchangzhongliang(pos,value,save_path):
    for i in range(len(pos)):
        if '出' in value[i] and '重' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][0][0]<shr_pos[0][0]+width/2 and shr_pos[0][1]+height/2<pos[i][0][1]<shr_pos[3][1]+height+height/2:
                    return value[i]

def match_jingzhong(pos,value,save_path):
    for i in range(len(pos)):
        if '净' in value[i] and '重' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][0][0]<shr_pos[0][0]+width/2 and shr_pos[0][1]+height/2<pos[i][0][1]<shr_pos[3][1]+height+height/2:
                    return value[i]
 
def match_wuliao(pos,value,save_path):
    for i in range(len(pos)):
        if '物料' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+width*4 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]:
                    return value[i]
    
        

def match_chehao(pos,value,save_path):
    for i in range(len(pos)):
        if '车牌' in value[i]:
            print('alksjdlka')
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][0][0]<shr_pos[0][0]+width/2 and shr_pos[0][1]+height/2<pos[i][0][1]<shr_pos[3][1]+height+height/2:
                    return value[i]
    else:
        pat=re.compile(r'[\u4e00-\u9fa5]+')
        for i in range(len(pos)):
            if value[i][0] in province:
                return value[i]
            elif  len(value[i])==7 and pat.findall(value[i]):
                return value[i]