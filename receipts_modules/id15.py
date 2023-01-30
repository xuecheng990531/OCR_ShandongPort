def match_xianghao(pos,value,save_path):

    for i in range(len(pos)):
        if len(value[i])>=6 and value[i][1:4].isdigit():
            n1=value[i]
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/3)<pos[i][0][0]<shr_pos[0][0]+int(width/2) and shr_pos[0][1]+int(height/2)<pos[i][0][1]<shr_pos[0][1]+int(height/2+height):
                    return n1+value[i]
    else:
        return '0'

def match_MAXGROSS(pos,value,save_path):
    for i in range(len(pos)):
        if 'MAX' in value[i]:
            return value[i+1],value[i+2]
    else:
        return '0'
def match_TARE(pos,value,save_path):
    for i in range(len(pos)):
        if 'TARE' in value[i]:
            return value[i+1],value[i+2]
    else:
        return '0'
def match_NET(pos,value,save_path):
    for i in range(len(pos)):
        if 'NET' in value[i]:
            return value[i+1],value[i+2]
    else:
        return '0'