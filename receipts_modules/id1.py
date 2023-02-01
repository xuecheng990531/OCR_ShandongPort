import re
import sys
import cv2
sys.path.append('../')
from component_modules import autils

def ReRec2(path,ymin,ymax,xmin,xmax,value):
    print(path)
    print(ymin,ymax,xmin,xmax)
    image = cv2.imread(path)
    cropImg=image[int(ymin):int(ymax),int(xmin):int(xmax)]
    cv2.imwrite('save_files/crop/'+str(value)+'.png',cropImg)
    pos,value=autils.detect_img('save_files/crop/'+str(value)+'.png')
    return pos,value

def match_fahuoren(pos,value,save_path):
    for i in range(len(pos)):
            if '发货人' in value[i]:
                if len(value[i])>5:
                    return value[i].split('人')[-1][1:]
                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                            return value[i]


def match_shouhuoren(pos,value,save_path):
    for i in range(len(pos)):
            if '收货' in value[i]:
                if len(value[i])>5:
                    return value[i][3:]
                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                            return value[i]

                    

def match_chengyunren(pos,value,save_path):
    for i in range(len(pos)):
            if '承运' in value[i]:
                if len(value[i])>5:
                    return value[i][3:]
                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                            return value[i]



def match_hangminghangci(pos,value,save_path):
    for i in range(len(pos)):
            if '航次' in value[i]:
                if len(value[i].split('次')[-1])>4:
                    return value[i].split('次')[-1]
                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                            return value[i]
    else:
        return '0'

def match_hangminghangci_english(pos,value,save_path):
    for i in range(len(pos)):
            if 'Voyage' in value[i]:
                #[78.0, 346.0, 215.0, 344.0, 216.0, 367.0, 78.0, 369.0]
                for i in range(len(pos)):
                    if 118<pos[i][1][0]-pos[i][0][0]<218 and 6<pos[i][2][1]-pos[i][0][1]< 76 and 48 < pos[i][0][0]< 108 and 340 < pos[i][3][1] < 400:
                        return value[i][0]
    else:
        return '0'

def match_zhuanghuogang(pos,value,save_path):
    for i in range(len(pos)):
            if '装货港' in value[i]:
                if len(value[i].split('港')[-1])>=2:
                    return value[i][3:]

                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                            return value[i]
    else:
        return '0'

def match_xiehuogang(pos,value,save_path):
    for i in range(len(pos)):
            if '卸货港' in value[i] or '御货港' in value[i]:
                if len(value[i].split('港')[1])>2:
                    return value[i][3:]
                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                            return value[i]
    else:
        return '0'

def match_tidanhao(pos,value,save_path):
    for i in range(len(pos)):
        if '提单号' in value[i]:
            if len(value[i].split('号')[-1])>4:
                return value[i].split('：')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-int(width/2)<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+int(height+height/2):
                        return value[i]
    else:
        return '0'

def match_IMO(pos,value,save_path):
    for i in range(len(pos)):
        if '危险类别' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/5)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+width:
                    return value[i]
    else:
        return '0'


def match_UN(pos,value,save_path):
    for i in range(len(pos)):
        if '危规编号' in value[i] and 'UN' in value[i]:
            if len(value[i].split('r')[-1])>2:
                m = re.search(r"\d", value[i])
                return value[i][int(m.start()):]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/6)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+int(height/2):
                        return value[i]
    else:
        return '0'        

def match_baozhuanglei(pos,value,save_path):
    for i in range(len(pos)):
            if 'group' in value[i]:
                if len(value[i].split('p')[-1])>2:
                    return value[i].split('p')[-1][1:]
                else:
                    shr_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0]-int(width/6)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+int(height/2):
                            return value[i]
    else:
        return '0'
                

def match_shandian(pos,value,save_path):
    for i in range(len(pos)):
        if '℃' in value[i] and value[i].split('℃')[0][-1].isdigit():
            number = re.findall("\d+",value[i])[0]
            return str(number)+'℃'
        elif '闪点' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/5)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+height:
                    if '应急' in value[i]:
                        return 'None'
                    else:
                        return value[i]
    else:
        return '0'

