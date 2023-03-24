import re

def remove_char(str, n):
    front = str[:n]  # up to but not including n
    back = str[n + 1:]  # n+1 till the end of string
    return front + back


def match_xianghao(pos,value,save_path):
    result=[]
    alpha=[]
    for i in range(len(value)):
        compileX = re.findall(r"^[A-Z]{1,4}$",value[i])
        if len(compileX)!=0:
            alpha.append(compileX[0])

    for i in range(len(pos)):
        if alpha[0] in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[1][1]+height*2: 
                    result.append(value[i])
            if len(result)!=0:
                final= alpha[0]+''.join(result)
                if len(final)==15:
                    final=remove_char(final,-5)
                    return final
                else:
                    return final
            
def match_MAXGROSS(pos,value,save_path):
    for i in range(len(pos)):
        result=[]
        if 'MAX' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]+height/2:
                    result.append(value[i])
        if len(result)>=2:
            print(result)
            return [result[0],result[1]]

def match_TARE(pos,value,save_path):
    for i in range(len(pos)):
        result=[]
        if 'TARE' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]+height/2:
                    result.append(value[i])
        if len(result)>=2:
            print(result)
            return [result[0],result[1]]

def match_NET(pos,value,save_path):
    for i in range(len(pos)):
        result=[]
        if 'NET' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[2][1]+height/1.5:
                    result.append(value[i])
        if len(result)>=2:
            print(result)
            return [result[0],result[1]]
