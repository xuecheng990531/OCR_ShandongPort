from io import IncrementalNewlineDecoder
import re
from LAC import LAC
import cv2
import sys
sys.path.append('../')
from component_modules import autils

def ReRec2(path,ymin,ymax,xmin,xmax,value):
    image = cv2.imread(path)
    cropImg=image[int(ymin):int(ymax),int(xmin):int(xmax)]
    pos,value=autils.detect_img(cropImg)
    return pos,value

lac=LAC(mode='lac')
VIN='^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$'
Engine_no='^(?![0-9]+)(?![A-Z]+)[0-9A-Z]{7,10}$'
date='^((([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29))\\s+([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
province=['京','沪','津','渝','鲁','冀','晋','蒙','辽','吉','黑','苏','浙','皖','闽','赣','豫','湘','鄂','粤','桂','琼','川','贵','云','藏','陕','甘','青','宁','新','港','澳','台']


def match_haoma(pos,value,save_path):
    for i in range(len(pos)):
        if value[i][0] in province:
            #print(value[i])
            return value[i]
        elif '码' in value[i]:
            if value[i].split('码')[1]!="":
                #print(value[i])
                return value[i].split('码')[1]
            elif value[i+1][0] in province or value[i+1][1] in province:
                print(value[i+1])
                return value[i+1]
    else:
        return '0'

def match_cheliangleixing(pos,value,save_path):
    for i in range(len(pos)):
        if '车辆类型' in value[i] or '车钢类型' in value[i] or '车辆奥型' in value[i]:
            if len(value[i].split('型')[-1])>3:
                return value[i].split('型')[-1][1:]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+height:
                        return value[i]
        elif 'Vehicle Type' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-height*4<pos[i][0][1]<shr_pos[1][1]+height:
                    return value[i]
        elif '重型' and '半挂' in value[i]:
            return value[i]
    else:
        return '无'        

def match_suoyouren(pos,value,save_path):
    for i in range(len(pos)):
        if '所有人' in value[i] or '有人' in value[i]:
            if len(value[i].split('人')[-1])>1:
                return value[i].split('人')[-1]
        elif '所' in value[i] and '人' in value[i]:
            if len(value[i].split('人')[-1])>1:
                return value[i].split('人')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-height/2<pos[i][0][1]<shr_pos[2][1]+height/2 and 'Type' not in value[i]:
                        return value[i] 

        elif '中华人民共和国' in value[i]:
            name=[]
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/6)<pos[i][0][0]<shr_pos[1][0]+int(width/6) and shr_pos[3][1]+2.3*height<pos[i][0][1]<shr_pos[3][1]+int(height*3):
                    return value[i]
        elif '有限公司' in value[i]:
            return value[i]

def match_address(pos,value,save_path):
    for i in range(len(pos)):
        if '住址' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[0][1]<pos[i][0][1]<shr_pos[2][1]+int(height/2) and '类型' not in value[i]:
                    result=re.sub(r'[住址]*', '', value[i])
                    return result
        else:
            for i in range(len(pos)):
                if '公司' not in value[i]:
                    if '省' in value[i] or '县' in value[i] or '市' in value[i] or '区' in value[i] and '局' not in value[i]:
                        if '庄' in value[i+1] or '村' in value[i+1] or '室' in value[i+1]:
                            value_all=value[i]+value[i+1]
                            result=re.sub(r'[住址]*', '', value_all)
                            return result
                        else:
                            result=re.sub(r'[住址]*', '', value[i])
                            return result


def match_shiyongxingzhi(pos,value,save_path):
    for i in range(len(pos)):
        if '性质' in value[i]:
            if len(value[i].split('质')[-1])>1:
                return value[i].split('质')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+int(height/2):
                        return value[i]
        elif '品牌型号' in value[i]:
            ymin=pos[i][0][1]
            ymax=pos[i][2][1]
            xmin=pos[i][0][0]
            xmax=pos[i][2][0]
            img_height=pos[i][3][1]-pos[i][0][1]
            img_width=pos[i][1][0]-pos[i][0][0]
            pos,result=ReRec2(save_path,ymin-img_height,ymax+img_height*2,xmin-img_width*2,xmax,value='id5_xingzhi')
            result=''.join(result)
            if '非' in result:
                return '非'+result.split('非')[-1][:2]
            elif '韭' in result:
                return '非'+result.split('韭')[-1][:2]
            elif '生' in result:
                return '非'+result.split('生')[-1][:2]    
            elif '营运' in result:
                return '营运'
            elif '货运' in result:
                return '货运'
            else:
                return 0
        elif '货运' in value[i]:
            return '货运'
    else:
        return '0'


def match_pinpaixinghao(pos,value,save_path):
    for i in range(len(pos)):
        if '品牌' in value[i] and '号' in value[i]:
            if len(value[i].split('号')[-1])>5:
                return value[i].split('号')[-1]
        elif '牌' in value[i] and re.match('[0-9A-Z]',value[i].split('牌')[-1]):
            return value[i]
    else:
        return '0'
def match_cheliangshibiedaihao(pos,value,save_path):
    for i in range(len(pos)):
        if '识别' in value[i] or '代号' in value[i] or '车辆' in value[i] and '类' not in value[i]:
            if len(value[i].split('号')[-1])>5:
                return value[i].split('号')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2) <pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+int(height+height/2):
                        return value[i]
    else:
        return '0'


                

def match_fadongjihaoma(pos,value,save_path):
    for i in range(len(value)):
        if '发动机' in value[i]:
            if len(value[i].split('码')[-1])>5:
                return value[i].split('码')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[2][1]+height:
                        return value[i]
    else:
        return '0'