def match_yingjicuoshi(pos,value,save_path):
    for i in range(len(pos)):
        
        if '应急措施编号' in value[i]:
            if 'No' in value[i] and len(value[i].split('No')[-1])>2:
                return value[i].split('No')[-1]



def match_baojianzhonglei(pos,value,save_path):
    for i in range(len(pos)):
        if 'packages' in value[i] and 'Bulk' not in value[i] and '/' in value[i] and value[i].split('/')[-1][0].isdigit():
                return value[i].split('packages')[-1]
        else:
            if '/' in value[i]:
                if value[i].split('/')[-1].isdigit():
                    word=value[i].split('/')[0]
                    for ch in word:
                        if u'\u4e00'<=ch<=u'\u9fff':
                            if 'packages' in value[i]:
                                return value[i].split('packages')[-1]
                            else:
                                return value[i]
    else:
        return 'packages'

def match_kongzhiwendu(pos,value,save_path):
    for i in range(len(pos)):
            if 'emergency' in value[i]:
                if 85<pos[i][1][0]-pos[i][0][0]<100 and 6<pos[i][2][1]-pos[i][0][1]< 35 and 290 < pos[i][0][0]< 340 and 790 < pos[i][0][1] < 830:
                    if len(value[i].split(':')[-1])==0:
                        return '无'
                    else:
                        return value[i].split('y')[-1]

# def match_haiyangwuranwu(pos,value,save_path):
    # for i in range(len(pos)):
    #     if 'POLLUT' in value[i]:
    #         # shr_pos=pos[i]
    #         # height=pos[i][3][1]-pos[i][0][1]
    #         # width=pos[i][1][0]-pos[i][0][0]
    #         # for i in range(len(pos)):
    #         #     if shr_pos[0][0]-int(width/5)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+int(2*height):
    #         #             return value[i]
    #         ymin=pos[i][0][1]
    #         ymax=pos[i][2][1]
    #         xmin=pos[i][0][0]
    #         xmax=pos[i][2][0]
    #         img_height=pos[i][3][1]-pos[i][0][1]
    #         img_width=pos[i][1][0]-pos[i][0][0]
    #         pos,result=ReRec2(save_path,ymin,ymax+img_height*3,xmin-img_width/2,xmax,value='id1_wuranwu')
    #         result=''.join(result)
    #         if '是' in result:
    #             return '是'
    #         elif '否' in result:
    #             return '否'
    #         else:
    #             return result

# 新的检测方式
def match_haiyangwuranwu(pos,value,save_path):
    result=[]
    for i in range(len(pos)):
        if 'POLLUT' in value[i]:

            if '是' in value[i].split('POLLUT')[-1]:
                return '是'
            elif '否' in value[i].split('POLLUT')[-1]:
                return '否'
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-int(width/3)<pos[i][0][0]<shr_pos[0][0]+int(width/2) and shr_pos[3][1]-height*1.2<pos[i][0][1]<shr_pos[3][1]+height:
                        if '是' in value[i]:
                            return '是'
                        else:
                            return '否'



def match_zongzhong(pos,value,save_path):
    for i in range(len(pos)):
        if 'Total' in value[i] and 'weight' in value[i]:
            if len(value[i].split('k')[-1])>4:
                m = re.search(r"\d", value[i])
                return value[i][int(m.start()):]+'KG'
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-int(width/5)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+width:
                        return value[i]+'KG'
    else:
        return '0'

def match_jingzhong(pos,value,save_path):
    for i in range(len(pos)):
        if 'Net' in value[i] and 'weight' in value[i]:
            if len(value[i].split('g')[-1])>4:
                m = re.search(r"\d", value[i])
                return value[i][int(m.start()):]+'KG'
                
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-int(width/5)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+width:
                        return value[i]+'KG'
    else:
        return '0'

