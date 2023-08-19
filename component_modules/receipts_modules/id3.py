import re


def match_bianhao(pos, value, save_path):
    for i in range(len(pos)):
        if '预' and '编号' in value[i]:
            m = re.search(r"\d", value[i])
            return value[i][int(m.start()):]

# new
def match_shouhuoren(pos, value, save_path):
    for i in range(len(pos)):
        if '境内收货人' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]  # 收货人的宽度
            width = pos[i][1][0] - pos[i][0][0]

            for i in range(len(pos)):
                if shr_pos[0][0] - width < pos[i][0][0] < shr_pos[0][
                        0] + width and shr_pos[3][1] - height < pos[i][0][
                            1] < shr_pos[3][1] + height and '收货人' not in value[
                                i]:
                    return value[i]
    else:
        return 'None'


# new
def match_shenbaoriqi(pos, value, save_path):
    for i in range(len(pos)):
        if '报日期' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]  # 收货人的宽度
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width < pos[i][0][0] < shr_pos[0][
                        0] + width and shr_pos[3][1] - height < pos[i][0][
                            1] < shr_pos[3][
                                1] + height and '申报日期' not in value[i]:
                    return value[i]
    else:
        return 'None'



# new
def match_jinjingguanbie(pos, value, save_path):
    for i in range(len(pos)):
        if '进境关别' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]  # 收货人的宽度
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width < pos[i][0][0] < shr_pos[0][
                        0] + width and shr_pos[3][1] - height < pos[i][0][
                            1] < shr_pos[3][
                                1] + height and '进境关别' not in value[i]:
                    return value[i]
    else:
        return 'None'


# new
def match_yunshufangshi(pos, value, save_path):
    for i in range(len(pos)):
        if '运输方式' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]  # 收货人的宽度
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width < pos[i][0][0] < shr_pos[0][
                        0] + width and shr_pos[3][1] - height < pos[i][0][
                            1] < shr_pos[3][
                                1] + height and '运输方式' not in value[i]:
                    return value[i]
    else:
        return 'None'



# new
def match_tiyundanhao(pos, value, save_path):
    for i in range(len(pos)):
        if '提运单号' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]  # 收货人的宽度
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0] - width < pos[i][0][0] < shr_pos[0][
                        0] + width and shr_pos[3][1] - height < pos[i][0][
                            1] < shr_pos[3][
                                1] + height and '提运单号' not in value[i]:
                    return value[i]
    else:
        return 'None'


def match_shenbaodanwei(pos, value, save_path):
    for i in range(len(pos)):
        if '申报单位' in value[i] and '签' not in value[i]:
            return value[i].split('位')[-1]
    else:
        return 'None'