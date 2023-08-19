import re

jingyingfanwei = ['货运', '客运', '国际运输', '站场', '机动车维修', '机动车驾驶员培训']
chepai = r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁台琼使领军北南成广沈济空海]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂领学警港澳]{1}(?!\d)'
province = [
    '京', '沪', '津', '渝', '鲁', '冀', '晋', '蒙', '辽', '吉', '黑', '苏', '浙', '皖', '闽',
    '赣', '豫', '湘', '鄂', '粤', '桂', '琼', '川', '贵', '云', '藏', '陕', '甘', '青', '宁',
    '新', '港', '澳', '台'
]
id_zhengze = r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'

jingjileixing = ['个体', '有限责任公司', '其他有限责任', '有限责任']


#-------------------------------------------------检查字符串中数字的长度-------------------------------------
def check_length(str):
    count = 0
    for i in range(len(str)):
        if str[i].isdigit():
            count += 1
        else:
            i += 1
    return count


#-------------------------------------------------检查字符串中数字的长度-------------------------------------
def match_zhenghao(pos, value, save_path):
    rot = []
    for i in range(len(pos)):
        if "中华人民共和国道路运输证" in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - int(
                        width / 2) < pos[i][0][0] < shr_pos[1][0] and shr_pos[
                            0][1] < pos[i][0][1] < shr_pos[3][1] + height * 5:
                    rot.append(value[i])
            if len(rot) != 0:
                text = ''.join(rot)
                number = ''.join(re.findall(r"\d+\.?\d*", text))
                return number
        elif '交运管' in value[i]:
            rot = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + width * 5 and shr_pos[0][1] - height / 2 < pos[i][
                            0][1] < shr_pos[2][1]:
                    rot.append(value[i])
            if len(rot) != 0:
                text = ''.join(rot)
                number = ''.join(re.findall(r"\d+\.?\d*", text))
                return number


def match_yehumingcheng(pos, value, save_path):
    for i in range(len(pos)):
        if '户名称' in value[i] or '名称' in value[i] or '称' in value[
                i] or ' 称' in value[i]:
            if len(value[i].split('称')[-1]) > 1:
                return value[i].split('称')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                width /
                                2) and shr_pos[1][1] - height * 1.4 < pos[i][
                                    0][1] < shr_pos[2][1] + height / 2:
                        return value[i]
        elif '业户名' in value[i]:
            result = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + 100 and shr_pos[1][1] - height * 0.6 < pos[i][0][
                            1] < shr_pos[2][
                                1] + height / 2 and '类' not in value[
                                    i] and '车架' not in value[i]:
                    result.append(value[i])
            if len(result) != 0:
                if '名称' in result:
                    return ''.join(result).split('名称')[-1]
                else:
                    return ''.join(result).split('名')[-1]


def match_dizhi(pos, value, save_path):
    address = []
    for i in range(len(pos)):
        if '址' in value[i]:
            if len(value[i].split('址')[-1]) > 3:
                return value[i].split('址')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + width * 5 and shr_pos[1][
                                1] - height * 2.4 < pos[i][0][
                                    1] < shr_pos[2][1] + height:
                        address.append(value[i])
                if len(address) > 0:
                    return ''.join(address)
        elif '业户名称' in value[i]:
            address = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                        0] + width * 2 and shr_pos[2][1] + height < pos[i][0][
                            1] < shr_pos[2][1] + height * 3.5:
                    if '色' not in value[i] or '黄' not in value[i]:
                        address.append(value[i])
            if len(address) != 0:
                return ''.join(address)
        if '号牌' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] < pos[i][0][0] < shr_pos[1][
                        0] + width * 2 and shr_pos[1][1] - height * 5 < pos[i][
                            1][1] < shr_pos[1][1] - height * 1.3 and len(
                                value[i]) > 4:
                    if '黄' not in value[i] or '色' not in value[i]:
                        address.append(value[i])
            if len(address) != 0:
                return ''.join(address)


