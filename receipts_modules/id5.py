import re
import regex as reg
from LAC import LAC
import cv2
import sys

sys.path.append('../')
from component_modules import autils


lac = LAC(mode='lac')
VIN = '^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$'
Engine_no = '^(?![0-9]+)(?![A-Z]+)[0-9A-Z]{7,10}$'
date = '^((([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29))\\s+([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
province = [
    '京', '沪', '津', '渝', '鲁', '冀', '晋', '蒙', '辽', '吉', '黑', '苏', '浙', '皖', '闽',
    '赣', '豫', '湘', '鄂', '粤', '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁',
    '新', '港', '澳', '台'
]


def match_haoma(pos, value, save_path):
    for i in range(len(pos)):
        match = re.search(
            r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]{1}[A-HJ-NP-Z]([0-9ABCDEFGHJKLMNPQRSTUVWXYZ]{5})',
            value[i])
        if match:
            return match.group()

        elif value[i][0] in province:
            return value[i]
        elif '码' in value[i]:
            if len(value[i].split('码')[-1]) > 0:
                return value[i].split('码')[-1]
            else:
                match = re.search(
                    r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]{1}[A-HJ-NP-Z]([0-9ABCDEFGHJKLMNPQRSTUVWXYZ]{5})',
                    value[i])
                if match:
                    return match.group()


def match_cheliangleixing(pos, value, save_path):
    for i in range(len(pos)):
        if '车辆类型' in value[i] or '车钢类型' in value[i] and '车辆奥型' in value[i] and len(value[i])>4:
            if len(value[i])>4:
                if '类型' in value[i]:
                    return value[i].split('类型')[-1]
                elif '奥型' in value[i]:
                    return value[i].split('奥型')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][0] + width and shr_pos[1][1] - int(height /2) < pos[i][0][1] < shr_pos[1][1] + height:
                        if '重型' in value[i]:
                            return '重型半挂牵引车'
                        else:
                            return value[i]

        elif 'Vehicle Type' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                        0] + width * 2 and shr_pos[1][1] - height * 4 < pos[i][
                            0][1] < shr_pos[1][1] + height:
                    if '重型' in value[i]:
                        return '重型半挂牵引车'
                    else:
                        return value[i]
        elif '重型' and '半挂' in value[i]:
            return '重型半挂牵引车'
        elif '重型' in value[i] and '车' in value[i]:
            return '重型半挂牵引车'


def match_suoyouren(pos, value, save_path):
    for i in range(len(pos)):
        if '所有人' in value[i] or '有人' in value[i]:
            if len(value[i].split('人')[-1]) > 1:
                return value[i].split('人')[-1]
        if '所' in value[i] and '人' in value[i]:
            if len(value[i].split('人')[-1]) > 1:
                return value[i].split('人')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[
                            1][0] + width and shr_pos[1][1] - height / 2 < pos[
                                i][0][1] < shr_pos[2][
                                    1] + height / 2 and 'Type' not in value[i]:
                        return value[i]

        if '中华人民共和国' in value[i]:
            name = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - int(
                        width / 6) < pos[i][0][0] < shr_pos[1][0] + int(
                            width / 6) and shr_pos[3][1] + 2.3 * height < pos[
                                i][0][1] < shr_pos[3][1] + int(height * 2.5):
                    return value[i]
        if '有限公司' in value[i]:
            return value[i]


def match_address(pos, value, save_path):
    address=[]
    syxz=match_shiyongxingzhi(pos,value,save_path)
    if syxz in value:
        for i in range(len(pos)):
            if str(syxz) in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-width/2 < pos[i][0][0] < shr_pos[1][
                            0] and shr_pos[0][1]-height*2 < pos[i][2][1] < shr_pos[
                                0][1] +height/2:
                        address.append(value[i])
                result=''.join(address)
                result = re.sub(r'[住佳址牌]*', '', result)
                return result
    else:
        for i in range(len(pos)):
            if '公司' not in value[i]:
                if '省' in value[i] or '县' in value[i] or '市' in value[i] or '区' in value[i] and '局' not in value[i]:
                    address.append(value[i])
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[0][0] < pos[i][1][0] < shr_pos[1][
                                0] and shr_pos[2][1]-height/2 < pos[i][0][1] < shr_pos[
                                    2][1] + height/2 and '类型' not in value[i] and '牌' not in value[i] and '使用' not in value[i]:
                            address.append(value[i])
                    
                    result=''.join(address)
                    result = re.sub(r'[住佳址牌]*', '', result)
                    xingzhi=match_shiyongxingzhi(pos,value,save_path)
                    if str(xingzhi) in result:
                        return result.replace(str(xingzhi),'')
                    else:
                        return result


