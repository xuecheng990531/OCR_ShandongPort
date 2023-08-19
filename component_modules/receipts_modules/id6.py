from LAC import LAC
import re

lac = LAC(mode="lac")
import sys

sys.path.append('../')
from component_modules import autils

zhunjia = ['A1', 'A2', 'A3', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4']
provinces = [
    "北京", "天津", "上海", "重庆", "新疆", "西藏", "宁夏", "内蒙古", "广西", "黑龙江", "吉林", "辽宁",
    "河北", "山东", "江苏", "安徽", "浙江", "福建", "广东", "海南", "云南", "贵州", "四川", "湖南",
    "湖北", "河南", "山西", "陕西", "甘肃", "青海", "江西", "台湾", "香港", "澳门"
]


def match_name(pos, value, save_path):
    for i in range(len(pos)):
        if '姓名' in value[i]:
            if len(value[i].split('名')[-1]) > 1:
                if '档案' in value[i]:
                    return value[i].split('名')[-1].split('档')[0]
                    break
                else:
                    return value[i].split('名')[-1]
                    break
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                            0] + int(2 * width) and shr_pos[0][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[3][
                                    1] and '姓名' not in value[
                                        i] and '档案编号' not in value[i]:
                        return value[i]
        elif '名' in value[i] and len(value[i].split('名')[0]) == 1:
            if len(value[i].split('名')[-1]) > 1:
                if '档案' in value[i]:
                    return value[i].split('名')[-1].split('档')[0]
                else:
                    return value[i].split('名')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                            0] + int(2 * width) and shr_pos[0][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[3][
                                    1] and '姓名' not in value[
                                        i] and '档案编号' not in value[i]:
                        return value[i]
        elif '姓' in value[i] and len(value[i].split('姓')[0])==0:
            if len(value[i].split('姓')[-1]) > 1:
                if '档案' in value[i]:
                    return value[i].split('姓')[-1].split('档')[0]
                else:
                    return value[i].split('姓')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                            0] + int(2 * width) and shr_pos[0][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[3][
                                    1] and '姓名' not in value[
                                        i] and '档案编号' not in value[i]:
                        return value[i]
    for i in range(len(pos)):
        if '中华人民共和国' in value[i] and '页' not in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] < pos[i][1][0] < shr_pos[1][
                        0] and shr_pos[3][1]+height*2 < pos[i][0][1] < shr_pos[3][
                                1]+height*2.5:
                                result = re.sub(r'[准住佳址牌Addressi]*', '', value[i])
                                print(result)
                                return result


def match_sex(pos, value, save_path):
    for i in range(len(pos)):
        if '性别' in value[i]:
            if len(value[i].split('别')[-1]) >= 1:
                if '男' in value[i]:
                    return '男'
                else:
                    return '女'
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[0][1] - height < pos[i][
                                    0][1] < shr_pos[3][1] + height:
                        if '男' in value[i]:
                            return '男'
                        else:
                            return '女'
        elif 'Sex' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][
                        0] < shr_pos[1][0] + int(
                            2 * width) and shr_pos[0][1] - 1.5 * height < pos[
                                i][0][1] < shr_pos[3][1] + height:
                    if '男' in value[i]:
                        return '男'
                    else:
                        return '女'
        else:
            return '男'


def match_jiashizhenghao(pos, value, save_path):
    for i in range(len(pos)):
        if '证号' in value[i]:
            if len(value[i].split('号')[-1]) > 2:
                id = value[i].split('号')[-1]
                return id
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                            0] + int(2 * width) and shr_pos[1][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[3][1]:
                        return value[i]
        else:
            if len(value[i]) > 10 and value[i][2:5].isdigit():
                if '号' in value[i]:
                    return value[i].split('号')[-1]
                else:
                    return value[i]

def match_address(pos, value, save_path):
    address=[]
    for i in range(len(pos)):
        if '公司' not in value[i]:
            if '省' in value[i] or '县' in value[i] or '市' in value[i] or '区' in value[i] and '局' not in value[i]:
                address.append(value[i])
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-width/4 < pos[i][0][0] < shr_pos[1][
                            0] and shr_pos[2][1]-height/2 < pos[i][0][1] < shr_pos[
                                2][1] + height and '类型' not in value[i] and '牌' not in value[i] and '使用' not in value[i]:
                        address.append(value[i])
                
                result=''.join(address)
                result = re.sub(r'[准住佳址牌Addressi]*', '', result)
                return result


def match_chexing(pos, value, save_path):
    for i in range(len(pos)):
        if value[i] in zhunjia:
            return value[i]
        elif '准驾' in value[i]:
            if (re.search(r'\d', value[i])):
                num_list = [i for i in value[i] if str.isdigit(i)]
                return value[i][int(num_list[0]):]
            else:
                zj_pos = pos[i]
                for i in range(len(pos)):
                    if zj_pos[1][0] < pos[i][0][0] < zj_pos[1][
                            0] + 100 and zj_pos[1][1] - 10 < pos[i][0][
                                1] < zj_pos[2][1] + 10:
                        return value[i]
    else:
        return 'A2'


def match_valid_date(pos, value, save_path):
    for i in range(len(pos)):

        if '年' in value[i] and len(value[i].split('年')[-1])==0 and value[i].split('年')[0][-1].isdigit() and len(value[i])==3:
            return value[i]

        elif '至' in value[i]:
            if '长期' not in value[i]:
                if '实习' not in value[i]:
                    if value[i].split('至')[-1][1:2].isdigit():
                        # return value[i].split('至')[-1]
                        if '限' in value[i]:
                            result= value[i].split('限')[-1]
                        else:
                            result= value[i]
                        return result
            else:
                return '长期'

        elif '有效期' in value[i]:
            if len(value[i].split('有效期')[-1])>2:
                numbers = re.findall(r'\d+', value[i])
                if numbers:
                    return str(numbers[0])+'年'
                else:
                    return value[i]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-width/2 < pos[i][0][0] < shr_pos[1][
                            0]+width*2 and shr_pos[0][1]-height/2 < pos[i][0][1] < shr_pos[
                                3][1]:
                                numbers = re.findall(r'\d+', value[i])
                                if numbers:
                                    return str(numbers[0])+'年'
                                else:
                                    return value[i]
