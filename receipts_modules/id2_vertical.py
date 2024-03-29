import re
import cv2
import sys

sys.path.append('../')
from component_modules import autils

jizhuangxiang_match = r'\b[A-Z\']{4}[0-9\']{7}\b'
date = "\d{4}[-]?\d{2}"


# -------------------------------------------------实现对规格的提取-------------------------------------------------
def get_star_before(s):
    s_nospace = s.replace(' ', '')

    pattern = r'\*(\d+)'  # 正则表达式
    match = re.search(pattern, s)  # 进行匹配
    if match:
        pos = match.start(1)  # 获取数字开始位置
        if pos is not None:
            return s[:pos]
        else:
            return s
    else:
        return s


def reverse_traversal(s):
    for i, c in reversed(list(enumerate(s))):
        if c.isdigit() and (i == 0 or not s[i - 1].isdigit()) and (
                c != '.' and c != '-' or i == len(s) - 1
                or not s[i + 1].isdigit()):
            return i
        elif not c.isdigit() and (i == 0 or s[i - 1].isdigit()) and (
                c != '.' and c != '-' or i == len(s) - 1
                or not s[i + 1].isdigit()):
            return i
    # 如果字符串为空或全是数字或全是非数字，则返回-1
    return -1


def get_result(chars: str):
    chars = chars.replace(' ', '')
    star_before = get_star_before(chars)
    # 定位到数字和非数字的索引位置
    s = reverse_traversal(star_before)
    if s != -1:
        number = reverse_traversal(star_before[:s])

    return star_before[number:]


# -------------------------------------------------实现对规格的提取-------------------------------------------------


def ReRec2(path, ymin, ymax, xmin, xmax, value):
    image = cv2.imread(path)
    cropImg = image[int(ymin):int(ymax), int(xmin):int(xmax)]
    pos, value = autils.detect_img(cropImg)
    return pos, value


def match_bianhao(pos, value, save_path):
    for i in range(len(pos)):
        if '编号' in value[i]:
            if len(value[i][2:]) > 5:
                m = re.search(r"\d", value[i])
                return value[i][int(m.start()):]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]

                for i in range(len(pos)):
                    if shr_pos[1][0] < pos[i][0][0] < shr_pos[0][0] + int(
                            3 * width
                    ) and shr_pos[0][1] - height < pos[i][0][1] < shr_pos[0][
                            1] + height and '编号' not in value[i]:
                        return value[i]
        elif '编号' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            pos, result = ReRec2(save_path,
                                 ymin - img_height,
                                 ymax + img_height * 1.5,
                                 xmin,
                                 xmax + img_width * 10,
                                 value='id2_bianhao')
            result = ''.join(result)
            if '编号' in result:
                return result.replace('编号', '')


def match_shouhuoren(pos, value, save_path):
    for i in range(len(pos)):
        if '收货人' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[1][0] < pos[i][0][0] < shr_pos[0][0] + int(
                        3 * width) and shr_pos[0][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[0][
                                1] + height and '收货人' not in value[i]:
                    return value[i]


def match_fahuoren(pos, value, save_path):
    for i in range(len(pos)):
        if '发货人' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[1][0] < pos[i][0][0] < shr_pos[0][0] + int(
                        3 * width) and shr_pos[0][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[2][
                                1] + height and '发货人' not in value[i]:
                    return value[i]


def match_pinming(pos, value, save_path):
    for i in range(len(pos)):
        if '品名' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] < pos[i][0][0] < shr_pos[1][0] + int(
                        3 * width) and shr_pos[0][1] - height < pos[i][0][
                            1] < shr_pos[2][1] + height:
                    return value[i]


def match_zhongliang(pos, value, save_path):
    for i in range(len(pos)):
        if '报检数' in value[i]:
            if len(value[i].split('报')[-1]) > 7:
                if '*' in value[i]:
                    return value[i].replace('*', '')
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] < pos[i][0][0] < shr_pos[1][0] + int(
                            3 * width) and shr_pos[0][1] - height < pos[i][0][
                                1] < shr_pos[2][1] + height:
                        if '*' in value[i]:
                            return value[i].replace('*', '')


def match_shuchuguojia(pos, value, save_path):
    for i in range(len(pos)):
        if '输出国家' in value[i] or '输出国家或地区' in value[i]:
            if len(value[i].split('家')[-1]) > 3:
                return value[i].split('家')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                5 * width) and shr_pos[0][1] - height < pos[i][
                                    0][1] < shr_pos[2][1] + height:
                        return value[i]


def match_jizhuangxiang(pos, value, save_path):
    result = []
    for i in range(len(pos)):
        a = re.findall(jizhuangxiang_match, value[i], re.S)
        if len(a) != 0:
            result.append(value[i])

    result = ''.join(result)

    if len(result) != 0:
        if '号' in result:
            return result.split('号')[-1]
        else:
            return result
    else:
        return 'None'


