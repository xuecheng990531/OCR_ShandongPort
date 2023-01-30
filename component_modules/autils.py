from paddleocr import PaddleOCR
from component_modules.paper_id_2_name import *
from component_modules.all_in_one import *
import os
import time
import fitz
import cv2
import aiofiles
import numpy as np
import cv2
import paddleocr

imgType_list = {'.jpg', '.bmp', '.png', '.jpeg', '.jfif', '.webp'}
#实例化paddleocr
ocr = PaddleOCR(use_angle_cls=False, lang="ch",workers=24,use_gpu=True ,det_limit_side_len=1280,cpu_threads=40)

#-------------------------------------------------保存上传图片-----------------------------------
async def save_img(File, filename):
    async with aiofiles.open(os.path.join('save_files',filename), 'wb') as out_file:
        content = await File.read()
        await out_file.write(content)
    print("文件：----> "+filename+" 保存成功")
#-------------------------------------------------保存上传图片-----------------------------------

#-------------------------------------------------倾斜检测并返回结果-----------------------------------
def detect_value(pos,ID,value,Type,save_path,filename):
    start = time.time()
    y_left_top=pos[0][0][1]
    y_right_top=pos[0][1][1]
    y_left_bottom=pos[0][3][1]
    x=abs(pos[3][3][0]-pos[3][0][0])
    y=abs(y_left_bottom-y_left_top)

    height=(x**2 + y**2)**(1/2)
    print(height)

    # 如果超过检测框高度的一半，判定为
    if abs(y_left_top-y_right_top)>height/2:
        return {
            "错误":"倾斜角度过大，重新上传"
        }
    else:
        result=detect_paper(ID,pos,value,Type,save_path)
        removed_result=remove(result)
        time_used=str(time.time() - start)+'s'
        return {"响应时间":time_used,"上传类型":get_paper_name(ID),"文件名":filename,"检测结果":removed_result,"算法检测的所有结果":value}
#-------------------------------------------------倾斜检测并返回结果-----------------------------------


#-------------------------------------------------逆时针旋转90度-----------------------------------
def RotateAntiClockWise90(img):
    trans_img = cv2.transpose( img )
    new_img = cv2.flip( trans_img, 0 )
    return new_img

def check(img_path):
    img=cv2.imread(img_path)
    height=img.shape[0]
    width=img.shape[1]

    if height>width:
        rotated=RotateAntiClockWise90(img)
        cv2.imwrite(img_path,rotated)
#-------------------------------------------------逆时针旋转90度-----------------------------------

#-------------------------------------------------对ID12的图像进行处理-----------------------------------
def gama_transfer(img,power1=1.1):
    if len(img.shape) == 3:
         img= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = 255*np.power(img/255,power1)
    img = np.around(img)
    img[img>255] = 255
    out_img = img.astype(np.uint8)
    
    return out_img

def process_ID12(img_path):
    img=cv2.imread(img_path)
    if img.shape[2]=='3':
        b,g,r=cv2.split(img)
        zengqiang=gama_transfer(r)
        kernel = np.ones((2, 2),np.uint8)
        img_process = cv2.erode(zengqiang, kernel)
    else:
        zengqiang=gama_transfer(img)
        kernel = np.ones((2, 2),np.uint8)
        img_process = cv2.erode(zengqiang, kernel)
    return img_process
#-------------------------------------------------对ID12的图像进行处理-----------------------------------


#-------------------------------------------------detect_pic-----------------------------------
def detect_img(img_path):
    result = ocr.ocr(img_path, cls=False)
    pos=[]
    value=[]
    version=paddleocr.VERSION
    print(version)
    if '2.6' in version:
        result=result[0]
        for i in range(len(result)):
            pos.append(result[i][0])
            value.append(result[i][1][0])
    else:
        for i in range(len(result)):
            pos.append(result[i][0])
            value.append(result[i][1][0])

    return pos,value
#-------------------------------------------------detect_pic-----------------------------------



#-------------------------------------------------detect_pdf-----------------------------------
def detect_pdf(img_list,page_no):
    if page_no==1:
        pos,value=detect_img(img_list[0])
        return pos,value
    else:
        value_all=[]
        pos_all=[]
        for index in range(page_no):
            pos,value=detect_img(img_list[index])
            value_all.extend(value)
            pos_all.extend(pos)
        return pos_all,value_all
#-------------------------------------------------detect_pdf-----------------------------------


#-------------------------------------------------PDF Compose-----------------------------------
def pdf_img(pdfPath,img_name): 
    img_list=[] 
    doc = fitz.open(pdfPath) 
    page_count=doc.page_count
    for page in doc: 
        pix = page.get_pixmap(dpi=300)  # render page to an image
        pix.save('save_files/'+img_name+'_%s.png' %page.number)  # store image as a PNG
        img_list.append('save_files/'+img_name+'_%s.png' %page.number)
    
    os.remove(pdfPath)

    return page_count,img_list
#-------------------------------------------------PDF Compose-------------------------------------

#-------------------------------------------------detect :-------------------------------------
def remove(dict):
    for i in dict:
        if dict[i] is None:
            dict[i]="None"
        else:
            if '：' in dict[i]:
                dict[i]=dict[i].replace('：','')
            elif '*' in dict[i]:
                dict[i]=dict[i].replace('*','')
            elif '，' in dict[i]:
                dict[i]=dict[i].replace('，','')
    return dict
#-------------------------------------------------detect :-------------------------------------

#-------------------------------------------------which paper-------------------------------------
def detect_paper(ID,pos,value,Type,save_path):
    if ID==1:
        result=match_weixian(pos,value,save_path)
        return result
    elif ID==2:
        result=match_jianyi(pos,value,save_path)
        return result
    elif ID==3:
        result=match_jinkou(pos, value,save_path)
        return result
    elif ID==4:
        result=match_id_card(pos,value,save_path)
        return result
    elif ID==5:
        result=match_xingshizheng(pos,value,save_path)   
        return result
    elif ID==6: 
        result=match_jiashizheng(pos,value,save_path)
        return result
    elif ID==7:
        result=match_tielu2(pos,value,save_path)
        return result
    elif ID==8:
        result=match_haiyun(pos,value,Type,save_path)
        return result
    elif ID==9:
        result=match_daoluyunshujingyingzigezheg(pos,value,save_path)
        return result
    elif ID==10:
        result=match_yingyezhizhao(pos,value,save_path)
        return result
    elif ID==11:
        result=match_congyezigezheng(pos,value,save_path)
        return result
    elif ID==12:
        result=match_daoluyunshu(pos,value,save_path)
        return result
    elif ID==13:
        result=match_xiahuozhi(pos,value,save_path)
        return result
    elif ID==14:
        result=match_guobangdan(pos,value,save_path)
        return result
    elif ID==15:
        result=match_jizhuangxiang(pos,value,save_path)
        return result
    else:
        return value
