import re
from LAC import LAC
import cv2
import sys

sys.path.append('../')
from component_modules import autils


# def ReRec2(path, ymin, ymax, xmin, xmax):
#     image = cv2.imread(path)
#     cropImg = image[int(ymin):int(ymax), int(xmin):int(xmax)]
#     cv2.imwrite('new.png', cropImg)
#     pos, value = autils.detect_img(cropImg)
#     return pos, value


lac = LAC(mode="lac")
shenfenzheng = r'^([1-9]\d{5}[12]\d{3}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])\d{3}[0-9xX])$'
minzu = [
    '汉', '蒙古', '回', '藏', '维吾尔', '苗', '彝', '壮', '布依', '朝鲜', '满', '侗', '瑶', '白',
    '土家', '哈尼', '哈萨克', '傣', '黎', '傈僳', '佤', '畲', '高山', '拉祜', '水', '东乡', '纳西',
    '景颇', '柯尔克孜', '土', '达斡尔', '仫佬', '羌', '布朗', '撒拉', '毛南', '仡佬', '锡伯', '阿昌',
    '普米', '塔吉克', '怒', '乌孜别克', '俄罗斯', '鄂温克', '德昂', '保安', '裕固', '京', '塔塔尔', '独龙',
    '鄂伦春', '赫哲', '门巴', '珞巴', '基诺'
]
area = {
    '11': '北京市',
    '12': '天津市',
    '13': '河北省',
    '14': '山西省',
    '15': '内蒙古自治区',
    '21': '辽宁省',
    '22': '吉林省',
    '23': '黑龙江省',
    '31': '上海市',
    '32': '江苏省',
    '33': '浙江省',
    '34': '安徽省',
    '35': '福建省',
    '36': '江西省',
    '37': '山东省',
    '41': '河南省',
    '42': '湖北省',
    '43': '湖南省',
    '44': '广东省',
    '45': '广西壮族自治区',
    '46': '海南省',
    '50': '重庆市',
    '51': '四川省',
    '52': '贵州省',
    '53': '云南省',
    '54': '西藏自治区',
    '61': '陕西省',
    '62': '甘肃省',
    '63': '青海省',
    '64': '宁夏回族自治区',
    '65': '新疆维吾尔族自治区',
    '81': '香港特别行政区',
    '82': '澳门特别行政区',
    '83': '台湾地区'
}  #全国省的字典,全局变量
pattern = r'[赵|钱|孙|李|周|吴|郑|王|冯|陈|褚|卫|蒋|沈|韩|杨|朱|秦|尤|许|何|吕|施|张|孔|曹|严|华|金|魏|陶|姜|戚|谢|邹|喻|柏|水|窦|章|云|苏|潘|葛|奚|范|彭|郎|鲁|韦|昌|马|苗|凤|花|方|俞|任|袁|柳|酆|鲍|史|唐|费|廉|岑|薛|雷|贺|倪|汤|滕|殷|罗|毕|郝|邬|安|常|乐|于|时|傅|皮|卞|齐|康|伍|余|元|卜|顾|孟|平|黄|和|穆|萧|尹|姚|邵|湛|汪|祁|毛|禹|狄|米|贝|明|臧|计|伏|成|戴|谈|宋|茅|庞|熊|纪|舒|屈|项|祝|董|梁|杜|阮|蓝|闵|席|季|麻|强|贾|路|娄|危|江|童|颜|郭|梅|盛|林|刁|锺|徐|邱|骆|高|夏|蔡|田|樊|胡|凌|霍|虞|万|支|柯|昝|管|卢|莫|经|房|裘|缪|干|解|应|宗|丁|宣|贲|邓|郁|单|杭|洪|包|诸|左|石|崔|吉|钮|龚|程|嵇|邢|滑|裴|陆|荣|翁|荀|羊|於|惠|甄|麴|家|封|芮|羿|储|靳|汲|邴|糜|松|井|段|富|巫|乌|焦|巴|弓|牧|隗|山|谷|车|侯|宓|蓬|全|郗|班|仰|秋|仲|伊|宫|宁|仇|栾|暴|甘|钭|历|戎|祖|武|符|刘|景|詹|束|龙|叶|幸|司|韶|郜|黎|溥|印|宿|白|怀|蒲|邰|从|鄂|索|咸|籍|卓|蔺|屠|蒙|池|乔|阳|郁|胥|能|苍|双|闻|莘|党|翟|谭|贡|劳|逄|姬|申|扶|堵|冉|宰|郦|雍|却|桑|桂|濮|牛|寿|通|边|扈|燕|冀|浦|尚|农|温|别|庄|晏|柴|瞿|充|慕|连|茹|习|宦|艾|鱼|容|向|古|易|慎|戈|廖|庾|终|暨|居|衡|步|都|耿|满|弘|匡|国|文|寇|广|禄|阙|东|欧|沃|利|蔚|越|夔|隆|师|巩|厍|聂|晁|勾|敖|融|冷|訾|辛|阚|那|简|饶|空|曾|毋|沙|乜|养|鞠|须|丰|巢|关|蒯|相|荆|红|游|竺|权|司马|上官|欧阳|夏侯|诸葛|闻人|东方|赫连|皇甫|尉迟|公羊|澹台|公冶宗政|濮阳|淳于|单于|太叔|申屠|公孙|仲孙|轩辕|令狐|钟离|宇文|长孙|慕容|司徒|司空|召|有|舜|岳|黄辰|寸|贰|皇|侨|彤|竭|端|赫|实|甫|集|象|翠|狂|辟|典|良|函|芒|苦|其|京|中|夕|乌孙|完颜|富察|费莫|蹇|称|诺|来|多|繁|戊|朴|回|毓|鉏|税|荤|靖|绪|愈|硕|牢|买|但|巧|枚|撒|泰|秘|亥|绍|以|壬|森|斋|释|奕|姒|朋|求|羽|用|占|真|穰|翦|闾|漆|贵|代|贯|旁|崇|栋|告|休|褒|谏|锐|皋|闳|在|歧|禾|示|是|委|钊|频|嬴|呼|大|威|昂|律|冒|保|系|抄|定|化|莱|校|么|抗|祢|綦|悟|宏|功|庚|务|敏|捷|拱|兆|丑|丙|畅|苟|随|类|卯|俟|友|答|乙|允|甲|留|尾|佼|玄|乘|裔|延|植|环|矫|赛|昔|侍|度|旷|遇|偶|前|由|咎|塞|敛|受|泷|袭|衅|叔|圣|御|夫|仆|镇|藩|邸|府|掌|首|员|焉|戏|可|智|尔|凭|悉|进|笃|厚|仁|业|肇|资|合|仍|九|衷|哀|刑|俎|仵|圭|夷|徭|蛮|汗|孛|乾|帖|罕|洛|淦|洋|邶|郸|郯|邗|邛|剑|虢|隋|蒿|茆|菅|苌|树|桐|锁|钟|机|盘|铎|斛|玉|线|针|箕|庹|绳|磨|蒉|瓮|弭|刀|疏|牵|浑|恽|势|世|仝|同|蚁|止|戢|睢|冼|种|涂|肖|己|泣|潜|卷|脱|谬|蹉|赧|浮|顿|说|次|错|念|夙|斯|完|丹|表|聊|源|姓|吾|寻|展|出|不|户|闭|才|无|书|学|愚|本|性|雪|霜|烟|寒|少|字|桥|板|斐|独|千|诗|嘉|扬|善|揭|祈|析|赤|紫|青|柔|刚|奇|拜|佛|陀|弥|阿|素|长|僧|隐|仙|隽|宇|祭|酒|淡|塔|琦|闪|始|星|南|天|接|波|碧|速|禚|腾|潮|镜|似|澄|潭|謇|纵|渠|奈|风|春|濯|沐|茂|英|兰|檀|藤|枝|检|生|折|登|驹|骑|貊|虎|肥|鹿|雀|野|禽|飞|节|宜|鲜|粟|栗|豆|帛|官|布|衣|藏|宝|钞|银|门|盈|庆|喜|及|普|建|营|巨|望|希|道|载|声|漫|犁|力|贸|勤|革|改|兴|亓|睦|修|信|闽|北|守|坚|勇|汉|练|尉|士|旅|五|令|将|旗|军|行|奉|敬|恭|仪|母|堂|丘|义|礼|慈|孝|理|伦|卿|问|永|辉|位|让|尧|依|犹|介|承|市|所|苑|杞|剧|第|零|谌|招|续|达|忻|六|鄞|战|迟|候|宛|励|粘|萨|邝|覃|辜|初|楼|城|区|局|台|原|考|妫|纳|泉|老|清|德|卑|过|麦|曲|竹|百|福|言|第五|佟|爱|年|笪|谯|哈|墨|连|南宫|赏|伯|佴|佘|牟|商|西门|东门|左丘|梁丘|琴|后|况|亢|缑|帅|微生|羊舌|海|归|呼延|南门|东郭|百里|钦|鄢|汝|法|闫|楚|晋|谷梁|宰父|夹谷|拓跋|壤驷|乐正|漆雕|公西|巫马|端木|颛孙|子车|督|仉|司寇|亓官|三小|鲜于|锺离|盖|逯|库|郏|逢|阴|薄|厉|稽|闾丘|公良|段干|开|光|操|瑞|眭|泥|运|摩|伟|铁|迮][\u4e00-\u9fa5]{1,3}$'


