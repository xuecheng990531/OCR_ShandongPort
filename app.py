import os
import uvicorn
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI, UploadFile, File, applications
from typing import Optional, Union
from component_modules.autils import *


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url=
        'https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js',
        swagger_css_url=
        'https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css')


applications.get_swagger_ui_html = swagger_monkey_patch

app = FastAPI(title='光学字符识别项目', description='根据每个单据要求的关键字进行返回。\n- 上传文件要求:\n- jpg、png、jpeg、pdf\n- 1.上传的图片需要摆正，不能存在未经过旋转的图片。\n- 2.上传的PDF尽量不要超过一页,上传的身份证等证件正反面都需要放在一个照片之内。')


@app.post('/ocr', tags=["识别接口（POST方法）"])
async def ocr(ID: int,Type: Optional[str] = None,File: UploadFile = File(...)):
    '''
    OCR单据识别识别
    - 参数 ID: 上传哪类单据
    ID类别:
    - ID=1------------>危险货物安全适运说明书

    - ID=2------------>入境货物检验检疫证明

    - ID=16------------>入境货物检验检疫证明,明细部分是竖着展示的

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
        return {"上传错误": '上传的文件不在可上传范围内'}
    else:

        # 写入图片
        await save_img(File, filename)

        # 检查上传的文件扩展名
        if extension in imgType_list:
            if ID == 7 or ID == 3 or ID == 11:
                check(img_path=save_path)
            elif ID == 12 or ID == 11 or ID == 14:
                process_ID12(save_path, ID)
            elif ID == 5 or ID==4:
                process_ID45(save_path)
            pos, value = detect_img(save_path)
            return detect_value(pos, ID, value, Type, save_path, Envir='dev')

        else:
            count, img_list = pdf_img(save_path, name)

            if ID == 7 or ID == 3 or ID == 11:
                check(img_path=img_list[0])

            pos, value = detect_pdf(img_list, count)

            return detect_value(pos, ID, value, Type, img_list[0], Envir='dev')


if __name__ == '__main__':
    import paddle
    paddle.device.set_device("gpu:0")
    uvicorn.run(app='app:app', host='0.0.0.0', port=8008, reload=True)