def match_chepaihaoma(pos, value, save_path):
    for i in range(len(pos)):
        if '黄色' in value[i] and value[i].split("黄")[0][-1].isdigit():
            if '牌' in value[i]:
                if '：' in value[i]:
                    return value[i].split('：')[-1]
                else:
                    return value[i].split('牌')[-1]
            else:
                return value[i]
        elif '号牌' in value[i] or '牌' in value[i]:
            if len(value[i].split('牌')[-1]) > 3:
                if '：' in value[i]:
                    return value[i].split('：')[-1]
                else:
                    return value[i].split('牌')[-1]
            else:
                rot = []
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                width * 2) and shr_pos[1][1] - height < pos[i][
                                    0][1] < shr_pos[2][1] + int(height / 2):
                        rot.append(value[i])

                if len(rot) != 0:
                    for i in range(len(rot)):
                        if '色' in rot[i] or '颜色' in rot[i]:
                            return rot[i]
                        else:
                            for j in range(len(province)):
                                if province[j] in rot[i]:
                                    return rot[i]


def match_jingyingxukezheng(pos, value, save_path):
    rot = []
    number = []
    for i in range(len(pos)):
        if '许可证号' in value[i]:
            if len(value[i].split('号')[-1]) > 3 and value[i].split(
                    '号')[-1][2:4].isdigit():
                return value[i].split('号')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0] - width / 2 < pos[i][1][
                            0] < shr_pos[0][0] + int(
                                width / 2 +
                                width) and shr_pos[1][1] - height * 2.5 < pos[
                                    i][0][1] < shr_pos[2][1] + int(
                                        height / 2) and '-' not in value[i]:
                        rot.append(value[i])
                if len(rot) != 0:
                    rot = ''.join(rot)
                    number = re.findall("\d+", rot)
                    if len(number) != 0:
                        for i in range(len(number)):
                            if len(number[i]) > 6:
                                return number[i]
        elif '号' in value[i] and value[i].split(
                '号')[-1][:4].isdigit() and '发动' not in value[i]:
            return value[i].split('号')[-1]
        elif '盘字' in value[i]:
            return value[i].split('盘字')[-1]
        elif '字' in value[i] and value[i].split('字')[-1][-1].isdigit():
            return value[i].split('字')[-1]


def match_jingyingleixing(pos, value, save_path):
    for i in range(len(pos)):
        result = match_jingyingleixing_single(pos, value, save_path)
        if result is None:
            if '经济类型' in value[i]:
                if len(value[i]) > 5:
                    return value[i].split('类型')[-1]
                else:
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[
                                1][0] + width and shr_pos[1][1] - height < pos[
                                    i][0][1] < shr_pos[2][1] + int(height / 2):
                            return value[i]
            elif '经济费型' in value[i]:
                if len(value[i]) > 5:
                    return value[i].split('类型')[-1]
                else:
                    shr_pos = pos[i]
                    height = pos[i][3][1] - pos[i][0][1]
                    width = pos[i][1][0] - pos[i][0][0]
                    for i in range(len(pos)):
                        if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[
                                1][0] + width and shr_pos[1][1] - height < pos[
                                    i][0][1] < shr_pos[2][1] + int(height / 2):
                            return value[i]
        else:
            return result


def match_jingyingleixing_single(pos, value, save_path):
    for i in range(len(pos)):
        if '有限责任' in value[i] and '（' in value[i] and '公司' not in value[i]:
            return '有限' + value[i].split('有限')[-1]
        elif '无限公司' in value[i]:
            return '无限' + value[i].split('限')[-1]
        elif '股份有限' in value[i]:
            return value[i]
        elif '股份两合' in value[i]:
            return value[i]
        elif '个体' in value[i] or '企体' in value[i]:
            return '个体'
        elif '普通' in value[i]:
            return '普通货运'
        elif '普' in value[i] and '货运' in value[i]:
            return '普通货运'
        elif '道路货物' in value[i]:
            return '道路' + str(value[i].split('道路')[-1])
        elif '有限责任' in value[i] and '公司' in value[i]:
            return '有限' + str(value[i].split('有限')[-1])
        elif '其他有限' in value[i]:
            return '其他' + str(value[i].split('其他')[-1])


