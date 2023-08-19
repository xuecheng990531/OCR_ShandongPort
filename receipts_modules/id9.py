from queue import Empty
import re
import cv2
import sys

sys.path.append('../')
from component_modules import autils

def check_number_length(char):
    # 匹配大于等于count个连在一起的数字
    pattern = r'\d{' + str(5) + ',}'  
    matches = re.findall(pattern, char)
    return len(matches) > 0

def match_yunshuzhenghao(pos, value, save_path):
    for i in range(len(pos)):
        if len(value[i]) > 6 and check_number_length(value[i]):
            a = re.findall("\d+\.?\d*", value[i])
            if len(a) > 0:
                return a[0]
        elif '字' in value[i] and value[i].split('字')[-1][4:6].isdigit():
            a = re.findall("\d+\.?\d*", value[i])
            return a[0]
        elif '交运' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            pos, result = autils.ReRec2(save_path,
                                 ymin - img_height,
                                 ymax + img_height,
                                 xmin,
                                 xmax + img_width * 5)
            result = ''.join(result)
            a = re.findall("\d+\.?\d*", result)
            if a is Empty:
                return 'null'
    else:
        return 'null'

def match_youxiaoqi(pos, value, save_path):
    if '长期' in value:
        return '长期'
    else:
        for i in range(len(pos)):
            if '有效期至' in value[i]:
                if len(value[i].split('有效期至')[-1])>5:
                    if '月' in value[i]:
                        return value[i].split('有效期至')[-1]
                    else:
                        date=[]
                        shr_pos = pos[i]
                        height = pos[i][3][1] - pos[i][0][1]
                        width = pos[i][1][0] - pos[i][0][0]
                        for i in range(len(pos)):
                            if shr_pos[1][0] - width / 2 < pos[i][0][
                                    0] < shr_pos[1][0] + int(4.5 * width) and shr_pos[1][1] - height < pos[i][
                                            0][1] < shr_pos[2][1] + 2*height:
                                date.append(value[i])
                                print(value[i])

                        return ''.join(date)
                else:
                    date=[]
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - width / 2 < pos[i][0][
                                0] < shr_pos[1][0] + int(4.5 * width) and shr_pos[1][1] - height < pos[i][
                                        0][1] < shr_pos[1][1] + 3*height:
                            date.append(value[i])

                    return ''.join(date)

            # case2 有效期开头，没有至
            elif '有效期' in value[i] and value[i].split('有效期')[-1][0]!='至':
                if len(value[i].split('有效期')[-1])>5:
                    if '至' in value[i] and value[i].split('至')[-1]!='':
                        return value[i].split('有效期')[-1]
                    elif '至' in value[i] and len(value[i].split('至')[-1])==0:
                        date=[]
                        shr_pos = pos[i]
                        height = pos[i][3][1] - pos[i][0][1]
                        width = pos[i][1][0] - pos[i][0][0]
                        for i in range(len(pos)):
                            if shr_pos[1][0] - width / 2 < pos[i][0][
                                    0] < shr_pos[1][0] + int(4.5 * width) and shr_pos[1][1] - height < pos[i][
                                            0][1] < shr_pos[2][1] + height:
                                date.append(value[i])

                        return ''.join(date)
                else:
                    date=[]
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - width / 2 < pos[i][0][
                                0] < shr_pos[1][0] + int(4.5 * width) and shr_pos[1][1] - height < pos[i][
                                        0][1] < shr_pos[1][1] + 3*height:
                            date.append(value[i])

                    return ''.join(date)

            # else:
            #     return 'null'


def match_yehumingcheng(pos, value, save_path):
    name = []
    for i in range(len(pos)):
        if '名称' in value[i]:
            if len(value[i].split('称')[-1]) > 3:
                return value[i].split('称')[-1]
            elif '名称' in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[1][1] - height < pos[i][
                                    0][1] < shr_pos[2][1] + height:
                        name.append(value[i])
                if len(name) > 0:
                    return "".join(name)
            else:
                ymin = pos[i][0][1]
                ymax = pos[i][2][1]
                xmin = pos[i][0][0]
                xmax = pos[i][2][0]
                pos, result = autils.ReRec2(save_path,
                                     ymin,
                                     ymax,
                                     xmin,
                                     xmax)
                result = ''.join(result)
                if '名称' in value[i]:
                    return result.split('称')[-1]
                else:
                    return value[i]
    else:
        return 'null'


