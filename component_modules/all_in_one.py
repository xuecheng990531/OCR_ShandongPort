from receipts_modules import id1, id10, id11, id12, id13, id14, id15, id2, id3, id4, id5, id6, id7, id8, id9,id2_vertical

def match_jinkou(pos,value,save_path):
    bianhao=id3.match_bianhao(pos, value,save_path)
    shouhuoren=id3.match_shouhuoren(pos,value,save_path)
    shenbaoriqi=id3.match_shenbaoriqi(pos, value,save_path)
    jinjingguanbie=id3.match_jinjingguanbie(pos, value,save_path)
    yunshufangshi=id3.match_yunshufangshi(pos, value,save_path)
    yundanhao=id3.match_tiyundanhao(pos, value,save_path)
    shenbaodanwei=id3.match_shenbaodanwei(pos, value,save_path)

    return {
        "编号":bianhao,"收货人":shouhuoren,"申报日期":shenbaoriqi,
        "进境关别":jinjingguanbie,"运输方式":yunshufangshi,
        "运单号":yundanhao,"申报单位":shenbaodanwei
        }

def match_jianyi_shuban(pos,value,save_path):
    bianhao=id2_vertical.match_bianhao(pos, value,save_path)
    shouhuoren=id2_vertical.match_shouhuoren(pos,value,save_path)
    fahuoren=id2_vertical.match_fahuoren(pos, value,save_path)
    pinming=id2_vertical.match_pinming(pos, value,save_path)
    zhongliang=id2_vertical.match_zhongliang(pos, value,save_path)
    shuchuguojia=id2_vertical.match_shuchuguojia(pos, value,save_path)
    jizhuangxiang=id2_vertical.match_jizhuangxiang(pos, value,save_path)
    shengchanriqi=id2_vertical.match_shengchanriqi(pos, value,save_path)
    shengchanchangjia=id2_vertical.match_shengchanchangjia(pos, value,save_path)
    pinpai=id2_vertical.match_pinpai(pos, value,save_path)
    guige=id2_vertical.match_guige(pos, value,save_path)
    hetonghao=id2_vertical.match_hetonghao(pos, value,save_path)
    yundanhao=id2_vertical.match_tiyundanhao(pos, value,save_path)
    rujingkouan=id2_vertical.match_rujingkouan(pos, value,save_path)
    rujingriqi=id2_vertical.match_rujingriqi(pos, value,save_path)
    biaoji=id2_vertical.match_biaoji(pos, value,save_path)
    baozhuangzhonglei=id2_vertical.match_baozhuangzhonglei(pos, value,save_path)
    beizhu=id2_vertical.match_beizhu(pos, value,save_path)

    return {
        "编号":bianhao,"收货人":shouhuoren,"发货人":fahuoren,
        "品名":pinming,"报检数/重量":zhongliang,"输出国家":shuchuguojia,
        "集装箱号":jizhuangxiang,"生产日期":shengchanriqi,"生产厂家":shengchanchangjia,
        "品牌":pinpai,"规格":guige,"合同号":hetonghao,"运单号":yundanhao,
        "入境口岸":rujingkouan,"入境日期":rujingriqi,
        "标记":biaoji,"包装种类":baozhuangzhonglei,"备注":beizhu
        }

def match_jianyi(pos,value,save_path):
    bianhao=id2.match_bianhao(pos, value,save_path)
    shouhuoren=id2.match_shouhuoren(pos,value,save_path)
    fahuoren=id2.match_fahuoren(pos, value,save_path)
    pinming=id2.match_pinming(pos, value,save_path)
    zhongliang=id2.match_zhongliang(pos, value,save_path)
    shuchuguojia=id2.match_shuchuguojia(pos, value,save_path)
    jizhuangxiang=id2.match_jizhuangxiang(pos, value,save_path)
    shengchanriqi=id2.match_shengchanriqi(pos, value,save_path)
    shengchanchangjia=id2.match_shengchanchangjia(pos, value,save_path)
    pinpai=id2.match_pinpai(pos, value,save_path)
    guige=id2.match_guige(pos, value,save_path)
    hetonghao=id2.match_hetonghao(pos, value,save_path)
    yundanhao=id2.match_tiyundanhao(pos, value,save_path)
    rujingkouan=id2.match_rujingkouan(pos, value,save_path)
    rujingriqi=id2.match_rujingriqi(pos, value,save_path)
    biaoji=id2.match_biaoji(pos, value,save_path)
    baozhuangzhonglei=id2.match_baozhuangzhonglei(pos, value,save_path)
    beizhu=id2.match_beizhu(pos, value,save_path)

    return {
        "编号":bianhao,"收货人":shouhuoren,"发货人":fahuoren,
        "品名":pinming,"报检数/重量":zhongliang,"输出国家":shuchuguojia,
        "集装箱号":jizhuangxiang,"生产日期":shengchanriqi,"生产厂家":shengchanchangjia,
        "品牌":pinpai,"规格":guige,"合同号":hetonghao,"运单号":yundanhao,
        "入境口岸":rujingkouan,"入境日期":rujingriqi,
        "标记":biaoji,"包装种类":baozhuangzhonglei,"备注":beizhu
        }

