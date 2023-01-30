
def match_tidanhao(pos,value,save_path):
    for i in range(len(pos)):
        if 'BILL' in value[i] and 'OF' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-int(width/2)<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+height:
                    return value[i]
    else:
        return '0'
        
def match_tidanhao_rizhao(pos,value,save_path):
    for i in range(len(pos)):
        if 'B/L' in value[i] and 'No' in value[i]:
            bl_pos=pos[i]
            for i in range(len(pos)):
                if bl_pos[0][0]<pos[i][0][0]<bl_pos[0][0]+140 and bl_pos[0][1]<pos[i][0][1]<bl_pos[0][1]+70:
                    return value[i]
    else:
        return '0'
def match_dingcanghao_rizhao(pos,value,save_path):
    for i in range(len(pos)):
        if 'Total' in value[i] and 'Number' in value[i]:
            bl_pos=pos[i]
            for i in range(len(pos)):
                if bl_pos[0][0]<pos[i][0][0]<bl_pos[0][0]+80 and bl_pos[0][1]-90<pos[i][0][1]<bl_pos[0][1]:
                    return value[i]
    else:
        return '0'
def match_dingcanghao(pos,value,save_path):
    for i in range(len(pos)):
        if 'OOKING' in value[i] or 'REF' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/4)<pos[i][0][0]<shr_pos[0][0]+int(width/5) and shr_pos[3][1]-int(height/2)<pos[i][0][1]<shr_pos[3][1]+int(height+height/2):
                    return value[i]
    else:
        return '0'