def match_address(pos, value, save_path):
    address = []
    for i in range(len(pos)):
        if '副本' in value[i]:
            if '址' in value[i] and len(value[i].split('址')[-1]) > 3:
                return value[i].replace('址', '')
            elif '址' in value[i] or '地' in value[i]:
                print('aksjdh')
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                10 * width) and shr_pos[1][1] - height < pos[
                                    i][0][1] < shr_pos[2][1] + height * 3:
                        address.append(value[i])
                if len(address) > 0:
                    address= ''.join(address)
                    if '地' in address:
                        return address.replace('地','')
                    elif '址' in address:
                        return address.replace('址','')
                    else:
                        return address
                else:
                    return 'null'
        else:
            if '址' in value[i] and len(value[i].split('址')[-1]) > 3:
                return value[i].replace('址', '')
            elif '址' in value[i] or '地' in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                10 * width) and shr_pos[1][1] - height < pos[
                                    i][0][1] < shr_pos[2][1] + height * 3:
                        address.append(value[i])
                if len(address) > 0:
                    address= ''.join(address)
                    if '地' in address:
                        return address.replace('地','')
                    elif '址' in address:
                        return address.replace('址','')
                    else:
                        return address
                else:
                    return 'null'


def match_jingjixingzhi(pos, value, save_path):
    xingzhi=['国有','集体','股份','有限责任','联营','私营','个人独资','合伙企业','有限贵任']
    for i in range(len(pos)):
        for j in range(len(xingzhi)):
            if xingzhi[j] in value[i]:
                return value[i]
            else:
                for i in range(len(pos)):
                    if '经济性质' in value[i]:
                        if len(value[i].split('性质')[-1]) > 3:
                            return value[i].split('性质')[-1]
                        else:
                            shr_pos = pos[i]
                            height = pos[i][3][1] - pos[i][0][1]
                            width = pos[i][1][0] - pos[i][0][0]
                            for i in range(len(pos)):
                                if shr_pos[1][0] - width < pos[i][0][0] < shr_pos[1][0] + int(2 * width) and shr_pos[0][1] -height/2 < pos[i][0][1] < shr_pos[2][1] + height*1.2:
                                    if len(value[i])!=0:
                                        if '贵任' in value[i]:
                                            return value[i].replace('贵','责')
                                        else:
                                            return value[i]
                                    else:
                                        return 'null'


def match_jingyingfanwei(pos, value, save_path):
    a = []
    jingyingfanwei= ['经', '营', '范', '围']
    for i in range(len(pos)):
        if '范围' in value[i]:
            if len(value[i].split('围')[-1]) > 3:
                ymin = pos[i][0][1]
                ymax = pos[i][2][1]
                xmin = pos[i][0][0]
                xmax = pos[i][2][0]
                img_height = pos[i][3][1] - pos[i][0][1]
                img_width = pos[i][1][0] - pos[i][0][0]
                pos, result = autils.ReRec2(save_path,
                                    ymin - img_height,
                                    ymax + img_height*4,
                                    xmin,
                                    xmax + img_width * 3)
                result = ''.join(result)
                pattern = "[" + "".join(jingyingfanwei) + "]"
                result = re.sub(pattern, '', result)
                if len(result)>0:
                    return result
                else:
                    return 'null'


            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                            0] + int(2 * width) and shr_pos[2][1] - (
                                height - height /
                                2) < pos[i][3][1] < shr_pos[2][1] + height * 2:
                        a.append(value[i])
                if len(value[i]) > 0:
                    return ''.join(a)
        elif '范围' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            pos, result = autils.ReRec2(save_path,
                                 ymin - img_height,
                                 ymax + img_height,
                                 xmin,
                                 xmax + img_width * 3)
            result = ''.join(result)
            if '围' in result:
                return result.split('围')[-1]
            else:
                return result
    else:
        return 'null'