def match_minzu(pos, value, save_path):
    for i in range(len(minzu)):
        for j in range(len(pos)):
            if minzu[i] in value[j]:
                return minzu[i]
    else:
        return '汉'


def match_address(pos, value, save_path):
    for i in range(len(pos)):
        if '住址' in value[i] or '住' in value[i] or '址' in value[
                i] or '佳址' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            pos, result = autils.ReRec2(save_path, ymin - img_height,
                                 ymax + img_height * 3, xmin,
                                 xmax + img_width * 20)
            result = ''.join(result)

            if '住址' in result or '住' in result or '址' or '佳' in result:
                return re.sub(r'[住址佳]*', '', result)
            else:
                return result
        elif '公民身份号码' in value[i] or '公民身份' in value[i]:
            address = []
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - width < pos[i][0][0] < shr_pos[1][
                        0] + width and shr_pos[1][1] - height * 7 < pos[i][0][
                            1] < shr_pos[1][1] - height:
                    address.append(value[i])
            if len(address) > 0:
                a = ''.join(address)
                if '住址' in a or '住' in a or '址' or '佳' in a:
                    return re.sub(r'[住址佳]*', '', a)
                else:
                    return 'a'
            else:
                return '无'
    else:
        return '无'


def match_name_LAC(pos, value, save_path):
    user_name_list = []
    for i in range(len(pos)):
        lac_result = lac.run(value[i])
        for index, lac_label in enumerate(lac_result[1]):
            if lac_label == "PER":
                user_name_list.append(lac_result[0][index])

    if len(user_name_list) != 0:
        return user_name_list[0]


