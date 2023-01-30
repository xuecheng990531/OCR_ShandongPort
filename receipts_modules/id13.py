import re

def match_hangming(pos, value,save_path):
    for i in range(len(pos)):
        if '船名' in value[i] or '航次(Vessel)' in value[i]:
            if len(value[i].split('l')[-1])>5:
                if '：' in value[i].split('l')[-1]:
                    return value[i].split('：')[-1].split('/')[0]
                elif ':' in value[i].split('l')[-1]:
                    return value[i].split(':')[-1].split('/')[0]
                else:
                    return value[i].split('l')[-1].split('/')[0]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                        return value[i] 
        elif 'Voy No' in value[i]:
            vessel=[]
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width*4<pos[i][1][0]<shr_pos[0][0] and shr_pos[0][1]-height/2<pos[i][0][1]<shr_pos[0][1]+height/2 and 'Vessel' in value[i]:
                    ves_pos=pos[i]
                    height=pos[i][3][1]-pos[i][0][1]
                    width=pos[i][1][0]-pos[i][0][0]
                    for i in range(len(pos)):
                        if ves_pos[0][0]-int(width/2)<pos[i][0][0]<ves_pos[0][0]+width/2 and ves_pos[3][1]-height/2<pos[i][0][1]<ves_pos[3][1]+height*3:
                            vessel.append(value[i])
            return vessel
    else:
        return '0'
        
def match_hangci(pos, value,save_path):
    for i in range(len(pos)):
        if '船名' in value[i] or '航次(Vessel)' in value[i]:
            if len(value[i].split('l')[-1])>5:
                if '：' in value[i].split('l')[-1]:
                    return value[i].split('l')[-1].split('/')[-1]
                else:
                    return value[i].split('l')[-1].split('/')[-1]
            else:
                hm_pos=pos[i]
                for i in range(len(pos)):
                    if hm_pos[1][0]<pos[i][0][0]<hm_pos[1][0]+100 and hm_pos[1][1]-10<pos[i][0][1]<hm_pos[2][1]+10:
                        if '：' in value[i]:
                            return value[i].split('：')[-1].split('/')[-1]
                        else:
                            return value[i].split('/')[-1]
        elif 'Voy No' in value[i]:
            hangci=[]
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/2)<pos[i][0][0]<shr_pos[0][0]+width/2 and shr_pos[3][1]-height/2<pos[i][0][1]<shr_pos[3][1]+height*3:
                    hangci.append(value[i])
            return ''.join(hangci)
    else:
        return '0'

def match_tidanhao(pos,value,save_path):
    for i in range(len(pos)):
        if 'Booking' in value[i] and 'No' in value[i]:
            if len(value[i].split('o')[-1])>6:
                if '：' in value[i]:
                    return value[i].split('：')[-1]
                elif ':' in value[i]:
                    return value[i].split(':')[-1]
                else:
                    return value[i].split('o')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(width*2) and shr_pos[0][1]-int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2):
                        return value[i] 
    else:
        return '0'

def jianshu_xiangxing(pos,value,save_path):
    for i in range(len(pos)):
        if 'Pack. Qty/Kind' in value[i] or '包装数量/种类' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/2)<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[3][1]-height/2<pos[i][0][1]<shr_pos[3][1]+height and 'Pack' not in value[i]:
                    num = re.findall("\d+\.?\d*", value[i])
                    return num[0],value[i].split(str(int(num[0])))[-1]
    else:
        return '0','0'

def match_xiangxing(pos,value,save_path):
    for i in range(len(pos)):
        if 'Size/Type/Height' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+int(width*2) and shr_pos[1][1]-height/2<pos[i][0][1]<shr_pos[1][1]+height:
                    return value[i] 
        elif 'DRY' in value[i]:
            return 'DRY'
        elif 'TANK' in value[i]:
            return 'TANK'
    else:
        return 'no type'
def match_zhongliang(pos,value,save_path):
    for i in range(len(pos)):
        if 'KGS' in value[i]:
            return value[i]
    else:
        return '0'
def match_chaozhongxiang(pos,value,save_path):
    return "0"

def match_mudigang(pos,value,save_path):
    for i in range(len(pos)):
        if 'Service Mode' in value[i]: 
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[3][1]+height<pos[i][0][1]<shr_pos[3][1]+height*2:
                    return value[i]
    else:
        return '0'
def match_zhongzhuangang(pos,value,save_path):
    return "0"

def match_huoming(pos,value,save_path):
    return "0"

def match_jianshu(pos,value,save_path):
    for i in range(len(pos)):
        if 'Piece(s)' in value[i]:
            return value[i]
        elif 'Pack' in value[i] or 'Qty' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/4)<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+height:
                    return value[i] 
    else:
        return '0'
def match_chicun(pos,value,save_path):
    for i in range(len(pos)):
        if 'Size/Type' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0] and shr_pos[2][1]-height/2<pos[i][0][1]<shr_pos[2][1]+height:
                    num = re.findall("\d+\.?\d*", value[i])
                    return num[0]
    else:
        return '0'
def match_wendu(pos,value,save_path):
    return '0'

def match_shidu(pos,value,save_path):
    return '0'

def match_weixiandengji(pos,value,save_path):
    for i in range(len(pos)):
        if 'IMO Class' in value[i]:
            return value[i]
    else:
        return '0'

def match_weixianfudengji(pos,value,save_path):
    return '0'

def match_weiguihao(pos,value,save_path):
    return "0"

def match_xuqiu(pos,value,save_path):
    return "0"
