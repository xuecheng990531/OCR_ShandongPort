import re
from LAC import LAC

lac = LAC(mode="lac")
tiaoxingma='^[A-Z0-9]*$'

PATTERN = r'([\u4e00-\u9fa5]{2,5}?(?:省|自治区|市)){0,1}([\u4e00-\u9fa5]{2,7}?(?:区|县|州)){0,1}([\u4e00-\u9fa5]{2,7}?(?:村|镇|街道)){1}'

def match_tiaoxingmabianhao(pos,value,save_path):
    for i in range(len(pos)):
        if '货物运单' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]+width<pos[i][0][0]<shr_pos[1][0]+width*10 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[1][1]+height:
                    return value[i]
        elif re.match(tiaoxingma,value[i]):
            return value[i]
    else:
        return ''
def match_tuoyunren(pos,value,save_path):
    for i in range(len(pos)):
        if '货位' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(4*width)<pos[i][1][0]<shr_pos[0][0] and shr_pos[0][1]-height<pos[i][1][1]<shr_pos[0][1]+height and '货位' not in value[i] and '经办人' not in value[i]:
                    return value[i]
    else:
        return '0'
def match_daozhanren(pos,value,save_path):
    for i in range(len(pos)):
        if '施' in value[i] and '号' in value[i] and len(value[i])==3:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(4*width)<pos[i][1][0]<shr_pos[0][0] and shr_pos[0][1]-height<pos[i][1][1]<shr_pos[0][1]+height and '号' not in value[i] and '经办人' not in value[i]:
                    return value[i]
    else:
        return '0'

def match_dizhi(pos,value,save_path):
    for i in range(len(pos)):
        pattern = re.compile(PATTERN)
        m = pattern.search(value[i])
    return m

def match_xuqiuhao(pos,value,save_path):
    for i in range(len(pos)):
        if '需求号' in value[i] or '求号' in value[i]:
            if len(value[i].split('号')[-1])>5:
                return value[i].split('号')[-1]
            else:
                shr_pos=pos[i]
                height=pos[i][3][1]-pos[i][0][1]# 收货人的宽度
                width=pos[i][1][0]-pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+int(height/2) and len(value[i])>11:
                        return value[i]
    else:
        return '0'            

def match_fazhan(pos,value,save_path):
    for i in range(len(pos)):
        if '发站' in value[i] and '公司' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]# 收货人的宽度
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+int(height/2) and '发站' not in value[i]:
                    return value[i]
    else:
        return '0'

# def match_tuoyunmingcheng(pos,value,save_path):
#     for i in range(len(pos)):
#         if '取货地址' in value[i]:
#             n_pos=pos[i]
#             for i in range(len(pos)):
#                 if n_pos[0][0]-30<pos[i][0][0]<n_pos[0][0] and n_pos[0][1]-80<pos[i][3][1]<n_pos[0][1]:
#                     return value[i]

# new
def match_tuoyunmingcheng(pos,value,save_path):
    for i in range(len(pos)):
        if '取货地址' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]# 收货人的宽度
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/3)<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-(height+int(height/2))<pos[i][3][1]<shr_pos[0][1]:
                    return value[i]
    else:
        return '0'
# def match_shouhuomingcheng(pos,value,save_path):
#     for i in range(len(pos)):
#         if '送货地址' in value[i]:
#             n_pos=pos[i]
#             for i in range(len(pos)):
#                 if n_pos[0][0]-30<pos[i][0][0]<n_pos[0][0] and n_pos[0][1]-80<pos[i][3][1]<n_pos[0][1]:
#                     return value[i]

#new
def match_shouhuomingcheng(pos,value,save_path):
    for i in range(len(pos)):
        if '送货地址' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width/3)<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[0][1]-(height+int(height/2))<pos[i][3][1]<shr_pos[0][1]:
                    return value[i]
    else:
        return '0'

# def match_daozhan(pos,value,save_path):
#     for i in range(len(pos)):
#         if '到站' in value[i] and '公司' in value[i]:
#             daozhan_pos=pos[i]
#             for i in range(len(pos)):
#                 if daozhan_pos[1][0]<pos[i][0][0]<daozhan_pos[1][0]+150 and daozhan_pos[0][1]-10<pos[i][0][1]<daozhan_pos[0][1]+30:
#                     return value[i]

# new
def match_daozhan(pos,value,save_path):
    for i in range(len(pos)):
        if '到站' in value[i] and '公司' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[1][1]-int(height/2)<pos[i][0][1]<shr_pos[1][1]+int(height/2) and '发站' not in value[i] and '取货地址' not in value[i]:
                    return value[i]
    else:
        return '0'
    
def match_phone_tuoyun(pos,value,save_path):
    for i in range(len(pos)):
        if '车种车号' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][1][0]<shr_pos[0][0] and value[i].isdigit() and shr_pos[0][1]-height<pos[i][1][1]<shr_pos[0][1]+height and '车号' not in value[i]:
                    return value[i]
    else:
        return '0'
