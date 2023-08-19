import re

# 删除集装箱号码中的非英文和数字
def remove_non_alphanumeric(string):
    pattern = r'[^a-zA-Z0-9]'
    return re.sub(pattern, '', string)


def remove_char(str, n):
    front = str[:n]  # up to but not including n
    back = str[n + 1:]  # n+1 till the end of string
    return front + back


def match_xianghao_onerow(pos,value,save_path):
    pattern2 = r'^[A-Z]{2}[a-zA-Z0-9]{7,}$'
    for i in range(len(value)):
        if re.match(pattern2,value[i].replace(' ','')):
            return remove_non_alphanumeric(value[i])
    else:
        return 'None'

def match_xianghao(pos,value,save_path):
    result=match_xianghao_onerow(pos, value, save_path)
    if result !='None':
        return result
    else:
        pattern = r'^[A-Z]{4}$'
        for i in range(len(pos)):
            if re.match(pattern, value[i]):
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for j in range(len(pos)):
                    if shr_pos[0][0] - width / 2 < pos[j][0][0] < shr_pos[1][
                            0] + width and shr_pos[3][1] - height/2 < pos[j][0][
                                1] < shr_pos[3][1] + height and value[j][2:4].isdigit():
                                result=value[i]+value[j]
                    elif shr_pos[1][0] - width / 2 < pos[j][0][0] < shr_pos[1][
                            0] + width and shr_pos[0][1] - height/2 < pos[j][0][
                                1] < shr_pos[3][1] and value[j][2:4].isdigit():
                                result=value[i]+value[j]
        
        return remove_non_alphanumeric(result)


def match_MAXGROSS(pos, value, save_path):
    for i in range(len(pos)):
        result = []
        if 'MAX' in value[i] or 'OSS' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                        0] + width * 2 and shr_pos[1][1] - height < pos[i][0][
                            1] < shr_pos[2][1] + height / 2:
                    result.append(value[i])
        if len(result) >= 2:
            print(result)
            return [result[0], result[1]]


def match_TARE(pos, value, save_path):
    for i in range(len(pos)):
        result = []
        if 'TARE' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                        0] + width * 2 and shr_pos[1][1] - height < pos[i][0][
                            1] < shr_pos[2][1] + height / 2:
                    result.append(value[i])
        if len(result) >= 2:
            print(result)
            return [result[0], result[1]]


def match_NET(pos, value, save_path):
    for i in range(len(pos)):
        result = []
        if 'NET' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width / 2 < pos[i][0][0] < shr_pos[1][
                        0] + width * 2 and shr_pos[1][1] - height < pos[i][0][
                            1] < shr_pos[2][1] + height / 1.5:
                    result.append(value[i])
        if len(result) >= 2:
            print(result)
            return [result[0], result[1]]