def match_name_single(pos, value, save_path):
    for i in range(len(pos)):
        if '姓名' in value[i] or '姓' in value[i] or '名' in value[i]:
            ymin = pos[i][0][1]
            ymax = pos[i][2][1]
            xmin = pos[i][0][0]
            xmax = pos[i][2][0]
            img_height = pos[i][3][1] - pos[i][0][1]
            img_width = pos[i][1][0] - pos[i][0][0]
            pos, result = autils.ReRec2(save_path, ymin - img_height * 1.4,
                                 ymax + img_height, xmin,
                                 xmax + img_width * 10)
            result = ''.join(result)
            return re.sub(r'[姓名]*', '', result)


def match_name(pos, value, save_path):
    for i in range(len(pos)):
        if '姓名' in value[i] or '姓' in value[i] or '名' in value[i]:
            if len(value[i].split('名')[-1]) > 1 and value[i].split(
                    '名')[0] == '姓' or value[i].split('名')[0] == '理':
                return value[i].split('名')[-1]
            else:
                result = match_name_single(pos, value, save_path)
                return result
        elif '姓名' in value[i] or '姓' in value[i] or '名' in value[i]:
            shr_pos = pos[i]
            height = pos[i][3][1] - pos[i][0][1]
            width = pos[i][1][0] - pos[i][0][0]
            for i in range(len(pos)):
                if shr_pos[1][0] - int(width / 2) < pos[i][0][0] < shr_pos[1][
                        0] + int(2 * width) and shr_pos[1][1] - int(
                            2 *
                            height) < pos[i][0][1] < shr_pos[1][1] + height:
                    return value[i]
        else:
            name = match_name_LAC(pos, value, save_path)
            return name