def match_shiyongxingzhi(pos, value, save_path):
    for i in range(len(pos)):
        if '危化品' in value[i]:
            return '危化品运输'
        else:
            for i in range(len(pos)):
                if '性质' in value[i]:
                    if len(value[i].split('质')[-1]) > 1:
                        return value[i].split('质')[-1]
                    else:
                        shr_pos = pos[i]
                        height = pos[i][3][1] - pos[i][0][1]
                        width = pos[i][1][0] - pos[i][0][0]
                        for i in range(len(pos)):
                            if shr_pos[1][0] - int(width / 2) < pos[i][0][
                                    0] < shr_pos[1][0] + width and shr_pos[1][1] - int(
                                        height / 2
                                    ) < pos[i][0][1] < shr_pos[1][1] + int(height / 2):
                                if '危化' in value[i]:
                                    return '危化品运输'
                                elif '营运' in value[i]:
                                    return '营运'
                                elif '货运' in value[i]:
                                    return '货运'
                                else:
                                    return '货运'
                                            
                if '品牌型号' in value[i]:
                    ymin = pos[i][0][1]
                    ymax = pos[i][2][1]
                    xmin = pos[i][0][0]
                    xmax = pos[i][2][0]
                    img_height = pos[i][3][1] - pos[i][0][1]
                    img_width = pos[i][1][0] - pos[i][0][0]
                    pos, result = autils.ReRec2(save_path,
                                        ymin - img_height,
                                        ymax + img_height * 2,
                                        xmin - img_width * 2,
                                        xmax)
                    result = ''.join(result)
                    if '非' in result:
                        return '非' + result.split('非')[-1][:2]
                    elif '韭' in result:
                        return '非' + result.split('韭')[-1][:2]
                    elif '生' in result:
                        return '非' + result.split('生')[-1][:2]
                    elif '营运' in result:
                        return '营运'
                    elif '货运' in result:
                        return '货运'
                    elif '危化' in result:
                        return '危化品运输'
                    else:
                        return '货运'
                if '货运' in value[i]:
                    return '货运'


def match_pinpaixinghao(pos, value, save_path):

    for i in range(len(pos)):
        if '品牌' in value[i] and '号' in value[i]:
            if len(value[i].split('号')[-1]) > 5:
                return value[i].split('号')[-1]
        elif '牌' in value[i] and re.match('[0-9A-Z]', value[i].split('牌')
        [-1]) and len(value[i].split('牌')[-1])>5:
            return value[i]
        else:
            VIN=match_cheliangshibiedaihao(pos,value,save_path)
            if VIN and str(VIN)!='None':
                for i in range(len(pos)):
                    if str(VIN) in value[i]:
                        shr_pos = pos[i]
                        height = pos[i][3][1] - pos[i][0][1]
                        width = pos[i][1][0] - pos[i][0][0]
                        for i in range(len(pos)):
                            if shr_pos[1][0] - int(width / 2) < pos[i][1][
                                    0] < shr_pos[1][0] + width/4 and shr_pos[1][1]-height-height/2< pos[i][2][1] < shr_pos[1][1] + height/2 and '牌' in value[i]:
                                if '号' in value[i]:
                                    return value[i].split('号')[-1]
                                else:
                                    return value[i]



def VIN(pos, value):
    for i in range(len(pos)):
        text = value[i]
        pattern = re.compile(r'\b([A-HJ-NPR-Z\d]{17})\b')
        result = pattern.search(text)
        if result:
            vin1 = result.group()
            return vin1


