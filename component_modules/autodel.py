# 自动清理保存图片
import os
def autodel(rootdir):

    imgType_list = {'.jpg', '.bmp', '.png', '.jpeg', '.jfif', '.webp'}
    filelist=os.listdir(rootdir)
    length=len(filelist)

    for i in range(length):
        extension = os.path.splitext(filelist[i])[-1]
        abs_path='/icislab/volume1/lixuecheng/ocr/save_files/'+filelist[i]
        if extension in imgType_list:
            os.remove(abs_path)
    
    return 'finished'