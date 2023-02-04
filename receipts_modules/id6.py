
from LAC import LAC
import re
lac = LAC(mode="lac")

zhunjia=['A1','A2','A3','B1','B2','C1','C2','C3','C4']

def match_name(pos,value,save_path):
    for i in range(len(pos)):
        if '姓名' in value[i]:
            if len(value[i].split('名')[-1])>2:
                if '档案' in value[i]:
                    return value[i].split('名')[-1].split('档')[0]
                else:
                    return value[i].split('名')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[0][0]-width/2<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1] and '姓名' not in value[i] and '档案编号' not in value[i]:
                        return value[i]

        else:
            user_name_lis = []
            for i in range(len(pos)):
                if re.findall('[\u4e00-\u9fa5]', value[i]):
                    _result = lac.run(value[i])
                    for _index, _label in enumerate(_result[1]):
                        if _label == "PER":
                            user_name_lis.append(_result[0][_index])
            if len(user_name_lis)!=0:
                return user_name_lis[0]

def match_sex(pos,value,save_path):
    for i in range(len(pos)):
        if '性别' in value[i]:
            if len(value[i].split('别')[-1])>=1:
                if '男' in value[i]:
                        return '男'
                else:
                    return '女'
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[0][1]-height<pos[i][0][1]<shr_pos[3][1]+height:
                        if '男' in value[i]:
                            return '男'
                        else:
                            return '女'
        elif 'Sex' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[0][1]-1.5*height<pos[i][0][1]<shr_pos[3][1]+height:
                    if '男' in value[i]:
                        return '男'
                    else:
                        return '女'
        else:
            return '男'

def match_jiashizhenghao(pos,value,save_path):
    for i in range(len(pos)):
        if '证号' in value[i]:
            if len(value[i].split('号')[-1])>2:
                id=value[i].split('号')[-1]
                return id
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]:
                        return value[i]

def match_address(pos,value,save_path):
    address=[]
    address2=[]
    for i in range(len(pos)):
        if '住址' in value[i] or '址' in value[i] or '佳址' in value[i]:
            if len(value[i].split('址')[-1])>3:
                return value[i].split('址')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(2*width) and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+height*2.2 and '址' not in value[i]:
                        address.append(value[i])
                if len(address)>0:
                    result = ''.join(address)
                    return result
        elif '性别' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width*10<pos[i][0][0]<shr_pos[0][0]-3*width and shr_pos[3][1]+height/2<pos[i][0][1]<shr_pos[3][1]+height*3.4:
                    address2.append(value[i])
            if len(address2)>0:
                result=''.join(address2)
                if '址' in result:
                    return result.split('址')[-1]
                else:
                    return result
    return '无'

def match_chexing(pos,value,save_path):
    for i in range(len(pos)):
        if value[i] in zhunjia:
            return value[i]
        elif '准驾' in value[i]:
            if (re.search(r'\d', value[i])):
                num_list = [i for i in value[i] if str.isdigit(i)]
                return value[i][int(num_list[0]):]
            else:
                zj_pos=pos[i]
                for i in range(len(pos)):
                    if zj_pos[1][0]<pos[i][0][0]<zj_pos[1][0]+100 and zj_pos[1][1]-10<pos[i][0][1]<zj_pos[2][1]+10:
                        return value[i]
    else:
        return 'A2'

def match_valid_date(pos,value,save_path):
    for i in range(len(pos)):
        if '至' in value[i] and len(value[i].split('至')[-1])>4:
            return value[i].split('至')[-1]
        elif '年' in value[i]:
            return value[i]
    else:
        return '0'