def match_cheliangshibiedaihao(pos, value, save_path):
    vinnumber = VIN(pos, value)
    if vinnumber is not None:
        return vinnumber
    else:
        for i in range(len(pos)):
            if '识别' in value[i] and '代号' in value[i]:
                if '类' not in value[i]:
                    if len(value[i].split('号')[-1]) > 5:
                        return value[i].split('号')[-1]
                    else:
                        shr_pos = pos[i]
                        height = pos[i][3][1] - pos[i][0][1]
                        width = pos[i][1][0] - pos[i][0][0]
                        for i in range(len(pos)):
                            if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + width * 2 and shr_pos[0][1] - int(height / 2) < pos[i][0][1] < shr_pos[1][1] + int(height +height / 2) and len(value[i]) > 10:
                                return value[i]
            if '车辆' in value[i] and '代号' in value[i]:
                if len(value[i].split('代号')[-1])>5:
                    return value[i].split('代号')[-1]
                else:
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + width and shr_pos[0][1] - int(height / 2) < pos[i][0][1] < shr_pos[1][1] +height/2 and len(value[i]) > 5:
                            return value[i]
            
            if '辆' in value[i] and '代号' in value[i]:
                if len(value[i].split('代号')[-1])>5:
                    return value[i].split('代号')[-1]
                else:
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + width and shr_pos[0][1] - int(height / 2) < pos[i][0][1] < shr_pos[1][1] +height/2 and len(value[i]) > 5:
                            return value[i]
            else:
                return 'None'


def EN(pos, value):
    for i in range(len(pos)):
        text = value[i]
        pattern = reg.compile(r'\b(?!\p{Han}|[A-Za-z]+\b)[A-Za-z0-9]{6,12}\b')
        result = pattern.search(text)
        if result:
            engine_number = result.group()
            return engine_number


def match_fadongjihaoma(pos, value, save_path):
    for i in range(len(pos)):
        if '发动机' in value[i] and '码' in value[i]:  
            if len(value[i].split('码')[-1]) > 5:
                return value[i].split('码')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][
                            0] < shr_pos[1][0] + width and shr_pos[1][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[2][1] + height:
                        return value[i]
                    
        if '发' in value[i] and '号码' in value[i]:
            if len(value[i].split('码')[-1]) > 5:
                return value[i].split('码')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][
                            0] < shr_pos[1][0] + width and shr_pos[1][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[2][1] + height:
                        return value[i]
        
        if '机号码' in value[i]:
            if len(value[i].split('码')[-1]) > 5:
                return value[i].split('码')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][
                            0] < shr_pos[1][0] + width and shr_pos[1][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[2][1] + height:
                        return value[i]

        if '发证日期' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] < pos[i][1][0] < shr_pos[1][
                        0] + width * 3 and shr_pos[1][1] - height * 2 < pos[i][
                            3][1] < shr_pos[0][1]:
                    pattern = re.compile(r"^[A-Za-z0-9]{6,12}$")
                    result = pattern.match(value[i])
                    if result:
                        return result.group()
        
        else:
            VIN=match_cheliangshibiedaihao(pos, value,save_path)
            for i in range(len(pos)):
                if str(VIN) in value[i] and str(VIN) is not None:
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[0][0] < pos[i][1][0] < shr_pos[1][
                                0] and shr_pos[2][1]-height/2 < pos[i][
                                    1][1] < shr_pos[2][1]+height+height/2 and value[i][0].isdigit():
                            return value[i]



