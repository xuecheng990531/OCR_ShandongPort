import os
import logging
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI, UploadFile, File, applications
from typing import Optional
from component_modules.autils import *

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(title='光学字符识别项目', description='根据每个单据要求的关键字进行返回')


@app.post('/ocr', tags=["识别接口（POST方法）"])
async def ocr(ID: int, Type: Optional[str] = None, Envir: Optional[str] = 'main', File: UploadFile = File(...)):
    '''
    OCR单据识别识别
    - 参数 ID: 上传哪类单据

    - 参数 Type: 某一单据下对应的其他单据 (不用管)

    - 参数 Envir: 是否展示全部结果(dev 显示全部结果, main 只显示需要检测的结果）

    上传文件要求:
    - jpg、png、jpeg、pdf

    - 1.上传的图片需要摆正，不能存在未经过旋转的图片。

    - 2.上传的PDF尽量不要超过一页,上传的身份证等证件正反面都需要放在一个照片之内。


    ID类别:
    - ID=1------------>危险货物安全适运说明书

    - ID=2------------>入境货物检验检疫证明

    - ID=3------------>进口报关单

    - ID=4------------>身份证

    - ID=5------------>行驶证

    - ID=6------------>驾驶证

    - ID=7------------>铁路货运单

    - ID=8------------>海运提单

    - ID=9------------>道路运输经营许可证

    - ID=10----------->营业执照

    - ID=11----------->从业资格证

    - ID=12----------->道路运输证

    - ID=13----------->MKL订舱下货纸

    - ID=14----------->过磅单

    - ID=15----------->集装箱信息
    '''
    filename = File.filename
    extension = os.path.splitext(File.filename)[-1]
    name = os.path.splitext(File.filename)[0]
    save_path = os.path.join('save_files', filename)

    if extension not in imgType_list and extension != '.pdf':
        logger.error("上传错误,上传的文件不在可上传范围内")
        return {"上传错误": '上传的文件不在可上传范围内'}
    else:

        # 写入图片
        await save_img(File, filename)

        # 检查上传的文件扩展名
        if extension in imgType_list:
            if ID == 7 or ID == 3 or ID == 11:
                check(img_path=save_path)
            elif ID == 12 or ID == 11:
                save_path = process_ID12(save_path)
            pos, value = detect_img(save_path)
            return detect_value(pos, ID, value, Type, save_path, Envir)

        else:
            count, img_list = pdf_img(save_path, name)

            if ID == 7 or ID == 3 or ID == 11:
                check(img_path=img_list[0])

            pos, value = detect_pdf(img_list, count)

            return detect_value(pos, ID, value, Type, img_list[0], Envir)


if __name__ == '__main__':
    uvicorn.run(app='app:app', host='0.0.0.0', port=8228, reload=True)
