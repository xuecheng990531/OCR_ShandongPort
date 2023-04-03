import cv2
import sys

sys.path.append('../')
from component_modules import autils
from LAC import LAC

lac = LAC(mode='lac')

jiagedanwei = ["仟", "佰", "拾", "万", "仟", "佰", "拾","人民币","壹"]


def ReRec2(path, ymin, ymax, xmin, xmax, value):
    image = cv2.imread(path)
    cropImg = image[int(ymin):int(ymax), int(xmin):int(xmax)]
    pos, value = autils.detect_img(cropImg)
    return pos, value


def match_mingcheng(pos, value, save_path):
    for i in range(len(pos)):
        if '称' in value[i]:
            if len(value[i]) > 5:
                if '公' in value[i] and len(value[i].split('公')[-1]) == 0:
                    return value[i].split('称')[-1]+'司'
                else:
                    return value[i].split('称')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + int(2 * width) and shr_pos[1][
                        1] - height < pos[i][0][1] < shr_pos[1][1] + height:
                        if '公' in value[i] and len(value[i].split('公')[-1]) == 0:
                            return value[i] + '司'
                        else:
                            return value[i]
        elif '注册资本' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width * 2.5 < pos[i][1][0] < shr_pos[0][0] - width and shr_pos[0][1] - height < \
                        pos[i][0][1] < shr_pos[3][1] + height / 2:
                    if '公' in value[i] and len(value[i].split('公')[-1])==0:
                        return value[i]+'司'
                    else:
                        return value[i]


def match_daima(pos, value, save_path):
    for i in range(len(pos)):
        if '代码' in value[i] or '统一社会' in value[i]:
            if len(value[i].split('码')[-1]) > 10:
                return value[i].split('码')[-1]
            elif value[i + 1][2:7].isdigit():
                return value[i + 1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - int(width / 2) < pos[i][0][0] < shr_pos[0][0] + width and shr_pos[3][
                        1] - height / 2 < pos[i][0][1] < shr_pos[3][1] + height * 2:
                        return value[i]


def match_daima2(pos, value, save_path):
    result = match_daima(pos, value, save_path)
    if result is None:
        for i in range(len(pos)):
            if '代码' in value[i]:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - int(width / 4) < pos[i][0][0] < shr_pos[1][0] and shr_pos[0][1] < shr_pos[1][
                        1] + int(2 * height) and '一' not in value[i]:
                        return value[i]
    else:
        return result


def search(pos, value, save_path):
    for i in range(len(pos)):
        if '有限责任' in value[i] and '自' in value[i] and '（' in value[i]:
            return value[i]
        elif '股份有限责任' in value[i]:
            return value[i]
        elif '股份有限' in value[i] and '（' in value[i]:
            return value[i]
        elif '个人' in value[i]:
            return value[i]
        elif '合伙' in value[i]:
            return value[i]
        elif '个体工商户' in value[i]:
            return value[i]
        elif '有限责任公司' in value[i] and '(' not in value[i]:
            return '有限责任公司'


def match_leixing(pos, value, save_path):
    for i in range(len(pos)):
        if '类型' in value[i] or '型' in value[i]:
            if len(value[i].split('型')[-1]) > 2:
                return value[i].split('型')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + int(2 * width) and shr_pos[1][
                        1] - height / 2 < pos[i][0][1] < shr_pos[1][1] + height:
                        return value[i]
        else:
            result = search(pos, value, save_path)
            return result


def match_daibiaoren(pos, value, save_path):
    for i in range(len(pos)):
        user_name_lis = []
        if '负责' in value[i] or '代表' in value[i] or '法定' in value[i]:
            if len(value[i]) > 5:
                _result = lac.run(value[i])
                for _index, _label in enumerate(_result[1]):
                    if _label == "PER":
                        user_name_lis.append(_result[0][_index])
                if len(user_name_lis) != 0:
                    return user_name_lis[0]
                else:
                    if len(value[i].split('人')[-1]) != 0:
                        return value[i].split('人')[-1]
                    elif len(value[i].split('入')[-1]) != 0:
                        return value[i].split('入')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + width and shr_pos[1][
                        1] - height < pos[i][0][1] < shr_pos[1][1] + height:
                        return value[i]


def match_zhucechengben(pos, value, save_path):
    for i in range(len(pos)):
        for j in range(len(jiagedanwei)):
            if jiagedanwei[j] in value[i]:
                if '本' in value[i] and '元' in value[i] and len(value[i].split('本')[-1])>2:
                    return value[i].split('本')[-1]
                else:
                    return value[i]


def match_chengliriqi(pos, value, save_path):
    data = []
    for i in range(len(pos)):
        if '成立日期' in value[i]:
            if len(value[i].split('期')[-1]) > 3:
                return value[i].split('期')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + width * 10 and shr_pos[1][
                        1] - height < pos[i][0][1] < shr_pos[1][1] + height:
                        data.append(value[i])
                if len(data) > 0:
                    return ''.join(data)
        if '年' in value[i] and '月' in value[i] and '日' in value[i] and '至' not in value[i]:
            if '期' in value[i]:
                return value[i].split('期')[-1]
            else:
                return value[i]


def match_yingyeqixian(pos, value, save_path):
    for i in range(len(pos)):
        if '月' in value[i] and '日' in value[i] and '至' in value[i] and '主体' not in value[i]:
            if len(value[i].split('至')[-1]) > 4:
                return value[i].split('至')[-1]
            else:
                return '长期'
        elif '长期' in value[i]:
            return '长期'
        elif '永久' in value[i]:
            return '永久'
    else:
        return '长期'


def match_jingyingfanwei(pos, value, save_path):
    result = []
    for i in range(len(pos)):
        if '范' in value[i] and len(value[i]) == 1:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] < pos[i][0][0] < shr_pos[1][0] + 20 * width and shr_pos[0][
                    1] - height / 2 < pos[i][2][1] < shr_pos[3][1] + 8 * height:
                    result.append(value[i])
            result=''.join(result)
            if '围' in result and len(result.split('围')[0])==0:
                return result.replace('围', '')
            else:
                return result
        elif '经营' in value[i] or '范围' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][0] + 10 * width and shr_pos[0][
                    1] - height / 2 < pos[i][2][1] < shr_pos[3][1] + 8 * height:
                    result.append(value[i])
                result=''.join(result)
            if '围' in result and len(result.split('围')[0]) == 0:
                return result.replace('围', '')
            else:
                return result