def match_zhucedate(pos, value, save_path):
    for i in range(len(pos)):
        if '注册日' in value[i] or '注册口' in value[i] or '册日期' in value[
                i] or '注册旧' in value[i]:
            if len(value[i].split('册')[-1]) > 7:
                if '发' in value[i].split('册')[-1]:
                    result = value[i].split('册')[-1].split('发')[0]
                    match = re.search(r'\d{4}-\d{1,2}-\d{1,2}', result)
                    return match.group()
                else:
                    result = value[i].split('册')[-1]
                    match = re.search(r'\d{4}-\d{1,2}-\d{1,2}', result)
                    if match:
                        return match.group()
            else:
                result = []
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][
                            0] < shr_pos[1][0] + width and shr_pos[1][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[2][
                                    1] + height and '-' in value[i]:
                        result.append(value[i])
                if len(result) != 0:
                    for i in range(len(result)):
                        if '-' in result[i] and result[i].split(
                                '-')[0][-1].isdigit():
                            if '发证' in result[i]:
                                return result[i].split('发证')[0]
                            else:
                                return result[i]
        else:
            result = []
            if '支队' in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[
                            1][0] + width * 4 and shr_pos[1][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[2][1] + height:
                        result.append(value[i])
                if len(result) != 0:
                    result_new = ''.join(result)
                    match = re.search(r'\d{4}-\d{1,2}-\d{1,2}', result_new)
                    if match:
                        return match.group()

            # if '-' in value[i] and value[i].split('-')[0][-1].isdigit():
            #     match=re.search(r'\d{4}-\d{1,2}-\d{1,2}',value[i])
            #     if match:
            #         return match.group()


def match_zairenshu(pos, value, save_path):
    for i in range(len(value)):
        if '人数' in value[i] and '人' in value[i].split('人数')[-1] and value[i].split('人数')[-1][0].isdigit():
            return value[i].split('人数')[-1]
        elif '核定' in value[i] and '质量' not in value[i] and '人' in value[i]:
            if '人' in value[i]:
                a = re.findall("\d+\.?\d*", value[i])
                a = list(map(int, a))
                return str(a).replace('[', '').replace(']', '') + '人'
            elif '入' in value[i]:
                a = re.findall("\d+\.?\d*", value[i])
                a = list(map(int, a))
                return str(a).replace('[', '').replace(']', '') + '人'
        elif '人' in value[i] or '入' in value[i]:
            if value[i].split('人')[0].isdigit():
                return value[i].split('人')[0] + '人'
    else:
        return '0'


def match_weight_sum(pos, value, save_path):
    for i in range(len(value)):
        if '总质量' in value[i] or '总质' in value[i] or '总' in value[i]:
            if len(value[i]) > 3:
                result = "".join(list(filter(str.isdigit, value[i])))
                if len(result) != 0:
                    return result + 'kg'

            elif '牵引' not in value[i] and '准' not in value[i]:
                if len(value[i]) > 5:
                    result = "".join(list(filter(str.isdigit, value[i])))
                    if len(result) != 0:
                        return result + 'kg'
                else:
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - int(width / 2) < pos[i][0][
                                0] < shr_pos[1][0] + int(
                                    3 * width) and shr_pos[1][1] - int(
                                        2 * height
                                    ) < pos[i][0][1] < shr_pos[1][1] + height:
                            return value[i]
        elif '核定载质量' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][
                        0] < shr_pos[1][0] + 2 * width and shr_pos[1][1] - int(
                            4.4 * height) < pos[i][0][1] < shr_pos[1][1]:
                    return value[i]


def match_weight_zhengbei(pos, value, save_path):
    for i in range(len(value)):
        if '整备' in value[i] or '备质量' in value[i] or '备至' in value[
                i] or '服备' in value[
                    i] or '务质量' in value[i] and '人' not in value[i]:
            if 'kg' in value[i]:
                result = "".join(list(filter(str.isdigit, value[i])))
                return result + 'kg'
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[1][1] - int(
                                    height *
                                    2) < pos[i][0][1] < shr_pos[1][1] + height:
                        result = "".join(list(filter(str.isdigit, value[i])))
                        return result + 'kg'
        elif '核定' in value[i] and '载' in value[i] and '人' not in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width * 7 < pos[i][0][
                        0] < shr_pos[0][0] - width and shr_pos[1][1] - int(
                            2 * height) < pos[i][0][1] < shr_pos[1][
                                1] + height and '人' not in value[i]:
                    result = "".join(list(filter(str.isdigit, value[i])))
                    return result + 'kg'
    else:
        return '0'


def match_weight_heding(pos, value, save_path):
    for i in range(len(value)):
        if '核定' in value[i] and '人' not in value[i] and '入' not in value[
                i] and '量' in value[i]:
            if len(value[i].split('量')[-1]) != 0:
                return value[i].split('量')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                3 * width) and shr_pos[1][1] - int(
                                    2 * height) < pos[i][0][1] < shr_pos[2][1]:
                        result = "".join(list(filter(str.isdigit, value[i])))
                        return result + 'kg'
        elif '核定载质量' in value[i] or '核定线质量' in value[i]:
            if len(value[i].split('量')[-1]) != 0:
                return value[i].split('量')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                3 * width) and shr_pos[1][1] - int(
                                    2 * height) < pos[i][0][1] < shr_pos[2][1]:
                        result = "".join(list(filter(str.isdigit, value[i])))
                        return result + 'kg'