def match_weixian(pos,value,save_path):
    fahuoren=id1.match_fahuoren(pos, value,save_path)
    shouhuoren=id1.match_shouhuoren(pos, value,save_path)
    chengyunren=id1.match_chengyunren(pos, value,save_path)
    hangminghangci=id1.match_hangminghangci(pos, value,save_path)
    zhuanghuogang=id1.match_zhuanghuogang(pos, value,save_path)
    xiehuogang=id1.match_xiehuogang(pos, value,save_path)
    tidanhao=id1.match_tidanhao(pos, value,save_path)
    IMO=id1.match_IMO(pos, value,save_path)
    UN=id1.match_UN(pos, value,save_path)
    baozhuanglei=id1.match_baozhuanglei(pos, value,save_path)
    shandian=id1.match_shandian(pos, value,save_path)
    yingjicuoshi=id1.match_yingjicuoshi(pos, value,save_path)
    baojianzhonglei=id1.match_baojianzhonglei(pos, value,save_path)
    kongzhiwendu=id1.match_kongzhiwendu(pos, value,save_path)
    haiyangwuranwu=id1.match_haiyangwuranwu(pos, value,save_path)
    zongzhong=id1.match_zongzhong(pos, value,save_path)
    jingzhong=id1.match_jingzhong(pos, value,save_path)

    return {
        "发货人":fahuoren,"收货人":shouhuoren,
        "承运人":chengyunren,"航名航次":hangminghangci,
        "装货港":zhuanghuogang,"卸货港":xiehuogang,"提运单号":tidanhao,"IMO":IMO,"UN":UN,
        "包装种类":baozhuanglei,"闪点":shandian,"应急措施":yingjicuoshi,"包件种类":baojianzhonglei,
        "控制温度":kongzhiwendu,"海洋污染物":haiyangwuranwu,"总重":zongzhong,"净重":jingzhong
        }

def match_id_card(pos,value,save_path):
    minzu=id4.match_minzu(pos,value,save_path)
    sex=id4.match_sex(pos,value,save_path)
    name=id4.match_name(pos,value,save_path)
    address=id4.match_address(pos,value,save_path)
    id_number,are,date=id4.match_idnumber(pos,value,save_path)
    validate_date=id4.match_validdate(pos,value,save_path)
    qianfa=id4.match_qianfa(pos,value,save_path)

    return{
        "姓名":name,"性别":sex,"民族":minzu,
        "出生日期":date,"住址":address,"身份证号":id_number,
        "签发机关":qianfa,"证件有效期":validate_date
        }


def match_xingshizheng(pos,value,save_path):
    chepaihaoma=id5.match_haoma(pos,value,save_path)
    cheliangleixing=id5.match_cheliangleixing(pos,value,save_path)
    suoyouren=id5.match_suoyouren(pos,value,save_path)
    zhuzhi=id5.match_address(pos,value,save_path)
    shiyongxingzhi=id5.match_shiyongxingzhi(pos,value,save_path)
    pinpaixinghao=id5.match_pinpaixinghao(pos,value,save_path)
    cheliangshibiedaihao=id5.match_cheliangshibiedaihao(pos,value,save_path)
    fadongjihao=id5.match_fadongjihaoma(pos,value,save_path)
    zhuceriqi=id5.match_zhucedate(pos,value,save_path)
    zairenshu=id5.match_zairenshu(pos,value,save_path)
    zongzhiliang=id5.match_weight_sum(pos,value,save_path)
    zhengbeizhiliang=id5.match_weight_zhengbei(pos,value,save_path)
    hedingzaizhiliang=id5.match_weight_heding(pos,value,save_path)
    chicun=id5.match_chicun(pos,value,save_path)
    youxiaoqi=id5.match_valid_date(pos,value,save_path)
    qianyin_weight=id5.match_weight_qianyin(pos,value,save_path)

    return {
        "车牌号码":chepaihaoma,"车辆类型":cheliangleixing,
        "所有人":suoyouren,"住址":zhuzhi,"使用性质":shiyongxingzhi,
        "品牌型号":pinpaixinghao,"车辆识别代号":cheliangshibiedaihao,
        "发动机号":fadongjihao,"注册日期":zhuceriqi,"核定载人数":zairenshu,
        "总质量":zongzhiliang,"整备质量":zhengbeizhiliang,"核定载质量":hedingzaizhiliang,
        "牵引总质量":qianyin_weight,"外廓尺寸":chicun,"有效期":youxiaoqi
        }