def match_cheliangleixing(pos, value, save_path):
    for i in range(len(pos)):
        if '牌' in value[i] and '号' not in value[i]:
            if '类型' in value[i]:
                return value[i].split('类型')[-1]
            elif '类 型' in value[i]:
                return value[i].split('类 型')[-1]
            elif '：' in value[i]:
                return value[i].split('：')[-1]
            else:
                return value[i]
        elif '车辆类型' in value[i]:
            if len(value[i].split('类')[-1]) > 3:
                return value[i].split('类')[-1][1:]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                width *
                                3) and shr_pos[1][1] - height < pos[i][0][
                                    1] < shr_pos[1][1] and '吨' not in value[i]:
                        return value[i]

    else:
        return '重型半挂牵引车'


def match_dunwei(pos, value, save_path):
    for i in range(len(pos)):
        if '吨' in value[i] and value[i].split('吨')[0][-1].isdigit(
        ) and '位' not in value[i] or '座' not in value[i]:
            a = []
            a = re.findall("\d+\.?\d*", value[i])
            if len(a) > 0:
                return str(a[0]) + '吨'
            else:
                return '0吨'
    else:
        return '0吨'


# def match_chicun(pos,value,save_path):
#     chicun=[]
#     a = []
#     chicun2=[]
#     for i in range(len(pos)):
#         if '长' in value[i]:
#             if len(value[i])>5:
#                 a = re.findall("\d+\.?\d*", value[i])
#                 chicun.append(a[0])
#             else:
#                 shr_pos=pos[i]
#                 height=pos[i][3][1]-pos[i][0][1]
#                 width=pos[i][1][0]-pos[i][0][0]
#                 for i in range(len(pos)):
#                     if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+int(width*30) and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]:
#                         if value[i].isdigit():
#                             chicun.append(value[i])
#                 if len(chicun)>0:
#                     return chicun
#         elif '宽' in value[i]:
#             if len(value[i])>5:
#                 a = re.findall("\d+\.?\d*", value[i])
#                 chicun.append(a[0])
#         elif '高' in value[i]:
#             if len(value[i])>5:
#                 a = re.findall("\d+\.?\d*", value[i])
#                 chicun.append(a[0])

#     if len(chicun2)>0:
#         return chicun2
#     else:
#         return '0*0*0mm'


def match_chicun(pos, value, save_path):
    for i in range(len(pos)):
        if 'mm' in value[i] and value[i].split('mm')[0][-2:-1].isdigit():
            if '尺寸' in value[i]:
                return value[i].split('尺寸')[-1]
            else:
                return value[i]
        elif 'mmx' in value[i] and value[i].split('mmx')[0][-2:-1].isdigit():
            if '尺寸' in value[i]:
                return value[i].split('尺寸')[-1]
            else:
                return value[i]
        elif '车辆' in value[i] or '米' in value[i]:
            if len(value[i].split('米')) > 5:
                return value[i].split('米')[-1]

        elif '经营范围' in value[i]:
            rot = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width / 3 < pos[i][0][0] < shr_pos[1][
                        0] + width * 4 and shr_pos[0][1] - height * 2.2 < pos[
                            i][0][1] < shr_pos[1][1]:
                    rot.append(value[i])

            if len(rot) != 0:
                for i in range(len(rot)):
                    if '长' in rot[i] and len(rot[i]) > 6:
                        return '长' + rot[i].split('长')[-1]
                    else:
                        number = []
                        for i in range(len(rot)):
                            a = re.findall('\d+', rot[i])
                            if len(a) != 0:
                                number.extend(a)
                        return number

        elif '*' in value[i] and value[i].split('*')[0][-1].isdigit():
            return value[i]
        else:
            result = match_chicun_buchong(pos, value, save_path)
            return result


def match_chicun_buchong(pos, value, save_path):
    chicun = []
    final = []
    list2 = []
    for i in range(len(pos)):
        if '车辆尺寸' in value[i] or '尺寸' in value[i] or '车辆（毫米' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                        0] + int(width *
                                 1.5) and shr_pos[1][1] - height * 1.4 < pos[
                                     i][0][1] < shr_pos[2][1] + height * 5:
                    chicun.append(value[i])
            if len(chicun) != 0:
                for i in range(len(chicun)):
                    number = re.findall("\d+", chicun[i])
                    if len(number) != 0:
                        final.extend(number)

            if len(final) != 0:
                list2 = [
                    i for i in final if len(i) > 2 and len(i) < 5 and i[0] != 0
                ]

            if len(list2) == 3:
                return {"长": list2[0], "宽": list2[1], "高": list2[2]}
            else:
                return list2