def match_weight_qianyin(pos, value, save_path):

    for i in range(len(value)):
        if '准' in value[i] and '质量' in value[i]:
            if len(value[i].split('质量')[-1]) > 3:
                return value[i]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] < pos[i][0][0] < shr_pos[1][
                            0] + width * 4 and shr_pos[1][1] - height < pos[i][
                                2][1] < shr_pos[2][1] + height and value[i][
                                    0].isdigit():
                        return value[i]
        elif '准' in value[i] and '总' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] < pos[i][0][0] < shr_pos[1][
                        0] + width * 4 and shr_pos[1][1] - height < pos[i][2][
                            1] < shr_pos[2][1] + height and value[i][
                                0].isdigit():
                    return value[i]

        elif '尺寸' in value[i] or '尺' in value[i]:
            chicun = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            if len(value[i]) < 6:
                for i in range(len(pos)):
                    if shr_pos[1][0] + width * 5 < pos[i][0][
                            0] < shr_pos[1][0] + width * 40 and shr_pos[1][
                                1] - height * 2.2 < pos[i][0][1] < shr_pos[2][
                                    1] + height / 2 and value[i][0].isdigit():
                        chicun.append(value[i])
                if len(chicun) > 0:
                    for i in range(len(chicun)):
                        if 'kg' in chicun[i]:
                            return chicun[i]

        elif '核定载质量' in value[i]:
            if len(value[i].split('量')[-1]) != 0:
                return value[i].split('量')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                3 * width
                            ) and shr_pos[1][1] + height < pos[i][0][
                                1] < shr_pos[2][1] + height * 1.5 and value[i][
                                    2].isdigit():
                        result = "".join(list(filter(str.isdigit, value[i])))
                        return result + 'kg'


def match_chicun(pos, value, save_path):
    for i in range(len(value)):
        if '外' in value[i]:
            if len(value[i]) > 10:
                s = autils.separate_digits_and_chinese_chars(value[i])
                return s
                # if '寸' in value[i]:
                #     return value[i].split('寸')[-1].split('m')[0]+'mm'
                # else:
                #     return value[i].split('m')[0]+'mm'
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[1][1] - height < pos[i][
                                    0][1] < shr_pos[1][1] + height:
                        if 'mm' in value[i]:
                            if '寸' in value[i]:
                                return value[i].split('寸')[-1].split(
                                    'm')[0] + 'mm'
                            else:
                                return value[i].split('m')[0] + 'mm'
        elif 'mm' in value[i] or 'x' in value[i]:
            if '寸' in value[i]:
                return value[i].split('寸')[-1].split('m')[0] + 'mm'
            else:
                return value[i].split('m')[0] + 'mm'
    else:
        return 'None'


def match_valid_date(pos, value, save_path):
    for i in range(len(value)):
        if '有效期' in value[i]:
            if '至' in value[i]:
                if '月' in value[i] and '年' in value[i]:
                    if int(value[i].split('年')[-1][0])>1:
                        print(value[i])
                        s=value[i].split('至')[-1].replace(value[i].split('年')[-1][0],'0')
                        s=s.split('月')[0]+'月'
                        return s
                    else:
                        return value[i].split('至')[1].split('月')[0] + '月'
                else:
                    return value[i].split('至')[1]
            elif '室' in value[i] and value[i].split('室')[-1][0].isdigit():
                if '月' in value[i]:
                    return value[i].split('室')[1].split('月')[0] + '月'
                else:
                    return value[i].split('室')[-1]
    else:
        return 'None'