def match_zhucedate(pos,value,save_path):
    for i in range(len(pos)):
        if '注册日' in value[i] or '注册口' in value[i] or '册日期' in value[i]:
            if len(value[i].split('册')[-1])>7:
                return value[i].split('-')[0][-4:]
            else:
                ymin=pos[i][1][1]
                ymax=pos[i][2][1]
                xmin=pos[i][1][0]
                xmax=pos[i][2][0]
                img_height=pos[i][3][1]-pos[i][0][1]
                img_width=pos[i][1][0]-pos[i][0][0]
                pos,result=ReRec2(save_path,ymin-img_height,ymax+img_height*2,xmin,xmax+img_width*2.5,value='id5_zhucedate')
                result=''.join(result)
                return result
    else:
        return '0'

def match_zairenshu(pos,value,save_path):
    for i in range(len(value)):
        if '核定' in value[i] and '质量' not in value[i] and '人' in value[i]:
            if '人' in value[i]:
                a = re.findall("\d+\.?\d*", value[i])
                a=list(map(int,a))
                return str(a).replace('[','').replace(']','')+'人'
            elif '入' in value[i]:
                a = re.findall("\d+\.?\d*", value[i])
                a=list(map(int,a))
                return str(a).replace('[','').replace(']','')+'人'
        elif '人' in value[i] or '入' in value[i]:
            if value[i].split('人')[0].isdigit():
                return value[i].split('人')[0]+'人'
    else:
        return '0'

def match_weight_sum(pos,value,save_path):
    for i in range(len(value)):
        if '总质量' in value[i] or '总质' in value[i] or '总' in value[i] and '牵引' not in value[i] and '准' not in value[i]:
            if len(value[i])>5:
                result="".join(list(filter(str.isdigit, value[i])))
                return result+'kg'
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(3*width) and shr_pos[1][1]-int(2*height)<pos[i][0][1]<shr_pos[1][1]+height:
                        return value[i]
        elif '核定载质量' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+2*width and shr_pos[1][1]-int(4.4*height)<pos[i][0][1]<shr_pos[1][1]+height*2:
                    return value[i]
    else:
        return '0kg'
                

def match_weight_zhengbei(pos,value,save_path):
    for i in range(len(value)):
        if '整备' in value[i] or '备质量' in value[i] or '备至' in value[i] or '服备' in value[i] or '务质量' in value[i] and '人' not in value[i]:
            if 'kg' in value[i]:
                result="".join(list(filter(str.isdigit, value[i])))
                return result+'kg'
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[1][1]-int(height*2)<pos[i][0][1]<shr_pos[1][1]+height:
                        result="".join(list(filter(str.isdigit, value[i])))
                        return result+'kg'
        elif '核定' in value[i] and '载' in value[i] and '人' not in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width*7<pos[i][0][0]<shr_pos[0][0]-width and shr_pos[1][1]-int(2*height)<pos[i][0][1]<shr_pos[1][1]+height and '人' not in value[i]:
                    result="".join(list(filter(str.isdigit, value[i])))
                    return result+'kg'
    else:
        return '0'            

def match_weight_heding(pos,value,save_path):
    for i in range(len(value)):
        if '核定' in value[i] and '数' not in value[i] and '人' not in value[i] and '入' not in value[i] or '核定载质量' in value[i]:
            if value[i].split('量')[1]!="":
                return value[i].split('量')[1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(3*width) and shr_pos[1][1]-int(2*height)<pos[i][0][1]<shr_pos[2][1]:
                        if value[i]!='':
                            return '0kg'
                        else:
                            result="".join(list(filter(str.isdigit, value[i])))
                            return result+'kg'
    else:
        return '0'

def match_weight_qianyin(pos,value,save_path):
    for i in range(len(value)):
        # if '总质量' in value[i] and '准' in value[i]:
        #     if len(value[i].split('量')[1])>4:
        #         return value[i].split('量')[-1]
        #     else:
        #         shr_pos=pos[i]
        #         height=pos[i][3][1]-pos[i][0][1]
        #         width=pos[i][1][0]-pos[i][0][0]
        #         for i in range(len(pos)):
        #             if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[1][1]-int(3*height)<pos[i][0][1]<shr_pos[2][1]+height/2 and '核定' not in value[i]:
        #                 if value[i]!='':
        #                     return '0kg'
        #                 else:
        #                     return value[i]
        if '尺寸' in value[i] or '尺' in value[i]:
            chicun=[]
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]+width*5<pos[i][0][0]<shr_pos[1][0]+width*40 and shr_pos[1][1]-height*2.2<pos[i][0][1]<shr_pos[2][1]+height/2:
                    chicun.append(value[i])
            if len(chicun)>0:
                for i in range(len(chicun)):
                    if 'kg' in chicun[i]:
                        return chicun[i]
    else:
        return '0'
def match_chicun(pos,value,save_path):
    for i in range(len(value)):
        if '外' in value[i]:
            if len(value[i])>10:
                if '寸' in value[i]:
                    return value[i].split('寸')[-1].split('m')[0]+'mm'
                else:
                    return value[i].split('m')[0]+'mm'
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[1][1]+height:
                        if 'mm' in value[i]:
                            if '寸' in value[i]:
                                return value[i].split('寸')[-1].split('m')[0]+'mm'
                            else:
                                return value[i].split('m')[0]+'mm'
        elif 'mm' in value[i] or 'x' in value[i]:
            if '寸' in value[i]:
                return value[i].split('寸')[-1].split('m')[0]+'mm'
            else:
                return value[i].split('m')[0]+'mm'
    else:
        return '0'
def match_valid_date(pos,value,save_path):
    for i in range(len(value)):
        if '有效期' in value[i]:
            return value[i].split('至')[1].split('月')[0]+'月'
    else:
        return '0'