def match_shengchanriqi(pos, value, save_path):
    for i in range(len(pos)):
        if '生产日期' in value[i] or '生产口' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] < pos[i][1][
                        0] < shr_pos[1][0] + width * 2 and shr_pos[3][1] - int(
                            height / 3) < pos[i][0][1] < shr_pos[3][
                                1] + height + height / 2 and '-' in value[i]:
                    if '克' in value[i] or '于克' in value[i]:
                        return value[i].split('克')[-1]
                    elif '于' in value[i] and '克' not in value[i]:
                        return value[i].split('于')[-1][1:]
                    else:
                        return value[i]


def match_shengchanchangjia(pos, value, save_path):
    for i in range(len(pos)):
        if '生产厂家' in value[i] and len(value[i].split('家')[-1]) > 5:
            if '注册' in value[i]:
                value[i] = value[i].split('注册')[0]
                if len(value[i].split('家')[-1]) > 5 and '名称' in value[i]:
                    return value[i].split('称')[-1]
                elif '名称' not in value[i]:
                    return value[i].split('家')[-1]
            elif '注册' not in value[i]:
                value[i] = value[i]
                if len(value[i].split('家')[-1]) > 5 and '名称' in value[i]:
                    return value[i].split('称')[-1]
                elif '名称' not in value[i]:
                    return value[i].split('家')[-1]
            else:
                return value[i]
        elif '生产厂家' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][
                        0] < shr_pos[1][0] + width * 2 and shr_pos[0][1] - int(
                            height /
                            2) < pos[i][0][1] < shr_pos[0][1] + height:
                    return value[i]


def match_pinpai(pos, value, save_path):
    if '无品牌' in value:
        return '无品牌'
    else:
        for i in range(len(pos)):
            if '品牌' in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                            0] and shr_pos[3][1] - int(height / 2) < pos[i][0][
                                1] < shr_pos[3][1] + height:
                        if '*' in value[i]:
                            return 'None'
                        else:
                            return value[i]


def match_guige(pos, value, save_path):
    gj = match_shuchuguojia(pos, value, save_path)
    if '无规格' in value:
        return '无规格'
    else:
        result = []
        for i in range(len(pos)):

            if '证明' in value[i] and len(value[i]) == 2:
                print('here')
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width * 4 < pos[i][0][0] < shr_pos[1][
                            0] * 100 and shr_pos[3][1] + 1.5 * height < pos[i][
                                0][1] < shr_pos[3][1] + height * 3:
                        result.append(value[i])

            elif '集装箱号' in value[i]:
                print('jizhuangxiang')
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width * 4 < pos[i][0][
                            0] < shr_pos[1][0] * 100 and shr_pos[0][
                                1] - 2 * height < pos[i][3][1] < shr_pos[0][1]:
                        result.append(value[i])

        result = ''.join(result)
        print('规格的结果是：', result)
        if len(result) != 0:
            return get_result(result)


def match_hetonghao(pos, value, save_path):
    for i in range(len(pos)):
        if '合同号' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + int(2 * width) and shr_pos[0][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[3][1] + (
                                height + height / 2) and '合同' not in value[i]:
                    if len(value[i]) != 0:
                        if '*' in value[i]:
                            return 'None'
                        else:
                            return value[i]


def match_tiyundanhao(pos, value, save_path):
    for i in range(len(pos)):
        if '提/运单号' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + int(width) and shr_pos[0][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[3][
                                1] + height and '提/运单号' not in value[i]:
                    return value[i]


def match_rujingkouan(pos, value, save_path):
    for i in range(len(pos)):
        if '口岸' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + int(width) and shr_pos[0][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[3][
                                1] + height and '提/运单号' not in value[i]:
                    return value[i]


def match_rujingriqi(pos, value, save_path):
    for i in range(len(pos)):
        if '境日期' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + int(width) and shr_pos[0][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[3][
                                1] + height and '提/运单号' not in value[i]:
                    return value[i]


def match_biaoji(pos, value, save_path):
    for i in range(len(pos)):
        if '标记及号码' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[0][0] - width < pos[i][0][
                        0] < shr_pos[0][0] + width and shr_pos[3][1] - int(
                            height / 2) < pos[i][0][1] < shr_pos[3][1] + int(
                                height * 3) and '口岸' not in value[i]:
                    return value[i]


def match_baozhuangzhonglei(pos, value, save_path):
    for i in range(len(pos)):
        if '包装种类' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[0][
                        0] + width + width / 2 and shr_pos[1][1] - int(
                            height /
                            2) < pos[i][0][1] < shr_pos[2][1] + height / 3:
                    if '*' in value[i]:
                        return value[i].replace('*', '')


def match_beizhu(pos, value, save_path):
    for i in range(len(pos)):
        if '备注' in value[i]:
            if len(value[i].split('备注')[-1]) > 2:
                return value[i].split('备注')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[
                            1][0] + int(width) and shr_pos[0][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[3][1] + height * 2:
                        if '水' in value[i] or '冰' in value[i]:
                            return "None"
                        else:
                            return value[i]
    return 'None'