def id_loc(number):  #地区切片
    loc = number[0:2]  #前2位
    return area[loc]


def match_sex(pos, value, save_path):
    for i in range(len(pos)):
        if '性别' in value[i] or '别' in value[i]:
            if len(value[i].split('别')[-1]) >= 1:
                if '男' in value[i]:
                    return '男'
                else:
                    return '女'
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - width / 2 < pos[i][0][
                            0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[0][1] - height < pos[i][
                                    0][1] < shr_pos[3][1] + height:
                        if '男' in value[i]:
                            return '男'
                        else:
                            return '女'
        elif '别' in value[i] and len(value[i].split('别')) >= 1:
            if '男' in value[i]:
                return '男'
            else:
                return '女'

        else:
            id = match_idnumber(pos, value, save_path)
            if id[1] is not None:
                if len(id[0]) == 18:
                    if int(id[0][-2]) % 2 == 0:
                        return '女'
                    elif int(id[0][-2]) % 2 != 0:
                        return '男'
                    


def match_id(pos, value, save_path):
    for i in range(len(pos)):
        if value[i].isdigit() and len(value[i]) > 10:
            return value[i]
        elif '码' in value[i] and len(value[i].split('码')[-1]) > 10:
            return value[i].split('码')[-1]


def match_born(pos, value, save_path):
    for i in range(len(pos)):
        if '年' in value[i]:
            return value[i][value[i].index('年') - 4:]


def match_idnumber(pos, value, save_path):
    for i in range(len(pos)):
        if '身份号码' in value[i]:
            if len(value[i].split('码')[-1]) > 5:
                id = value[i].split('码')[-1]
                if len(id) < 18:
                    date = match_born(pos, value, save_path)
                else:
                    year = value[i].split('码')[-1][6:10]
                    month = value[i].split('码')[-1][10:12]
                    date = value[i].split('码')[-1][12:14]
                    date = "%s年%s月%s日" % (year, month, date)
                return date, id

        elif re.match(shenfenzheng, value[i]):
            id = value[i]
            if len(id) < 18:
                date = match_born(pos, value, save_path)
            else:
                year = value[i][6:10]
                month = value[i][10:12]
                date = value[i][12:14]
                date = "%s年%s月%s日" % (year, month, date)
            return id, date
        else:
            born = match_born(pos, value, save_path)
            idnumber = match_id(pos, value, save_path)
            return born, idnumber
    else:
        return 'None', 'None'


def match_validdate(pos, value, save_path):
    for i in range(len(pos)):
        if '有效期限' in value[i] or '期限' in value[i]:
            if len(value[i].split('限')[-1]) > 4:
                return value[i].split('限')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[1][1] - height < pos[i][
                                    0][1] < shr_pos[1][1] + height:
                        return value[i]
        if '.' in value[i] and value[i].split(
                '.')[0][-1].isdigit() and '-' in value[i]:
            return value[i]


def match_qianfa(pos, value, save_path):
    for i in range(len(pos)):
        if '签发' in value[i] and '关' in value[i]:
            if len(value[i].split('关')[-1]) > 4:
                return value[i].split('关')[-1]
            else:
                shr_pos = pos[i]
                height = pos[i][3][1] - pos[i][0][1]
                width = pos[i][1][0] - pos[i][0][0]
                for i in range(len(pos)):
                    if shr_pos[1][0] - int(
                            width / 2) < pos[i][0][0] < shr_pos[1][0] + int(
                                2 * width) and shr_pos[1][1] - int(
                                    2 * height
                                ) < pos[i][0][1] < shr_pos[1][1] + height:
                        return value[i]
