import re
import sys

sys.path.append('../')
from component_modules import autils

jizhuangxiang_match = r'\b[0-0A-Z\']{4}[0-9\']{7}\b'
date = "\d{4}[-]?\d{2}"

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
                    ) and shr_pos[0][1] - height * 2 < pos[i][0][1] < shr_pos[
                            3][1] + height * 1.5 and '编号' not in value[
                                i] and value[i].isdigit():
                        return value[i]
        elif '编号' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            pos, result = autils.ReRec2(save_path,
                                 ymin - img_height * 1.5,
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
    result = []
    for i in range(len(pos)):
        if '生产日期' in value[i]:
            if len(value[i].split('期')[-1]) > 6:
                m = re.search(r"\d", value[i])
                first = value[i][int(m.start()):]
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - int(width / 2) < pos[i][0][0] < shr_pos[
                            1][0] + width * 5 and shr_pos[0][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[3][
                                    1] + height and '生产' not in value[
                                        i] and '.' in value[i] and value[
                                            i].split('.')[0][-1].isdigit():
                        result.append(value[i])
                    return ''.join(result) + ' ' + first
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]

                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[
                            1][0] + width * 5 and shr_pos[0][1] - int(
                                height / 2) < pos[i][0][1] < shr_pos[2][
                                    1] + height and '生产' not in value[
                                        i] and '.' in value[i] and value[
                                            i].split('.')[0][-1].isdigit():
                        result.append(value[i])
                return ''.join(result)


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
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[
                            1][0] + width * 2 and shr_pos[0][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[0][1] + height:
                        return value[i]


def match_pinpai(pos, value, save_path):
    for i in range(len(pos)):
        if '品牌' in value[i] and len(value[i].split('牌')[-1]) > 2:
            if '原产' not in value[i]:
                return value[i].split('牌')[-1]
            elif '原产' in value[i]:
                return value[i].split('牌')[-1].split('原产')[0]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width / 4 < pos[i][0][0] < shr_pos[0][
                            0] + width / 5 and shr_pos[3][1] - int(
                                height /
                                2) < pos[i][0][1] < shr_pos[3][1] + height:
                        if '原产' not in value[i]:
                            return value[i].split('牌')[-1]
                        elif '原产' in value[i]:
                            return value[i].split('牌')[-1].split('原产')[0]


def match_guige(pos, value, save_path):
    for i in range(len(pos)):
        if '规格' in value[i]:
            if len(value[i].split('格')
                   [-1]) > 1 and '原产' not in value[i] and '数' not in value[i]:
                if '千克' in value[i]:
                    return value[i][3:].split('千克')[0] + '千克'
                elif '7' in value[i]:
                    return '/'
                else:
                    return value[i][3:]
        else:
            return '/'


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