def match_jiashizheng(pos,value,save_path):
    name=id6.match_name(pos,value,save_path)
    sex=id6.match_sex(pos,value,save_path)
    address=id6.match_address(pos,value,save_path)
    chexing=id6.match_chexing(pos,value,save_path)
    zhenghao=id6.match_jiashizhenghao(pos,value,save_path)
    youxiaoqi=id6.match_valid_date(pos,value,save_path)


    return {
        "姓名":name,"性别":sex,"住址":address,
        "准驾车型":chexing,"证号":zhenghao,"有效期":youxiaoqi
    }


def match_tielu2(pos,value,save_path):
    yundan=id7.yundanhao(pos,value,save_path)
    chehao=id7.chezhong_chehao(pos,value,save_path)
    huowu=id7.match_huowumingcheng(pos,value,save_path)
    xuqiuhao=id7.match_xuqiuhao(pos,value,save_path)
    fazhan=id7.match_fazhan(pos,value,save_path)
    daozhan=id7.match_daozhan(pos,value,save_path)
    tuoyunmingcheng=id7.match_tuoyunmingcheng(pos,value,save_path)
    shouhuomingcheng=id7.match_shouhuomingcheng(pos,value,save_path)
    jianshu_all=id7.match_jianshu_all(pos,value,save_path)
    xianghao=id7.match_xianghao(pos,value,save_path)
    shifenghao=id7.match_shifenghao(pos,value,save_path)

    feimu,origin_feimu = id7.match_feimu(pos, value, save_path)
    jine = id7.match_jine(pos, value, save_path)
    shuie = id7.match_shuie(pos, value, save_path,jine_list=jine)

    jianshu_split=id7.match_jianshu_split(pos,value,save_path)
    baozhuang_split=id7.baozhuang_split(pos,value,save_path)
    zhongliang_split=id7.zhongliang_split(pos,value,save_path)
    xianglei_split=id7.xianglei_split(pos,value,save_path)
    quedingzhongliang_split=id7.quedingzhongliang_split(pos,value,save_path)
    tiji_split=id7.tiji_split(pos,value,save_path)
    yunjia_split=id7.yunjia_split(pos,value,save_path)
    jifeizhongliang_split=id7.jifeizhongliang_split(pos,value,save_path)
    baozhuang_all=id7.match_baozhuang_all(pos,value,save_path)
    huowujg_split=id7.huowujiage_split(pos,value,save_path)
    huowujg_all=id7.match_huowujiage_all(pos,value,save_path)
    zl_all=id7.match_zhongliang_all(pos,value,save_path)
    xl_all=id7.match_xinaglei_all(pos,value,save_path)
    xh_all=id7.match_xinaghap_all(pos,value,save_path)
    sfh_all=id7.match_shifeng_all(pos,value,save_path)
    qdzl_all=id7.match_quedingzl_all(pos,value,save_path)
    tj_all=id7.match_tiji_all(pos,value,save_path)
    yunjia_all=id7.match_yunjia_all(pos,value,save_path)
    jifei_all=id7.match_jifeizl_all(pos,value,save_path)
    feimu_detail=id7.match_feimu_detail(feimu,jine,shuie)
    tuoyunren=id7.match_tuoyunren(pos,value,save_path)
    tuoyun_phone=id7.match_phone_tuoyun(pos,value,save_path)
    shouhuoren=id7.match_shouhuoren(pos,value,save_path)
    shouhuo_phone = id7.match_phone_shouhuo(pos, value, save_path)

    d = [{} for i in range(len(huowu))]
    for i in range(len(huowu)):
        d[i]['货物名称']=huowu[i]
        if len(jianshu_split)!=len(huowu):
            d[i]['件数']='None'
        else:
            d[i]['件数']=jianshu_split[i]
        if len(baozhuang_split)!=len(huowu):
            d[i]['包装']='None'
        else:
            d[i]['包装']=baozhuang_split[i]
        
        if len(huowujg_split)!=len(huowu):
            d[i]['货物价格']='None'
        else:
            d[i]['货物价格']=huowujg_split[i]

        if len(zhongliang_split)!=len(huowu):
            d[i]['重量']='None'
        else:
            d[i]['重量']=zhongliang_split[i]

        if len(xianglei_split)!=len(huowu):
            d[i]['箱型箱类']='None'
        else:
            d[i]['箱型箱类']=xianglei_split[i]

        if len(xianghao)!=len(huowu):
            d[i]['箱号']='None'
        else:
            d[i]['箱号']=xianghao[i]
        
        if len(shifenghao)!=len(huowu):
            d[i]['施封号']='None'
        else:
            d[i]['施封号']=shifenghao[i]
        
        if len(quedingzhongliang_split)!=len(huowu):
            d[i]['确定重量']='None'
        else:
            d[i]['确定重量']=quedingzhongliang_split[i]
        
        if len(tiji_split)!=len(huowu):
            d[i]['体积']='None'
        else:
            d[i]['体积']=tiji_split[i]

        if len(yunjia_split)!=len(huowu):
            d[i]['运价号']=yunjia_split[0]
        else:
            d[i]['运价号']=yunjia_split[i]

        if len(jifeizhongliang_split)!=len(huowu):
            d[i]['计费重量']='None'
        else:
            d[i]['计费重量']=jifeizhongliang_split[i]
    
    hejixinxi=[{
        '件数':jianshu_all,'包装':baozhuang_all,
        '货物价格':huowujg_all,'重量':zl_all,'箱型箱类':xl_all,
        '箱号':xh_all,'集装箱施封号':sfh_all,'承运人确定重量':qdzl_all,
        '体积':tj_all,'运价号':yunjia_split[0],'计费重量':jifei_all
    }]

    return {
        "需求号":xuqiuhao,
        '车种车号':chehao,
        '运单号':yundan,
        "托运名称":tuoyunmingcheng,"发站":fazhan,
        "托运联系人":tuoyunren,"托运联系人电话":tuoyun_phone,
        "收货名称":shouhuomingcheng,"到站":daozhan,
        "收货联系人": shouhuoren, "收货联系人电话": shouhuo_phone,
        '货物明细信息':d,'货物合计信息':hejixinxi,'费目信息':feimu_detail
    }

