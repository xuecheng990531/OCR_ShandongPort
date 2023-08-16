from paddleocr import PaddleOCR
from component_modules.paper_id_2_name import *
from component_modules.all_in_one import *
import os
import fitz
import cv2
import aiofiles
import numpy as np
import cv2
import paddleocr
import re

imgType_list = {'.jpg', '.bmp', '.png', '.jpeg', '.jfif', '.webp'}
ocr = PaddleOCR(cls=True,
                lang="ch",
                workers=4,
                use_gpu=True,
                precision='fp16',
                det_limit_side_len=1216,
                use_multiprocess=True)


#-------------------------------------------------图片上传和删除-----------------------------------
async def save_img(File, filename):
    async with aiofiles.open(os.path.join('save_files', filename),
                             'wb') as out_file:
        content = await File.read()
        await out_file.write(content)
    print("文件：----> " + filename + " 上传成功!")


def del_upload_file():
    dir = 'save_files'
    for root, dirs, files in os.walk(dir):
        for name in files:
            if name.endswith(".png") or name.endswith(".jpg") or name.endswith(
                    ".pdf") or name.endswith(".jpeg") or name.endswith(
                        ".JPEG"):
                os.remove(os.path.join(root, name))
                print("文件：----> " + os.path.join(root, name) + " 删除成功!")


#-------------------------------------------------图片上传和删除-----------------------------------


#-------------------------------------------------倾斜检测并返回结果-----------------------------------
def detect_value(pos, ID, value, Type, save_path, Envir):
    result = detect_paper(ID, pos, value, Type, save_path)
    removed_result = remove(result)
    del_upload_file()

    if Envir == 'main':
        return {"检测结果": removed_result}
    else:
        return {"检测结果": removed_result, "算法检测的所有结果": value}


#-------------------------------------------------倾斜检测并返回结果-----------------------------------


#-------------------------------------------------逆时针旋转90度-----------------------------------
def RotateAntiClockWise90(img):
    trans_img = cv2.transpose(img)
    new_img = cv2.flip(trans_img, 0)
    return new_img


def check(img_path):
    img = cv2.imread(img_path)
    height = img.shape[0]
    width = img.shape[1]

    if height > width:
        rotated = RotateAntiClockWise90(img)
        cv2.imwrite(img_path, rotated)


#-------------------------------------------------逆时针旋转90度-----------------------------------


#-------------------------------------------------对ID12的图像进行处理-----------------------------------
def gama_transfer(img, power1=1.1):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = 255 * np.power(img / 255, power1)
    img = np.around(img)
    img[img > 255] = 255
    out_img = img.astype(np.uint8)

    return out_img


