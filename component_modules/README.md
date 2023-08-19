# OCR 单据识别使用说明

## 运行说明 :zap:
<li>安装Paddle以及PaddleOCR
<ol>
<li>Paddle 安装: https://www.paddlepaddle.org.cn/ </li>
<li>PaddleOCR 安装: https://github.com/PaddlePaddle/PaddleOCR</li>
</ol>
</li>
<li>安装其他依赖 <code>pip install -r requirements.txt (里面有些可能是错的，安装不上的百度一搜就行)</code></li>
<li>启动程序 <code>python app.py</code>（注意：在app.py的最后，可以选择端口号，默认8008）</li>
<li>打开网页，输入<code>http://localhost:8008/docs</code>即可进行交互式API测试。</li>

## 组织架构 :wrench:
<li>:label:Model:用来存放每一次训练的模型</li>
<li>:label:component_modules
<ol>
<li><code>all_in_one.py</code> 该文件是所有单据返回结果的地方，使用list对每个单据的结果进行返回。</li>
<li><code>autils.py</code> 该文件包含各种工具，比如图像增强，裁剪，PDF保存为图片等。</li>
<li><code>paper_id_2_nam.py</code> 单据名称对应的ID号。</li>
</ol>
</li>
<li> :label:receipts_modules  包含各个单据对应的的检测方法。</li>
<li>:label:save_files 通过API上传的图片会保存在这里。</li>