def match_daoluyunshujingyingzigezheg(pos,value,save_path):
    haoma=id9.match_yunshuzhenghao(pos,value,save_path)
    yehu=id9.match_yehumingcheng(pos,value,save_path)
    dizhi=id9.match_address(pos,value,save_path)
    jingjixingzhi=id9.match_jingjixingzhi(pos,value,save_path)
    jingyingfanwei=id9.match_jingyingfanwei(pos,value,save_path)
    youxiaoqi=id9.match_youxiaoqi(pos,value,save_path)

    return {
        '号码':haoma,"业户名称":yehu,"地址":dizhi,"经济性质":jingjixingzhi,
        "经营范围":jingyingfanwei,"有效期":youxiaoqi
    }

def match_yingyezhizhao(pos,value,save_path):
    mingcheng=id10.match_mingcheng(pos,value,save_path)
    daima=id10.match_daima2(pos,value,save_path)
    leixing=id10.match_leixing(pos,value,save_path)
    daibiaoren=id10.match_daibiaoren(pos,value,save_path)
    zhucechengben=id10.match_zhucechengben(pos,value,save_path)
    chengliriqi=id10.match_chengliriqi(pos,value,save_path)
    yingyeqixian=id10.match_yingyeqixian(pos,value,save_path)
    jingyingfanwei=id10.match_jingyingfanwei(pos,value,save_path)

    return {
        "名称":mingcheng,"代码":daima,"类型":leixing,"代表人":daibiaoren,"注册成本":zhucechengben,
        "成立日期":chengliriqi,"营业期限":yingyeqixian,"经营范围":jingyingfanwei
    }

