import  re
from LAC import LAC
lac=LAC(mode='lac')


id_zhengze=r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'


def match_name(pos,value,save_path):
    for i in range(len(pos)):
        if '姓名' in value[i]:
            if len(value[i].split('名')[-1])>2:
                return value[i].split('名')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[0][1]-int(2*height)<pos[i][0][1]<shr_pos[2][1]+int(height/2):
                        return value[i]
        else:
            user_name_lis = []
            for i in range(len(pos)):
                _result = lac.run(value[i])
                for _index, _label in enumerate(_result[1]):
                    if _label == "PER":
                        user_name_lis.append(_result[0][_index])
            if len(user_name_lis)!=0:
                return user_name_lis[0]


def match_shenfenzhenghao(pos,value,save_path):
    for i in range(len(pos)):
        if re.findall(id_zhengze,value[i]):
            return value[i]
        elif '证号' in value[i]:
            if value[i].split('号')[1]!="" and value[i].split('号')[-1][2:8].isdigit():
                if len(value[i].split('号')[-1])>=15 and len(value[i].split('号')[1])<=19:
                    return value[i].split('号')[1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*3 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]+int(height/2):
                        if value[i][2:8].isdigit():
                            return value[i]
        elif '身份证件' in value[i]:
            if len(value[i].split('证')[-1])>5:
                num_list = [i for i in value[i] if str.isdigit(i)]
                return value[i].split('证')[-1][int(num_list[0])-1:]
    else:
        return '0'
        
    
def match_congyezigeleibie(pos,value,save_path):
    for i in range(len(pos)):
        type=[]
        if '性别' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]+width*4.5<pos[i][0][0]<shr_pos[1][0]+width*10 and shr_pos[0][1]-int(2*height)<pos[i][0][1]<shr_pos[2][1]+int(height/2):
                    type.append(value[i])
            all=''.join(type)
            if '经营性'in all or '道路' in all or '驾驶' in all:
                return '经营性道路货物运输驾驶员'
            elif 'J-货运' in all:
                return 'J-货运'
        elif '经营性'in value[i] or '道路' in value[i] or '驾驶' in value[i] and '运输管理' not in value:
            return '经营性道路货物运输驾驶员'
        elif 'J-货运' in value[i]:
            return 'J-货运'
    else:
        return '经营性道路货物运输驾驶员'


def match_riqi(pos,value,save_path):
    for i in range(len(pos)):
        if '初次' in value[i]:
            if len(value[i].split('日')[-1])>2:
                return value[i]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/4)<pos[i][0][0]<shr_pos[1][0]+int(width/4) and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[2][1]+height:
                        if value[i][1:2].isdigit():
                            return value[i]
    else:
        return '0'


def match_validate_date(pos,value,save_path):
    for i in range(len(pos)):
        if '至' in value[i] and value[i].split('至')[-1][:2].isdigit():
            if '考核' in value[i]:
                return value[i].split('至')[-1].split('考')[0]
            else:
                return value[i].split('至')[-1]
        elif '有效' in value[i] and '起' not in value[i] or '有效期限' in value[i]:
            if len(value[i].split('有效')[-1])>5:
                if '年' in value[i]:
                    return value[i].split('年')[0][-4:-1]+'年'+value[i].split('年')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(width/2) and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]+height/2:
                        if '年' in value[i]:
                            return value[i].split('年')[0][-4:-1]+'年'+value[i].split('年')[-1]
                        else:
                            return value[i]


def match_dangan(pos,value,save_path):
    for i in range(len(pos)):
        if '档案' in value[i] or '档家' in value[i] or '当案' in value[i]:
            if len(value[i])>5:
                a = []
                a = re.findall("\d+\.?\d*", value[i])
                if len(a[0])>0:
                    return a[0]
                else:
                    return value[i]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/4)<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]+height:
                        if value[i][1:2].isdigit():
                            return value[i]
        if '二维码' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[2][1]+height*2.5<pos[i][0][1]<shr_pos[2][1]+height*6:
                    if '：' in value[i]:
                        return value[i].split('：')[-1]