def process_ID12(img_path, ID):
    img = cv2.imread(img_path)
    if img.shape[2] == '3':
        b, g, r = cv2.split(img)
        zengqiang = gama_transfer(r)
        kernel = np.ones((2, 2), np.uint8)
        img_process = cv2.erode(zengqiang, kernel)
        if ID == 14:
            width, height = img_process.shape[:2]
            img_process = cv2.resize(img_process, (3 * height, 3 * width),
                                     interpolation=cv2.INTER_LINEAR)
    else:
        zengqiang = gama_transfer(img)
        kernel = np.ones((2, 2), np.uint8)
        img_process = cv2.erode(zengqiang, kernel)
        if ID == 14:
            width, height = img_process.shape[:2]
            img_process = cv2.resize(img_process, (3 * height, 3 * width),interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(img_path,img_process)


def process_ID45(img_path):
    img = cv2.imread(img_path)
    width, height = img.shape[:2]
    img2 = cv2.resize(img, (3 * height, 3 * width),interpolation=cv2.INTER_LINEAR)

    if img2.shape[2] == '3':
        b, g, r = cv2.split(img2)
        zengqiang = gama_transfer(r)
        kernel = np.ones((2, 2), np.uint8)
        img_process = cv2.erode(zengqiang, kernel)
    else:
        zengqiang = gama_transfer(img2)
        kernel = np.ones((2, 2), np.uint8)
        img_process = cv2.erode(zengqiang, kernel)
    cv2.imwrite(img_path,img_process)


def process_ID15(img_path):
    img = cv2.imread(img_path)
    width, height = img.shape[:2]
    img2 = cv2.resize(img, (3 * height, 3 * width),interpolation=cv2.INTER_LINEAR)
    gray_img = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    denoised_img = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(img_path,denoised_img)

#-------------------------------------------------对ID12的图像进行处理-----------------------------------


#-------------------------------------------------分离汉字和数字-----------------------------------
def separate_digits_and_chinese_chars(string):
    # 定义匹配数字和汉字字符的正则表达式
    digit_pattern = r'\d+'
    chinese_char_pattern = r'[\u4e00-\u9fa5]+'
    # 使用re.findall()函数找到所有匹配项，并存储在相应的列表中
    digits_list = re.findall(digit_pattern, string)
    if len(digits_list) == 3:
        return digits_list[0] + 'x' + digits_list[1] + 'x' + digits_list[2] + 'mm'
    else:
        return digits_list


#-------------------------------------------------分离汉字和数字-----------------------------------


#-------------------------------------------------分离英语和其他-----------------------------------
def split_address(string):
    english_chars = ""
    non_english_chars = ""
    for char in string:
        if char.isalpha() and ord(char) < 128:  # 只保留ASCII码范围内的英文字符
            english_chars += char
        else:
            non_english_chars += char
    return non_english_chars


#-------------------------------------------------分离英语和其他-----------------------------------


#-------------------------------------------------detect-----------------------------------
def detect_img(img_path):
    result = ocr.ocr(img_path, cls=False)
    pos = []
    value = []
    result = result[0]
    for i in range(len(result)):
        pos.append(result[i][0])
        value.append(result[i][1][0])
    # print('all pos',pos)
    # print('all value',value)
    return pos, value


def detect_pdf(img_list, page_no):
    if page_no == 1:
        pos, value = detect_img(img_list[0])
        return pos, value
    else:
        value_all = []
        pos_all = []
        for index in range(page_no):
            pos, value = detect_img(img_list[index])
            value_all.extend(value)
            pos_all.extend(pos)
        return pos_all, value_all


#-------------------------------------------------detect-----------------------------------


#-------------------------------------------------PDF 转换为图片-----------------------------------
def pdf_img(pdfPath, img_name):
    img_list = []
    doc = fitz.open(pdfPath)
    page_count = doc.page_count
    for page in doc:
        pix = page.get_pixmap(dpi=300)  # render page to an image
        pix.save('save_files/' + img_name +
                 '_%s.png' % page.number)  # store image as a PNG
        img_list.append('save_files/' + img_name + '_%s.png' % page.number)

    os.remove(pdfPath)

    return page_count, img_list


#-------------------------------------------------PDF 转换为图片-------------------------------------


#-------------------------------------------------检查不必要的字符并删除 :-------------------------------------
def remove(dict):
    if type(dict)==dict:
        for i in dict:
            if dict[i] is None:
                dict[i] = "None"
            else:
                if '：' in dict[i]:
                    dict[i]=dict[i].replace('：','')
                if '*' in dict[i]:
                    if '**/**' in dict[i]:
                        dict[i] = dict[i].replace('**/**', '')
                    else:
                        dict[i] = dict[i].replace('*', '')
                elif ':' in dict[i]:
                    dict[i] = dict[i].replace(':', '')
                # elif '，' in dict[i]:
                #     dict[i] = dict[i].replace('，', '')
                elif '\\"' in dict[i]:
                    dict[i] = dict[i].replace('\\"', '  ')
                elif '冰冰冰' in dict[i]:
                    dict[i] = dict[i].replace('冰冰冰', 'None')
                elif '备注' in dict[i]:
                    dict[i] = dict[i].split('备注')[-1]
        return dict
    else:
        return dict

#-------------------------------------------------检查不必要的字符并删除 :-------------------------------------

#-------------------------------------------------裁切图片-------------------------------------
def ReRec2(path, ymin, ymax, xmin, xmax):
    # 判断要裁切的坐标是不是大于0
    if ymin<0:
        ymin=0
    elif ymax<0:
        ymax=0
    elif xmin<0:
        xmin=0
    elif xmax<0:
        xmax=0
    
    # print(ymin,ymax,xmin,xmax)
    image = cv2.imread(path)
    cropImg = image[int(ymin):int(ymax), int(xmin):int(xmax)]
    cv2.imwrite('cropimg.png', cropImg)
    pos, value = detect_img(cropImg)
    return pos, value
#-------------------------------------------------裁切图片-------------------------------------

#-------------------------------------------------根据ID定位单据进行检测-------------------------------------
def detect_paper(ID, pos, value, Type, save_path):
    if ID == 1:
        result = match_weixian(pos, value, save_path)
        return result
    elif ID == 2:
        result = match_jianyi(pos, value, save_path)
        return result
    elif ID == 3:
        result = match_jinkou(pos, value, save_path)
        return result
    elif ID == 4:
        result = match_id_card(pos, value, save_path)
        return result
    elif ID == 5:
        result = match_xingshizheng(pos, value, save_path)
        return result
    elif ID == 6:
        result = match_jiashizheng(pos, value, save_path)
        return result
    elif ID == 7:
        result = match_tielu2(pos, value, save_path)
        return result
    elif ID == 8:
        result = match_haiyun(pos, value, Type, save_path)
        return result
    elif ID == 9:
        result = match_daoluyunshujingyingzigezheg(pos, value, save_path)
        return result
    elif ID == 10:
        result = match_yingyezhizhao(pos, value, save_path)
        return result
    elif ID == 11:
        result = match_congyezigezheng(pos, value, save_path)
        return result
    elif ID == 12:
        result = match_daoluyunshu(pos, value, save_path)
        return result
    elif ID == 13:
        result = match_xiahuozhi(pos, value, save_path)
        return result
    elif ID == 14:
        result = match_guobangdan(pos, value, save_path)
        return result
    elif ID == 15:
        result = match_jizhuangxiang(pos, value, save_path)
        return result
    elif ID == 16:
        result = match_jianyi_shuban(pos, value, save_path)
        return result
    else:
        return value