def match_congyezigezheng(pos,value,save_path):
    
    xingming=id11.match_name(pos,value,save_path)
    # xingbie=id11.match_sex(pos,value,save_path)
    shenfenzhenghao=id11.match_shenfenzhenghao(pos,value,save_path)
    danganhao=id11.match_dangan(pos,value,save_path)
    congyeleibie=id11.match_congyezigeleibie(pos,value,save_path)
    youxiaoqi=id11.match_validate_date(pos,value,save_path)
    # chuci=id11.match_riqi(pos,value,save_path)

    return {
        "姓名":xingming,"身份证号":shenfenzhenghao,
        "档案号":danganhao,"从业类别":congyeleibie,"有效期":youxiaoqi
    }

def match_daoluyunshu(pos,value,save_path):
    
    yunshuzhenghao=id12.match_zhenghao(pos,value,save_path)
    yehumingcheng=id12.match_yehumingcheng(pos,value,save_path)
    dizhi=id12.match_dizhi(pos,value,save_path)
    chepaihaoma=id12.match_chepaihaoma(pos,value,save_path)
    jingyingxukezhenghao=id12.match_jingyingxukezheng(pos,value,save_path)
    jingyingleixing=id12.match_jingyingleixing(pos,value,save_path)
    cheliangleixing=id12.match_cheliangleixing(pos,value,save_path)
    dunwei=id12.match_dunwei(pos,value,save_path)
    chicun=id12.match_chicun(pos,value,save_path)

    
    return {
        "运输证号":yunshuzhenghao,"业户名称":yehumingcheng,"地址":dizhi,"车牌号码":chepaihaoma,
        "经营许可证号":jingyingxukezhenghao,"经营类型":jingyingleixing,"车辆类型":cheliangleixing,
        "吨位":dunwei,"尺寸":chicun
    }


def match_xiahuozhi(pos,value,save_path):
    hangming=id13.match_hangming(pos,value,save_path)
    hangci=id13.match_hangci(pos,value,save_path)
    tidanhao=id13.match_tidanhao(pos,value,save_path)
    zhongliang=id13.match_zhongliang(pos,value,save_path)
    mudigang=id13.match_mudigang(pos,value,save_path)
    huoming=id13.match_huoming(pos,value,save_path)
    chicun=id13.match_chicun(pos,value,save_path)
    jianshu,leixing=id13.jianshu_xiangxing(pos,value,save_path)
    return {
        "航名":hangming,"航次":hangci,"提单号":tidanhao,"箱型":leixing,"重量":zhongliang,
        "目的港":mudigang,"货名":huoming,"件数":jianshu,"尺寸":chicun
    }

def match_haiyun(pos,value,Type,save_path):
    if Type=='rizhao':
        tidanhao=id8.match_tidanhao_rizhao(pos,value,save_path)
        dingcanghao=id8.match_dingcanghao_rizhao(pos,value,save_path)
    else:
        tidanhao=id8.match_tidanhao(pos,value,save_path)
        dingcanghao=id8.match_dingcanghao(pos,value,save_path)

    return {
        "提单号":tidanhao,"订舱号":dingcanghao
    }

def match_guobangdan(pos,value,save_path):
    fahuodanwei=id14.match_fahuodanwei(pos,value,save_path)
    shouhuodanwei=id14.match_shouhuodanwei(pos,value,save_path)
    wuliao=id14.match_wuliao(pos,value,save_path)
    chehao=id14.match_chehao(pos,value,save_path)
    jinchang_weight=id14.match_jinchangzhongliang(pos,value,save_path)
    chuchang_weight=id14.match_chuchangzhongliang(pos,value,save_path)
    jing_weight=id14.match_jingzhong(pos,value,save_path)

    return {
        "发货单位":fahuodanwei,"收货单位":shouhuodanwei,
        "物料名称":wuliao,"车号":chehao,
        "进厂重量":jinchang_weight,"出厂重量":chuchang_weight,
        "净重":jing_weight
    }

def match_jizhuangxiang(pos,value,save_path):
    xianghao=id15.match_xianghao(pos,value,save_path)
    max=id15.match_MAXGROSS(pos,value,save_path)
    tare=id15.match_TARE(pos,value,save_path)
    net=id15.match_NET(pos,value,save_path)

    return {
        "箱号":xianghao,
        "MAX GROSS":max,"TARE":tare,"NET":net
    }