def match_phone_shouhuo(pos,value,save_path):
    for i in range(len(pos)):
        if '布号' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width<pos[i][1][0]<shr_pos[0][0] and value[i].isdigit() and shr_pos[0][1]-height<pos[i][1][1]<shr_pos[0][1]+height and '布号' not in value[i]:
                    return value[i]

    else:
        return '0'
def match_huowumingcheng(pos,value,save_path):
    huowu=[]
    for i in range(len(pos)):
        if '货物名称' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width*1.5<pos[i][0][0]<shr_pos[0][0]+width and shr_pos[3][1]-height/2<pos[i][0][1]<shr_pos[3][1]+(height*3.5):
                    huowu.append(value[i])
            if len(huowu)>0:
                return huowu
            else:
                return ''
    else:
        return '0'


def match_jianshu(pos,value,save_path):
    for i in range(len(pos)):
        if '合计' in value[i] and len(value[i])==2:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]+width<pos[i][0][0]<shr_pos[1][0]+int(width*4) and value[i].isdigit() and shr_pos[0][1]-height<pos[i][1][1]<shr_pos[0][1]+height and '合计' not in value[i]:
                    return value[i]+'件'
    else:
        return '0'
def match_zhongliang(pos,value,save_path):
    for i in range(len(pos)):
        if '合计' in value[i] and len(value[i])==2:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]+int(5*width)<pos[i][0][0]<shr_pos[1][0]+int(width*15) and shr_pos[0][1]-height/2<pos[i][1][1]<shr_pos[0][1]+height/2 and '合计' not in value[i]:
                    return value[i]+'KG'
    else:
        return '0'
# def match_xianghao(pos,value,save_path):
#     xianghao=[]
#     for i in range(len(pos)):
#         if value[i][:3].isalpha() and re.sub('[\u4e00-\u9fa5]', '', value[i][:3]) and len(value[i])==11:
#             xianghao.append(value[i])
#     return xianghao

# new
def match_xianghao(pos,value,save_path):
    xianghao=[]
    for i in range(len(pos)):
        if '箱号' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-2*width<pos[i][0][0]<shr_pos[0][0] and shr_pos[3][1]-height<pos[i][0][1]<shr_pos[3][1]+(height*3) and '箱号' not in value[i]:
                    xianghao.append(value[i])
            return xianghao
    else:
        return '0'                
                    
def match_shifenghao(pos,value,save_path):
    sf=[]
    for i in range(len(pos)):
        if '装箱' in value[i] and '封号' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width+width/2)<pos[i][0][0]<shr_pos[0][0] and shr_pos[3][1]<pos[i][0][1]<shr_pos[3][1]+int(height*3) and '封号' not in value[i]:
                    sf.append(value[i])
    if len(sf)==0:
        return '0'
    else:
        return sf
        

def match_feimu(pos,value,save_path):
    feimu=[]
    for i in range(len(pos)):
        if '费目' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-int(width+width/2)<pos[i][0][0]<shr_pos[0][0] and shr_pos[3][1]<pos[i][0][1]<shr_pos[3][1]+int(height*3):
                    feimu.append(value[i])
        elif '税额' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[3][1]<pos[i][0][1]<shr_pos[3][1]+int(height*5):
                    pattern = re.compile("[\u4e00-\u9fa5]")
                    s="".join(pattern.findall(value[i]))
                    feimu.append(s)
    if len(feimu)==0:
        return '0'
    else:
        return feimu

                    

def match_feiyongheji(pos,value,save_path):
    for i in range(len(pos)):
        if '大写' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[0][0]-width*2.4<pos[i][1][0]<shr_pos[0][0] and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[1][1]+height and '￥' in value[i]:
                    return value[i]

        elif '￥' in value[i]:
            return value[i]
        elif '费用合计' in value[i] or'用合计' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]<pos[i][0][0]<shr_pos[1][0]+width*2 and shr_pos[1][1]-height<pos[i][0][1]<shr_pos[1][1]+height:
                    return value[i]
    else:
        return '0'


def match_shuie(pos,value,save_path):
    shiue=[]
    for i in range(len(pos)):
        if '税额' in value[i]:
            shr_pos=pos[i]
            height=pos[i][3][1]-pos[i][0][1]
            width=pos[i][1][0]-pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0]-width/2<pos[i][0][0]<shr_pos[1][0]+width and shr_pos[3][1]<pos[i][0][1]<shr_pos[3][1]+int(height*5):
                    s="".join(filter(lambda s:s in'0123456789.', value[i]))
                    shiue.append(s)
    if len(shiue)==0:
        return '0'
    else:
        return shiue

                

def match_jine(pos,value,save_path):
    return '0'

