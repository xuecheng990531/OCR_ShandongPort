from queue import Empty
import re
import cv2
import sys

sys.path.append('../')
from component_modules import autils



def match_yunshuzhenghao(pos, value, save_path):
    for i in range(len(pos)):
        if len(value[i]) > 6:
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
                                 xmax + img_width * 5,
                                 value='id9_yunshuzhenghao')
            result = ''.join(result)
            a = re.findall("\d+\.?\d*", result)
            if a is Empty:
                return 'null'
    else:
        return 'null'


def match_youxiaoqi(pos, value, save_path):
    for i in range(len(pos)):
        if '至' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            height = img_height * 0.5  #默认不加高度
            width = img_width * 7  #默认不加宽度
            # pos,result=ReRec(save_path,ymin,ymax,xmin,xmax,height,width,value='youxiaoqi')
            pos, result = autils.ReRec2(save_path,
                                 ymin - img_height,
                                 ymax + height,
                                 xmin,
                                 xmax + width,
                                 value='id9_youxiaoqi')
            result = ''.join(result)
            if '至' in result:
                return result.split('至')[-1]
            else:
                return result

        elif '有效期' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            height = img_height * 0.5  #默认不加高度
            width = img_width * 5  #默认不加宽度
            # pos,result=ReRec(save_path,ymin,ymax,xmin,xmax,height,width,value='youxiaoqi')
            pos, result = autils.ReRec2(save_path,
                                 ymin - img_height,
                                 ymax + height,
                                 xmin,
                                 xmax + width,
                                 value='id9_youxiaoqi')
            # result=''.join(result)
            year = []
            for i in range(len(value)):
                if value[i].isdigit():
                    year.append(int(value[i]))
            if len(year) > 0:
                return str(max(year)) + '年'
            else:
                return '长期'
    else:
        return '长期'


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
                                     xmax,
                                     value='id9_yehumingcheng')
                result = ''.join(result)
                if '名称' in value[i]:
                    return result.split('称')[-1]
                else:
                    return value[i]
    else:
        return '无'


def match_address(pos, value, save_path):
    address = []
    for i in range(len(pos)):

        if '副本' in value[i]:
            if '址' in value[i] and len(value[i].split('址')[-1]) > 3:
                return value[i].replace('址', '')
            elif '址' in value[i] or '地' in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                5 * width) and shr_pos[1][1] - height < pos[i][
                                    0][1] < shr_pos[2][1] + height:
                        address.append(value[i])
                if len(address) > 0:
                    return ''.join(address)
            elif '址' in value[i]:
                ymin = pos[i][0][1]
                ymax = pos[i][2][1]
                xmin = pos[i][0][0]
                xmax = pos[i][2][0]
                img_height = pos[i][3][1] - pos[i][0][1]
                img_width = pos[i][1][0] - pos[i][0][0]
                height = img_height * 2  #默认不加高度
                width = img_width * 20  #默认不加宽度
                pos, result = autils.ReRec2(save_path,
                                     ymin - height / 3,
                                     ymax + height + img_height * 2,
                                     xmin,
                                     xmax + width,
                                     value='id9_address')
                result = ''.join(result)
                if '址' in result:
                    return result.split('址')[-1]
                else:
                    return result
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
                    return ''.join(address)
            elif '址' in value[i]:
                ymin = pos[i][0][1]
                ymax = pos[i][2][1]
                xmin = pos[i][0][0]
                xmax = pos[i][2][0]
                img_height = pos[i][3][1] - pos[i][0][1]
                img_width = pos[i][1][0] - pos[i][0][0]
                height = img_height * 2  #默认不加高度
                width = img_width * 20  #默认不加宽度
                pos, result = autils.ReRec2(save_path,
                                     ymin - height,
                                     ymax + height + img_height * 3,
                                     xmin,
                                     xmax + width,
                                     value='id9_address')
                result = ''.join(result)
                if '址' in result:
                    return result.split('址')[-1]
                else:
                    return result


def match_jingjixingzhi(pos, value, save_path):
    for i in range(len(pos)):
        if '经济性质' in value[i]:
            if len(value[i].split('质')[-1]) > 3:
                return value[i].split('质')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width < pos[i][0][0] < shr_pos[1][
                            0] + int(2 * width) and shr_pos[1][1] - (
                                height + height /
                                2) < pos[i][0][1] < shr_pos[2][1] + height / 2:
                        return value[i]
    else:
        return '无'


def match_jingyingfanwei(pos, value, save_path):
    a = []
    for i in range(len(pos)):
        if '范围' in value[i]:
            if len(value[i].split('围')[-1]) > 3:
                return value[i].split('围')[-1]
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
                                 xmax + img_width * 3,
                                 value='id9_jingyingfanwei')
            result = ''.join(result)
            if '围' in result:
                return result.split('围')[-1]
            else:
                return result
    else:
        return '无'