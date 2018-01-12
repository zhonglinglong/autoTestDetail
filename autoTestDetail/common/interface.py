# -*- coding:utf8 -*-
import collections

from common.base import consoleLog
from common.base import solr
from common.base import get_conf, get_randomString, set_conf
from common import sqlbase
from common import datetimes
import requests, json, time, random, re


user, pwd = get_conf('loginUser', 'user'), get_conf('loginUser', 'pwd')

def myRequest(url,data=None, needCookie=True, contentType='application/json', method='post', returnValue=False):
    headers = {
        'content-type' : contentType,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    host = 'http://isz.ishangzu.com/'
    interfaceURL = host+url
    cookie = eval(get_conf('cookieInfo', 'cookies'))
    if method == 'get':
        if needCookie:
            request = requests.get(url, cookie=cookie)
        else:
            request = requests.get(url)
    if method == 'post':
        if needCookie:
            request = requests.post(interfaceURL, data=json.dumps(data), headers=headers, cookies=cookie)
        else:
            request = requests.post(interfaceURL, data=json.dumps(data), headers=headers)
    result = json.loads(request.text)
    if request.status_code is not 200 or result['code'] is -1:
        if result['type'] == 'ok' or u'验证码发送过于频繁' in result['msg'] or u'密码错误' in result['msg']:
            return result
        msg = result['msg'].encode('utf-8')
        consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (interfaceURL, data, msg.decode('utf-8')), 'w')
        return False if not returnValue else msg
    else:
        return result

def get_cookie():
    needClient = None
    #默认登录不使用客户端，如果报错，则赋值给needClient为True，然后调用客户端的登录接口进行校验
    url = 'http://isz.ishangzu.com/isz_base/LoginController/login.action'
    data = {
        'user_phone': user, 'user_pwd': pwd, 'auth_code': '', 'LechuuPlatform': 'LECHUU_CUSTOMER',
        'version': '1.0.0'
    }
    headers = {
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    result = json.loads(response.text)
    if result['msg'] == u'登录成功' or result['msg'] == u'非生产环境,不做校验！':
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        set_conf('cookieInfo', cookies=cookies)
    elif u'密码错误' in result['msg']:
        msg = result['msg'].encode('utf-8')
        consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
        raise
    else:
        needClient = True

    if needClient:
        from common.getAuthKey import getAuthKey
        auth_key = getAuthKey()
        # 检查授权
        url = 'isz_base/LoginAuthController/checkLoginAuth.action'
        data ={'auth_key': auth_key}
        result = myRequest(url, data, needCookie=False)
        if u'授权成功' in result['msg']:
            auth_code = result['obj']['authList'][0]['auth_code']
            authTag = result['obj']['authTag']
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第一步：检查授权失败'

        # 检查用户名密码
        url = 'isz_base/LoginController/checkUserPassWord.action'
        data = {
            'auth_code': auth_key,
            'authTag': authTag,
            'user_phone': user, 'user_pwd': pwd
        }
        result = myRequest(url, data, needCookie=False)
        if u'用户名密码正确' not in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第二步：检查用户名密码失败'

        # 获取短信验证码
        url = 'isz_base/LoginController/getVerificationCode.action'
        data = {
            'authTag': authTag,
            'mobile': user
        }
        result = myRequest(url, data, needCookie=False)
        if result['msg'] != 'ok' and u'验证码发送过于频繁' not in result['msg']:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第三步：获取短信验证码失败'

        # 验证码登录
        url = 'isz_base/LoginController/checkVerificationCode.action'
        data = {
            'auth_code': auth_key,
            'authTag': authTag,
            'user_phone': user,
            'user_pwd': pwd,
            'verificationCode': '0451'
        }
        # 判断是否是开发部，然后决定验证码是默认的0451还是从数据库查最新收到的
        if myRequest(url, data, needCookie=False):
            sql = "select * from sys_department_flat where dept_id=(SELECT dep_id from sys_department where dep_name = '技术开发中心') and child_id=(" \
                  "SELECT dep_id from sys_user where user_phone = '%s' and user_status = 'INCUMBENCY')" % user
            if sqlbase.get_count(sql) == 0:
                content = sqlbase.serach("SELECT content from sms_mt_his where destPhone = '%s' ORDER BY create_time desc limit 1" % user)[0]
                sms_code = re.findall('验证码：(.*?)，', content.encode('utf-8'))[0]
                data['verificationCode'] = sms_code
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        }
        url = 'http://isz.ishangzu.com/isz_base/LoginController/checkVerificationCode.action'
        response = requests.post(url, data=json.dumps(data), headers=headers)
        result = json.loads(response.text)
        if result['msg'] == 'ok':
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            print cookies
            set_conf('cookieInfo', cookies=cookies)
        else:
            msg = result['msg'].encode('utf-8')
            consoleLog(u'接口异常！\n接口地址：%s\n请求参数：%s\n返回结果：%s' % (url, data, msg.decode('utf-8')), 'w')
            raise u'客户端登录第四步：验证码登录失败'

def delNull(data):
    """删除字典中为null的值"""
    def typeDict(data):
        for x,y in data.items():
            if y is None:
                del data[x]
            elif type(y) is list:
                typeList(data[x])
            elif type(y) is dict:
                typeDict(data[x])

    def typeList(data):
        for x,y in enumerate(data):
            if type(y) is dict:
                typeDict(data[x])
            if y is None:
                del data[x]
    typeDict(data) if type(data) is dict else typeList(data)
    return data

def creatResidential():
    url = 'isz_house/ResidentialController/saveResidential.action'
    residentialName = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S')
    sql = "SELECT sd.parent_id from sys_department sd INNER JOIN sys_user sur on sur.dep_id = sd.dep_id INNER JOIN sys_position spt on spt.position_id = sur.position_id " \
            "where sd.dep_district = '330100' and sd.dep_id <> '00000000000000000000000000000000' and (spt.position_name like '资产管家%' or spt.position_name like '综合管家%') " \
            "ORDER BY RAND() LIMIT 1"
    dutyDepID = sqlbase.serach(sql)[0]
    data = {
        "residential_name":residentialName,
        "residential_jianpin":"auto",
        "city_code":"330100",
        "area_code":"330108",
        "taBusinessCircleString":"4",
        "address":"autoTest",
        "gd_lng":"120.138631",
        "gd_lat":"30.186537",
        "property_type":"ordinary",
        "taDepartString":dutyDepID,
        "byname":"auto"
    }
    result = myRequest(url,data)
    if result:
        sql = "SELECT residential_id from residential where residential_name = '%s'" % residentialName
        residentialID = sqlbase.serach(sql)[0]
        residential = {'residentialName':residentialName,'residentialID':residentialID,'dutyDepID':dutyDepID}
        return residential

def creatBuilding():
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingNew.action'
    residential = creatResidential()
    buildingName = 'buiding'
    data = {
        "property_name":residential['residentialName'],
        "building_name":buildingName,
        "no_building":u"无",
        "housing_type":"ordinary",
        "residential_id":residential['residentialID'],
        "have_elevator":"Y"
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT building_id from residential_building where residential_id = '%s'" % residential['residentialID']
        buildingID = sqlbase.serach(sql)[0]
        residential['buildingID'] = buildingID
        residential['buildingName'] = buildingName
        return residential

def creatUnit():
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingUnit.action'
    residential = creatBuilding()
    unitName = 'unit'
    data = {
        "property_name": residential['residentialName']+residential['buildingName'],
        "unit_name": unitName,
        "no_unit": u"无",
        "building_id": residential['buildingID']
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT unit_id from residential_building_unit where building_id = '%s'" % residential['buildingID']
        unitID = sqlbase.serach(sql)[0]
        residential['unitID'] = unitID
        residential['unitName'] = unitName
        return residential

def creatFloor():
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingFloor.action'
    residential = creatUnit()
    floorName = 'floor'
    data = {
        "property_name": residential['residentialName'] + residential['buildingName'] + residential['unitName'],
        "floor_name": floorName,
        "unit_id": residential['unitID'],
        "building_id": residential['buildingID']
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT floor_id from residential_building_floor where building_id = '%s' and unit_id = '%s'" % (residential['buildingID'],residential['unitID'])
        floorID = sqlbase.serach(sql)[0]
        residential['floorID'] = floorID
        residential['floorName'] = floorName
        return residential

def creatHouseNum():
    url = 'isz_house/ResidentialBuildingController/saveResidentialBuildingHouseNo.action'
    residential = creatFloor()
    houseNumName = 'number'
    data = {
        "property_name": residential['residentialName'] + residential['buildingName'] + residential['unitName'] + residential['floorName'] + u'层',
        "rooms": "1", "livings": "1", "bathrooms": "1", "kitchens": "1", "balconys": "1", "build_area": "100.00","orientation": "NORTH",
        "house_no": houseNumName,
        "unit_id": residential['unitID'],
        "building_id": residential['buildingID'],
        "floor_id": residential['floorID']
    }
    result = myRequest(url, data)
    if result:
        sql = "SELECT house_no_id from residential_building_house_no where building_id = '%s' and unit_id = '%s' and floor_id = '%s'" % \
              (residential['buildingID'],residential['unitID'],residential['floorID'])
        houseNumID = sqlbase.serach(sql)[0]
        residential['houseNumID'] = houseNumID
        residential['houseNumName'] = houseNumName
        return residential

def addHouse():
    url = 'isz_house/HouseController/saveHouseDevelop.action'
    residential = creatHouseNum()
    personInfo = sqlbase.serach("select user_id,dep_id from sys_user where user_phone = '15168368432'")
    data = {
        "residential_name_search": residential['residentialID'],
        "building_name_search": residential['buildingID'],
        "unit_search": residential['unitID'],
        "house_no_search": residential['houseNumID'],
        "residential_name": residential['residentialName'],
        "building_name": residential['buildingName'],
        "unit": residential['unitName'],
        "floor": residential['floorName'],
        "house_no": residential['houseNumName'],
        "residential_address": u"杭州市 滨江区 浦沿 autoTest",
        "city_code": "330100",
        "area_code": "330108",
        "business_circle_id": "4",
        "contact": "test",
        "did": personInfo[1],
        "uid": personInfo[0],
        "house_status": "WAITING_RENT",
        "category": "NOLIMIT",
        "source": "INTRODUCE",
        "rental_price": "1234.00",
        "rooms": "1",
        "livings": "1",
        "kitchens": "1",
        "bathrooms": "1",
        "balconys": "1",
        "build_area": "100",
        "orientation": "NORTH",
        "residential_id": residential['residentialID'],
        "building_id": residential['buildingID'],
        "unit_id": residential['unitID'],
        "floor_id": residential['floorID'],
        "house_no_id": residential['houseNumID'],
        "business_circle_name": u"浦沿",
        "contact_tel": "15168368432"
    }
    result = myRequest(url, data)
    if result:
        sql = "select house_develop_id from house_develop where residential_id = '%s'" % residential['residentialID']
        houseDevelogID = sqlbase.serach(sql)[0]
        residential['houseDevelogID'] = houseDevelogID
        return residential

def auditHouse():
    url = 'isz_house/HouseController/auditHouseDevelop.action'
    houseInfo = addHouse()
    data = {
        "residential_name_search": houseInfo['residentialID'],
        "building_name_search": houseInfo['buildingID'],
        "unit_search": houseInfo['unitID'],
        "house_no_search": houseInfo['houseNumID'],
        "residential_name": houseInfo['residentialName'],
        "building_name": houseInfo['buildingName'],
        "floor": houseInfo['floorName'],
        "house_no_suffix": "xxx",
        "residential_address": u"杭州市 滨江区 浦沿 autoTest",
        "residential_department_did": houseInfo['dutyDepID'],
        "house_status": "WAITING_RENT",
        "category": "NOLIMIT",
        "rental_price": "1234.00",
        "build_area": "100.00",
        "rooms": "1",
        "livings": "1",
        "kitchens": "1",
        "bathrooms": "1",
        "balconys": "1",
        "orientation": "NORTH",
        "source": "INTRODUCE",
        "houseRent": {
            "house_status": "WAITING_RENT",
            "category": "NOLIMIT",
            "source": "INTRODUCE",
            "rental_price": "1234.00"
        }, "audit_status": "PASS",
        "building_id": houseInfo['buildingID'],
        "residential_id": houseInfo['residentialID'],
        "unit_id": houseInfo['unitID'],
        "unit": houseInfo['unitName'],
        "floor_id": houseInfo['floorID'],
        "house_no_id": houseInfo['houseNumID'],
        "house_no": houseInfo['houseNumName'],
        "area_code": "330108",
        "city_code": "330100",
        "house_develop_id": houseInfo['houseDevelogID'],
        "update_time":sqlbase.serach("SELECT update_time from house_develop where house_develop_id = '%s'" % houseInfo['houseDevelogID'])[0],
        #"update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "audit_content": u"同意"
    }
    result = myRequest(url, data)
    if result:
        sql = "select house_id,house_code from house where residential_id = '%s' and house_no_id = '%s'" % (houseInfo['residentialID'],houseInfo['houseNumID'])
        house = sqlbase.serach(sql)
        houseInfo['houseID'] = house[0]
        houseInfo['houseCode'] = house[1]
        # 避免等待时间太长，生成的房源没有出来，此处调用solr的增量操作
        solr('house', get_conf('testCondition', 'test'))
        return houseInfo

def addHouseContractAndFitment(apartment_type,entrust_type,sign_date,owner_sign_date,entrust_start_date,entrust_end_date,delay_date,free_start_date,free_end_date,first_pay_date,second_pay_date,
    rent,parking,year_service_fee,payment_cycle,freeType='STARTMONTH',fitment_start_date=None,fitment_end_date=None,contract_type='NEWSIGN',contract_id=None,rooms=None,
    fitmentCost=None,house_rent_price=None,houseInfo=None):
    #暂时先不考虑续签，所以不要用此接口做续签
    """
    新增委托合同以及分割交房之后同时定价
    :param apartment_type: 公寓类型
    :param entrust_type: 合同类型
    :param sign_date: 签约日期
    :param owner_sign_date: 业主交房日
    :param entrust_start_date: 委托起算日
    :param entrust_end_date: 委托到期日
    :param delay_date: 延长到期日
    :param free_start_date: 免租开始日
    :param free_end_date: 免租到期日
    :param first_pay_date: 首次付款日
    :param second_pay_date: 二次付款日
    :param rent: 房租
    :param parking:车位费
    :param year_service_fee:服务费
    :param payment_cycle:付款类型
    :param freeType:免租类型，默认为首月
    :param fitment_start_date:装修起算日，默认无
    :param fitment_end_date:装修结束日，默认无
    :param contract_type:合同类型，默认新签
    :param contract_id:续签情况下，要传递被续签的合同ID，默认无
    :param rooms:设计工程户型分割时，需要的房间数量，默认无
    :param fitmentCost:交房时的装修总成本，默认无
    :param house_rent_price:为合租时，此值为其中一个房源价格，整租直接为房源价格，此价格也为签约合同的出租价
    :return:合租返回其中一条公寓ID，整租直接返回公寓ID
    """
    if houseInfo == None:
        houseInfo = auditHouse()
    data = {}
    data['house_id'] = houseInfo['houseID']
    data['residential_id'] = houseInfo['residentialID']
    data['building_id'] = houseInfo['buildingID']
    data['property_type'] = 'HAVECARD'                                                              # 有产证商品房
    data['inside_space'] = '123'                                                                            # 使用面积
    data['pledge'] = '0'                                                                                        # 是否抵押
    data['apartment_type'] = apartment_type                                                      # 公寓类型
    data['reform_way'] = 'OLDRESTYLE' if apartment_type is 'BRAND' else 'UNRRESTYLE'   # 改造方式
    data['entrust_type'] = entrust_type                                                                # 合同类型
    data['contract_num'] = 'AutoTest' + '-' + time.strftime('%m%d-%H%M%S')+get_randomString()  # 合同编号
    data['sign_body'] = 'ISZPRO'                                                                          # 签约主体
    data['sign_date'] = sign_date                                                                         # 签约日期
    data['owner_sign_date'] = owner_sign_date                                                   # 业主交房日
    if fitment_start_date or fitment_end_date:
        data['fitment_start_date'] = fitment_start_date                                           # 装修起算日
        data['fitment_end_date'] = fitment_end_date                                             # 装修结束日
    data['entrust_start_date'] = entrust_start_date                                                # 委托起算日
    data['entrust_end_date'] = entrust_end_date                                                  # 委托到期日
    data['delay_date'] = delay_date                                                                      # 延长到期日
    data['freeType'] = freeType                                                                            # 免租类型
    data['free_start_date'] = free_start_date                                                          # 免租开始日
    data['free_end_date'] = free_end_date                                                           # 免租到期日
    data['first_pay_date'] = first_pay_date                                                             # 首次付款日
    data['second_pay_date'] = second_pay_date                                                   # 二次付款日
    data['rental_price'] = str(float(rent)+float(parking))                                         # 月租金
    data['rent'] = str(rent)                                                                                          # 房租
    data['property'] = '0.00'                                                                                  # 物业费
    data['energy_fee'] = '0.00'                                                                              #能耗费
    data['remember'] = '0'                                                                                   # 是否包含车位费，默认为0，程序写死
    data['parking'] = str(parking)                                                                          # 车位费
    data['deposit'] = '0.00'                                                                                    # 押金
    data['year_service_fee'] = str(year_service_fee)                                                      # 年服务费
    data['payment_cycle'] = payment_cycle                                                          # 付款类型
    data['property_company'] = '0.00'                                                                  # 需公司缴纳的物业费
    data['energy_company'] = '0.00'                                                                     # 需公司缴纳的能耗费
    data['remark'] = 'autotest'                                                                             # 备注
    data['account_name'] = '业主姓名'                                                                  # 收款人
    data['account_bank'] = u'支行'                                                                        # 支行
    data['account_num'] = '10086'                                                                       # 银行账号
    data['model'] = '5'                                                                                         #当前共有几个页面，判断是新增还是分别保存某个tab页面
    # 业主信息
    data['lords'] = [
        {
            'landlord_name': 'autoTest',  # 业主姓名
            'ownerCardType': u'身份证',  # 证件类型
            'id_card': '330122197012091969',  # 证件号码
            'phone': '15168368432',  # 联系电话
            'mailing_address': u'海创基地爱上租',  # 通讯地址
            'card_type': 'IDNO'  # 证件类型
        }
    ]
    # 紧急联系人信息
    data['emergency'] = {
        'emergency_name': 'auto',  # 姓名
        'emergency_phone': '15268843624',  # 电话
        'emergency_card_type': 'IDNO',  # 证件类型
        'emergency_id_card': '332521197002020427',  # 证件号
        'emergency_address': u'海创基地南楼三层爱上租'  # 通讯地址
    }
    # 签约人信息
    data['sign'] = {
        'card_type': 'IDNO',  # 证件类型
        'id_card': '330122197012091969',  # 证件号
        'sign_name': 'autoTest',  # 签约人姓名
        'phone': '15168368432',  # 联系电话
        'gender': 'MALE',  # 性别
        'sign_from': 'INTRODUCE',  # 业主来源
        'email': 'test@ishangzu.com',  # 邮箱
        'address': u'海创基地爱上租',  # 通讯地址
        'other_contact': '15268843624'  # 其他联系方式
    }

    def step1():
        # 添加房源信息以及签约人信息到请求参数中
        url = 'isz_contract/houseContractController/getHouseContractInfo.action'
        requestPayload = {"houseId":houseInfo['houseID']}
        result = myRequest(url, requestPayload)
        if result:
            data['city_code'] = result['obj']['city_code']
            data['area_code'] = result['obj']['area_code']
            data['contract_type'] = result['obj']['contract_type']
            data['house_code'] = result['obj']['house_code']
            data['property_address'] = result['obj']['property_address']
            data['production_address'] = result['obj']['production_address']
            data['sign_did'] = result['obj']['sign_did']
            data['sign_uid'] = result['obj']['sign_uid']
            data['create_name'] = result['obj']['create_name']

    def step2():
        # 添加租金策略到请求参数中
        url = 'isz_contract/houseContractController/createRentInfo.action'
        requestPayload = {
            "property": "0.00",             #需公司缴纳的物业费
            "energy_fee": "0.00",           #需公司缴纳的能耗费
            "parking": str(parking),
            "rent": str(rent),
            "year_service_fee": str(year_service_fee),
            "entrust_start_date": entrust_start_date,
            "entrust_end_date": entrust_end_date,
            "freeType": freeType,
            "free_start_date": free_start_date,
            "free_end_date": free_end_date,
            "payment_cycle": payment_cycle
        }
        result = myRequest(url, requestPayload)
        if result:
            data['hcris'] = []
            for x in range(len(result['obj'])):
                content = {
                    'details': result['obj'][x]['details'],
                    'end_date': result['obj'][x]['details'][0]['end_date'],
                    'free_end_date': result['obj'][x]['details'][0]['free_end_date'],
                    'free_start_date': result['obj'][x]['details'][0]['free_start_date'],
                    'start_date': result['obj'][x]['details'][0]['start_date']
                }
                data['hcris'].append(content)
            data['hcris'] = delNull(data['hcris'])

    def step3():
        # 添加租金明细到请求参数中
        url = 'isz_contract/houseContractController/createContractPayable.action'
        requestPayload = data['hcris']
        for x in requestPayload:
            for y in x['details']:
                y['deposit'] = '0.00'
                y['first_pay_date'] = first_pay_date
                y['second_pay_date'] = second_pay_date
        result = myRequest(url, requestPayload)
        if result:
            data['hcp'] = delNull(result['obj']['payables'])
            data['expenses'] = delNull(result['obj']['expenses'])

    def step4():
        # 续签情况下添加前合同数据导请求参数中
        url = 'isz_contract/houseContractController/getLandlordAndSign.action'
        requestPayload = {'contract_id':contract_id}
        result = myRequest(url,requestPayload)
        if result:
            pass

    if contract_type is 'NEWSIGN':
        step1()
        step2()
        step3()
    elif contract_type is 'RENEWSIGN':
        step2()
        step3()
        step4()

    url = 'isz_contract/houseContractController/saveOrUpdateHouseContract.action'
    result = myRequest(url,data)
    if result:
        houseContractInfo = sqlbase.serach("select contract_id,contract_num from house_contract where house_id = '%s' and deleted = 0 order by create_time desc limit 1" % houseInfo['houseID'])
        consoleLog(u'新签委托合同成功！合同编号 : %s' % houseContractInfo[1])

        def fitmentHouseAndSolr():
            """户型分割"""
            if apartment_type is 'BRAND' or apartment_type is 'MANAGE' and entrust_type is 'SHARE':
                url = 'isz_house/DesignController/breaksUpEntire.action'
                requestPayload = {
                    'house_id': houseInfo['houseID'],
                    'contract_id': houseContractInfo[0],
                    'apartment_type': apartment_type,
                    'rent_type': entrust_type,
                    'fitmentHouse': {
                        'house_id': houseInfo['houseID'],
                        'contract_id': houseContractInfo[0],
                        'reform_way': data['reform_way'],
                        'apartment_kind': 'DWELLING',  # 公寓名称
                        'fitment_style': 'SIMPLECHINESE',  # 装修风格
                        'rooms': '2' if rooms is None else str(rooms),
                        'livings': '1',
                        'kitchens': '1',
                        'bathrooms': '1',
                        'balconys': '1'
                    },
                    'fitmentRoomList': [
                        {
                            'houseRoom': {
                                # 公共区域配置
                                'houseRoomConfigurationList': [
                                    {'configuration_code': 'TV', 'owner_type': 'LANDLORD'},
                                    {'configuration_code': 'GAS_HEATER', 'owner_type': 'LANDLORD'},
                                    {'configuration_code': 'SOFAGROUP', 'owner_type': 'LANDLORD'},
                                    {'configuration_code': 'TV', 'owner_type': 'ISHANGZU'},
                                    {'configuration_code': 'GAS_HEATER', 'owner_type': 'ISHANGZU'},
                                    {'configuration_code': 'SOFAGROUP', 'owner_type': 'ISHANGZU'}
                                ],
                                'public_flag': 'Y'
                            }
                        }
                    ]
                }
                def addRoomsToRequestPayload():
                    """根据分割的房间数量，动态将房间数据添加至请求参数中"""
                    for i in range(rooms):
                        room_no = None
                        if i is 0:
                            room_no = 'METH'
                        if i is 1:
                            room_no = 'ETH'
                        if i is 2:
                            room_no = 'PROP'
                        if i is 3:
                            room_no = 'BUT'
                        if i is 4:
                            room_no = 'PENT'
                        if i is 5:
                            room_no = 'HEX'
                        if i is 6:
                            room_no = 'HEPT'
                        if i is 7:
                            room_no = 'OCT'
                        if i is 8:
                            room_no = 'NON'
                        if i is 9:
                            room_no = 'DEC'
                        content = {
                            'houseRoom': {
                                'houseRoomConfigurationList': [
                                    {'configuration_code': 'TV', 'owner_type': 'LANDLORD'},
                                    {'configuration_code': 'SOFAGROUP', 'owner_type': 'LANDLORD'},
                                    {'configuration_code': 'TV', 'owner_type': 'ISHANGZU'},
                                    {'configuration_code': 'SOFAGROUP', 'owner_type': 'ISHANGZU'}
                                ],
                                'public_flag': 'N',
                                'room_no': room_no,
                                'room_area': '28',
                                'room_orientation': 'NORTH'
                            }
                        }
                        requestPayload['fitmentRoomList'].append(content)
                if apartment_type is 'BRAND':
                    if entrust_type is 'SHARE':
                        addRoomsToRequestPayload()
                        result = myRequest(url,requestPayload)
                        if result:
                            consoleLog(u'委托合同 %s 已分割' % houseContractInfo[1])
                            sendOrder()
                            closingRoom()
                            return confirmPrice()
                    elif entrust_type is 'ENTIRE':
                        #没有房间（室）的概念，添加单一卧室的配置数据至请求参数中
                        content = {
                            'houseRoom':{
                                'houseRoomConfigurationList':[
                                    {'configuration_code':'TV','owner_type':'LANDLORD'},
                                    {'configuration_code': 'SOFAGROUP', 'owner_type': 'LANDLORD'},
                                    {'configuration_code': 'TV', 'owner_type': 'ISHANGZU'},
                                    {'configuration_code': 'SOFAGROUP', 'owner_type': 'ISHANGZU'}
                                ],
                                'public_flag':'N'
                            }
                        }
                        requestPayload['fitmentRoomList'].append(content)
                        requestPayload['fitmentHouse']['apartment_kind'] = 'WUSHE'
                        result = myRequest(url,requestPayload)
                        if result:
                            consoleLog(u'委托合同 %s 已分割' % houseContractInfo[1])
                            sendOrder()
                            closingRoom()
                            return confirmPrice()
                elif apartment_type is 'MANAGE' and entrust_type is 'SHARE':
                    addRoomsToRequestPayload()
                    result = myRequest(url,requestPayload)
                    requestPayload['fitmentHouse']['apartment_kind'] = 'SHARE'
                    del requestPayload['fitmentHouse']['fitment_style']
                    if result:
                        consoleLog(u'委托合同 %s 已分割' % houseContractInfo[1])
                        closingRoom()
                        return confirmPrice()
            else:
                return confirmPrice()

        def sendOrder():
            """派单"""
            sql = "SELECT su.user_id FROM sys_user su, sys_position sp,sys_department sd WHERE su.position_id = sp.position_id and su.dep_id = sd.dep_id and sd.dep_district = '330100' " \
                  "AND su.user_status = 'INCUMBENCY' AND sp.position_name LIKE '%品牌公寓专员%' LIMIT 1"
            user_id = sqlbase.serach(sql)[0]
            url = 'isz_house/DesignController/sendOrder.action'
            fitmentInfo = sqlbase.serach("select fitment_id,update_time from fitment_house where contract_id = '%s'" % houseContractInfo[0])
            requestPayload = {
                'fitment_id':fitmentInfo[0],
                'fitment_uid':user_id,
                'update_time':fitmentInfo[1]
            }
            result = myRequest(url,requestPayload)
            if result:
                consoleLog(u'委托合同 %s 已派单' % houseContractInfo[1])

        def closingRoom():
            """交房"""
            url = 'isz_house/DesignController/closingRoom.action'
            fitmentInfo = sqlbase.serach("select fitment_id,update_time from fitment_house where contract_id = '%s'" % houseContractInfo[0])
            requestPayload = {
                'fitment_id': fitmentInfo[0],
                'decorate_start_date':time.strftime('%Y-%m-%d'),
                'hard_delivery_date': time.strftime('%Y-%m-%d'),
                'set_delivery_date': time.strftime('%Y-%m-%d'),
                'update_time': fitmentInfo[1],
                'total_cost':str(fitmentCost)
            }
            if apartment_type is 'MANAGE' and entrust_type is 'SHARE':
                del requestPayload['decorate_start_date']
                del requestPayload['hard_delivery_date']
                del requestPayload['set_delivery_date']
            result = myRequest(url,requestPayload)
            if result:
                consoleLog(u'委托合同 %s 已交房' % houseContractInfo[1])

        def confirmPrice():
            """定价"""
            if entrust_type is 'SHARE':
                url = 'isz_house/ApartmentController/searchShareApartment.action'
                apartments_id = sqlbase.serach("SELECT apartment_id from apartment where house_id = '%s' and date(create_time)=date(sysdate()) and rent_type='SHARE'" % houseInfo['houseID'],oneCount=False)
                requestPayload = {'apartment_id':apartments_id[0]}
                result = myRequest(url, requestPayload)
                if result:
                    url = 'isz_house/ApartmentController/confirmPricing.action'
                    requestPayload = []
                    # 根据房间数量，动态将参数添加至定价请求参数中
                    default_rent_price = 24
                    for x in range(rooms):
                        content = result['obj'][x]
                        if 'func_type_desc' in content:
                            del content['func_type_desc']
                        if 'rent_price' in content:
                            del content['rent_price']
                        if x is 0:
                            content['current_apartment'] = 'Y'
                        default_rent_price += 1000
                        content['rent_price'] = str(house_rent_price) if house_rent_price else str(default_rent_price)
                        requestPayload.append(content)
                    result = myRequest(url, requestPayload)
                    if result:
                        # 避免等待时间太长，生成的房源没有出来，此处调用solr的增量操作
                        solr('apartment', get_conf('testCondition', 'test'))
                        consoleLog(u'房源 %s 完成定价' % houseInfo['houseCode'])
                        return apartments_id[0]
            else:
                url = 'isz_house/ApartmentController/confirmApatmentRentPricing.action'
                apartments_id = sqlbase.serach("SELECT apartment_id from apartment where house_id = '%s' and date(create_time)=date(sysdate())" % houseInfo['houseID'])
                requestPayload = {'apartment_id': apartments_id[0],'rent_price':str(house_rent_price) if house_rent_price else '1024'}
                result = myRequest(url,requestPayload)
                if result:
                    # 避免等待时间太长，生成的房源没有出来，此处调用solr的增量操作
                    solr('apartment', get_conf('testCondition', 'test'))
                    consoleLog(u'房源 %s 完成定价' % houseInfo['houseCode'])
                    return apartments_id[0]


        return fitmentHouseAndSolr()

def createCustomer():
    """
    新增租前客户
    :return: 返回租客信息字典，给创建承租合同提供使用
    """
    url = 'isz_customer/CustomerController/saveCustomer.action'
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    phone = random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
    data = {
        'customer_name':'AutoTest' + '-' + time.strftime('%m%d-%H%M%S'),        #姓名
        'phone':phone,                                                                                          #手机
        'customer_status':'EFFECTIVE',                                                                   #状态
        'email':'isz@ishangzu.com',                                                                       #邮箱
        'wechat':'wechat',                                                                                      #微信
        'constellation':'VIRGO',                                                                              #星座
        'education':'BACHELOR',                                                                            #学历
        'belong_did':sqlbase.serach("select dep_id from sys_user where user_phone = '15168368432' and user_status = 'INCUMBENCY'")[0],      #所属部门
        'belong_uid': sqlbase.serach("select user_id from sys_user where user_phone = '15168368432' and user_status = 'INCUMBENCY'")[0],      #所属人
        'customer_from':'FLOOR19',                                                                       #来源
        'rent_class':'CLASSA',                                                                                  #求租等级
        'rent_type':'GATHERHOUSE',                                                                      #求租类型
        'rent_use':'RESIDENCE',                                                                             #求租用途
        'rent_fitment':'FITMENT_SIMPLE',                                                              #装修情况
        'city_code':'330100',                                                                                   #求租城区
        'rent_area_code':'330108',                                                                          #求租地区
        'rent_business_circle_ids':'4',                                                                       #求租商圈
        'office_address':u'海创基地',                                                                       #上班地点
        'address_gd_lng':'120.138631',                                                                   #经度
        'address_gd_lat':'30.186537',                                                                      #纬度
        'rent_rooms':'1',                                                                                         #求租户型
        'rent_livings':'1',
        'rent_bathrooms':'1',
        'rent_from_price':'1000.00',                                                                        #求租价格
        'rent_to_price':'2000.00',
        'rent_date':time.strftime('%Y-%m-%d'),                                                      #希望入住日期
        'rent_people':'2',                                                                                       #入住人数
        'area':'28',                                                                                                 #面积
        'rent_other':'other demand',                                                                       #其他需求
        'gender':'MALE',                                                                                        #性别
        'marriage':'UNMARRIED',                                                                          #婚否
        'submit_channels':'ERP'                                                                             #提交渠道
    }
    if myRequest(url,data):
        customerInfo = sqlbase.serach("select customer_id,customer_name,customer_num from customer where customer_name = '%s'" % data['customer_name'])
        consoleLog(u'租前客户 %s 创建成功' % customerInfo[1])
        return {'customer_id':customerInfo[0],'customer_name':customerInfo[1],'customer_num':customerInfo[2]}

def createApartmentContract(apartement_id,customerInfo,rent_price,sign_date,rent_start_date,rent_end_date,deposit,payment_cycle):
    """
    新增出租合同
    :param apartement_id: 签约的公寓ID，创建委托合同的接口会返回此信息
    :param customerInfo: 签约的租前客户信息，创建租客的接口会返回此信息
    :param rent_price: 目标出租价格（由于半年付和年付会有优惠，此价格直接为优惠后的价格）
    :param sign_date: 签约日期
    :param rent_start_date: 承租起算日
    :param rent_end_date: 承租到期日
    :param deposit: 押金
    :param payment_cycle:付款周期
    :return: 返回创建的合同信息字典
    """
    url = 'isz_contract/ApartmentContractController/saveOrUpdateApartmentContract.action'
    houseInfo = sqlbase.serach("select house_id,room_id,house_contract_id from apartment where apartment_id = '%s'" % apartement_id)
    houseContractInfo = sqlbase.serach("select entrust_type from house_contract where contract_id = '%s'" % houseInfo[2])[0]
    def modifiApartmentRentPrice(apartmentID,rentPrice):
        """修改定价"""
        url = 'isz_house/ApartmentController/confirmApatmentRentPricing.action'
        data = {'apartment_id':apartmentID,'rent_price':str(rentPrice)}
        myRequest(url,data)
    def updateCostAccount(apartmentID,rentPrice):
        """更新成本占比"""
        url = 'isz_house/ApartmentController/updateCostAccount.action'
        data = {'apartment_id':apartmentID,'rent_price':str(rentPrice)}
        myRequest(url,data)
    if houseContractInfo == 'SHARE':
        modifiApartmentRentPrice(apartement_id,rent_price)
        updateCostAccount(apartement_id,rent_price)
    elif houseContractInfo == 'ENTIRE':
        modifiApartmentRentPrice(apartement_id,rent_price)

    if payment_cycle is 'HALF_YEAR':
        real_due_rent_price = rent_price * 0.985
    elif payment_cycle is 'ONE_YEAR':
        real_due_rent_price = rent_price * 0.97
    else:
        real_due_rent_price = rent_price
    data = {
        'contract_num':'AutoTest' + '-' + time.strftime('%m%d-%H%M%S') + get_randomString(),     #合同编号
        'sign_date':sign_date,          #签约日期
        'rent_start_date':rent_start_date,      #承租起算日
        'rent_end_date':rent_end_date,      #承租结束日
        'payment_date':rent_start_date,     #首次付款日
        'deposit':str(deposit),         #押金
        'payment_type':'NORMAL',        #付款方式
        'payment_cycle':payment_cycle,      #付款周期
        'cash_rent':str(rent_price * 0.1),     #转租费
        'agency_fee':'1000',                                                        #中介服务费
        'month_server_fee_discount':'100%',     #服务费折扣
        'remark':'remark',      #备注
        'sign_name':u'签约人',     #签约人
        'sign_id_type':'IDNO',      #签约人证件类型
        'sign_id_no':'42062119910828541X',      #签约人证件号
        'sign_phone':'15168368432',     #签约人手机号
        'sign_is_customer':'Y',     #签约人是否是承租人
        'postal_address':u'通讯地址',   #签约人通讯地址
        'deposit_type': 'ONE',
        'depositIn': '1',
        'apartmentContractRentInfoList':[
            {
                'firstRow':True,
                'money':str(real_due_rent_price),
                'start_date':rent_start_date,
                'end_date':rent_end_date,
                'rowIndex':0,
                'money_cycle':payment_cycle,
                'payment_date':rent_start_date,
                'deposit':deposit,
                'agencyFeeMoney':1000,
                'money_type':'RENT',
                'rent_start_date':rent_start_date,
                'rent_end_date':rent_end_date,
                'sign_date':sign_date
            }
        ],
        'person':{
            "urgent_customer_name": "紧急联系人",
            "urgent_phone": "15168368433",
            "urgent_card_type": "PASSPORT",
            "urgent_id_card": "huzhaohuzhao",
            "urgent_postal_address": "紧急联系人通讯地址",
            "customer_id": customerInfo['customer_id'],#FF8080815F0A26E8015F1427B6040140
            "birth_date": "1991-8-28",
            "constellation": "VIRGO",
            "customer_num": customerInfo['customer_num'],
            "customer_from": "FLOOR19",
            "customer_type": "PERSONALITY",
            "customer_name": "签约人",
            "card_type": "IDNO",
            "id_card": "42062119910828541X",
            "phone": "15168368432",
            "gender": "MALE",
            "education": "BACHELOR",
            "trade": "IT",
            "email": "isz@mail.com",
            "tent_contact_address": "通讯地址",
            "yesNo": "Y",
            "person_type": 3
        },
        'persons':[
            {
                "person_type": 3,
                "gender": "MALE",
                "card_type": "IDNO",
                "customer_name": "签约人",
                "id_card": "42062119910828541X",
                "phone": "15168368432",
                "cardType": "身份证",
                "sex": "男",
                "staydate": time.strftime('%Y-%m-%d')
            }
        ],
        'model':'4'
    }
    def step1():
        url = 'isz_contract/ApartmentContractController/searchApartmentContractDetail.action'
        requestPayload = {"apartment_id":apartement_id,"contract_type":"NEWSIGN"}
        result = myRequest(url,requestPayload)
        if result:
            content = delNull(result['obj']['apartmentContract'])
            for x,y in content.items():
                data[x] = y

    def step2():
        url = 'isz_contract/ApartmentContractController/getHouseContractByHouseId.action'
        requestPayload = {
            "rent_start_date":rent_start_date,
            "rent_end_date":rent_end_date,
            "houseId":houseInfo[0],
            "apartment_id":apartement_id,
            "room_id":houseInfo[1]
        }
        if houseContractInfo == 'ENTIRE':
            del requestPayload['room_id']
        result = myRequest(url,requestPayload)
        if result:
            data['houseContractList'] = delNull(result['obj'])

    def step3():
        url = 'isz_contract/ApartmentContractController/getServiceAgencyProperty.action'
        requestPayload = {
            "houseContractId": data['houseContractList'][0]['contract_id'],
            "firstMoney": str(real_due_rent_price),
            "rent_start_date": rent_start_date,
            "rent_end_date": rent_end_date,
            "contract_type": "NEWSIGN",
            "sign_date": sign_date,
            "house_id": houseInfo[0],
            "room_id": houseInfo[1]
        }
        if houseContractInfo == 'ENTIRE':
            del requestPayload['room_id']
        result = myRequest(url,requestPayload)
        if result:
            data['month_server_fee'] = str(result['obj']['month_server_fee'])

    def step4():
        url = 'isz_contract/ApartmentContractController/createApartmentContractReceivable.action'
        requestPayload = data['apartmentContractRentInfoList']
        result = myRequest(url,requestPayload)
        if result:
            data['receivables'] = delNull(result['obj'])
            index = 0
            for x in data['receivables']:
                x['edit'] = False
                x['rowIndex'] = index
                index += 1
    step1()
    step2()
    step3()
    step4()
    result = myRequest(url,data)
    if result:
        consoleLog(u'承租合同 %s 已创建完成' % data['contract_num'])
        apartmentContractInfo = {'contractID':sqlbase.serach("select contract_id from apartment_contract where contract_num = '%s'" % data['contract_num'])[0],'contractNum':data['contract_num']}
        return apartmentContractInfo

auditTypeInfo = collections.namedtuple('auditType',['houseContract','apartmentContract','houseContractEnd','apartmentContractEnd'])
auditType = auditTypeInfo(houseContract='HOUSECONTRACT',apartmentContract='APARTMENTCONTRACTE',houseContractEnd='HOUSECONTRACTEND',apartmentContractEnd='APARTMENTCONTRACTEND')
auditStatusInfo = collections.namedtuple('auditStatus',['chuShen','fuShen','fanShen','boHui','shenhe'])
auditStatus = auditStatusInfo(chuShen='PASS',fuShen='APPROVED',fanShen='REAUDIT',boHui='REJECTED',shenhe='AUDIT')
def audit(id,type,*actions):
    """
    所有流程的审核操作
    :param type: 要审核的模块，如出租合同、委托合同终止等，传入auditType类的属性
    :param auditStatus: 要做的动作，如做初审、反审等，传入auditStatus类的属性
    :param id: 要审核的数据主键，如出租合同ID，委托合同终止ID
    :return: None
    """
    if type is auditType.houseContract:
        if sqlbase.serach("select audit_status from house_contract_payable where contract_id = '%s' and deleted = 0 limit 1" % id)[0] == 'NOTAUDIT':
            url = 'isz_contract/houseContractController/houseContractPayableAudit.action'
            requestPayload = {
                'payableid':','.join(sqlbase.serach("select payable_id from house_contract_payable where contract_id = '%s' and deleted = 0" % id,oneCount=False)),
                'contractid':id,'status':'AUDITED'
            }
            myRequest(url,requestPayload)
        url = 'isz_contract/houseContractController/houseContractAudit.action'
        data = {'achieveid':id,'content':'test','activityId':''}
        for action in actions:
            if action is auditStatus.chuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % (auditStatus.chuShen,auditType.houseContract))[0]
            elif action is auditStatus.fuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.fuShen, auditType.houseContract))[0]
            elif action is auditStatus.boHui:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.boHui, auditType.houseContract))[0]
            elif action is auditStatus.fanShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.fanShen, auditType.houseContract))[0]
            myRequest(url,data)
            time.sleep(1) if len(actions) >  1 else None
    elif type is auditType.apartmentContract:
        url = 'isz_contract/ApartmentContractController/apartmentContractAudit.action'
        data = {'achieveid': id, 'content': 'test', 'activityId': ''}
        for action in actions:
            if action is auditStatus.chuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % (auditStatus.chuShen, auditType.apartmentContract))[0]
            elif action is auditStatus.fuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.fuShen, auditType.apartmentContract))[0]
            elif action is auditStatus.boHui:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.boHui, auditType.apartmentContract))[0]
            elif action is auditStatus.fanShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.fanShen, auditType.apartmentContract))[0]
            myRequest(url, data)
            time.sleep(1) if len(actions) > 1 else None
    elif type is auditType.houseContractEnd:
        url = 'isz_contract/endAgreementControl/houseContractEndAudit.action'
        data = {'achieveid': id, 'content': 'test', 'activityId': ''}
        for action in actions:
            if action is auditStatus.chuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % (auditStatus.chuShen, auditType.houseContractEnd))[0]
            elif action is auditStatus.fuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % ('REVIEW', auditType.houseContractEnd))[0]
            elif action is auditStatus.boHui:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % ('RE_JECT', auditType.houseContractEnd))[0]
            elif action is auditStatus.fanShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % (auditStatus.fanShen, auditType.houseContractEnd))[0]
            myRequest(url, data)
            time.sleep(1) if len(actions) > 1 else None
    elif type is auditType.apartmentContractEnd:
        url = 'isz_contract/endAgreementControl/apartmentEndAudit.action'
        data = {'achieveid': id, 'content': 'test', 'activityId': ''}
        for action in actions:
            if action is auditStatus.chuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s' and activity_type = '%s'" % (auditStatus.chuShen, auditType.apartmentContractEnd))[0]
            elif action is auditStatus.fuShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % ('REVIEW', auditType.apartmentContractEnd))[0]
            elif action is auditStatus.boHui:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % ('RE_JECT', auditType.apartmentContractEnd))[0]
            elif action is auditStatus.fanShen:
                data['activityId'] = sqlbase.serach("select activity_id from workflow_activity where activity_status = '%s'and activity_type = '%s'" % (auditStatus.fanShen,auditType.apartmentContractEnd))[0]
            myRequest(url, data)
            time.sleep(1) if len(actions) > 1 else None

def receipt(contractType,contractID):
    """
    出租合同实收及应收的审核
    :param contractType: 委托合同或者出租合同
    :param contractID: 对应的合同ID
    :return: None
    """
    if contractType == 'houseContract':
        url = 'isz_finance/HouseContractPayableController/savePay.action'
        info = sqlbase.serach("select payable_amount,payable_id from house_contract_payable where contract_id = '%s' and deleted = 0" % contractID,oneCount=False)
        for i in info:
            data = {
                'payable_amount':i[0],      #应付金额
                'payment_money':i[0],       #实付金额
                'payment_date':datetimes.today(),        #实付日期
                'payment_type':'CASH',      #付款方式
                'remark':'test',        #备注
                'payable_id':i[1],      #应付ID
                'contract_id':contractID
            }
            myRequest(url,data)
        time.sleep(1)
    elif contractType == 'apartmentContract':
        url = 'isz_finance/ApartmentContractReceiptsController/saveOrUpdateNewReceipts.action'
        info = sqlbase.serach("select receivable_money,receivable_id from apartment_contract_receivable where contract_id = '%s' and deleted = 0" % contractID,oneCount=False)
        for i in info:
            data = {
                'alipay_card':'0011',   #支付宝账号
                'company':sqlbase.serach("select sign_body from apartment_contract where contract_id = '%s'" % contractID)[0],     #收款公司
                'contract_id':contractID,
                'operation_total':'1024',    #转账总金额
                'receipts_date':datetimes.today(),      #收款日期
                'receipts_type':'ALIPAY',       #收款方式：支付宝转账
                'receipts_money':i[0],      #收款金额
                'receivable_id':i[1]    #应收ID
            }
            #实收
            result = myRequest(url,data)
            if result:
                #审核
                myRequest(url='isz_finance/ApartmentContractReceiptsController/endReceivable.action',data={'receivable_id':i[1]})
            else:
                break
        time.sleep(1)


if __name__ == '__main__':
    # apartment = addHouseContractAndFitment(apartment_type='MANAGE',entrust_type='SHARE',sign_date='2017-10-01',owner_sign_date='2017-10-01',entrust_start_date='2017-10-01',
    #                                        entrust_end_date='2019-10-10',delay_date='2020-01-10',free_start_date='2017-10-01',free_end_date='2017-10-31',first_pay_date='2017-10-01',second_pay_date='2017-10-31',
    #                                        rent=1234,parking=123,year_service_fee=321,payment_cycle='MONTH',fitment_start_date='2017-10-01',fitment_end_date='2017-10-31',rooms=3,fitmentCost=88888)
    # customer = createCustomer()
    # createApartmentContract(apartement_id=apartment,customerInfo=customer,rent_price=5500,sign_date='2017-10-01',rent_start_date='2017-10-02',rent_end_date='2018-12-12',
    #                         deposit=2000,payment_cycle='MONTH')

    #audit('FF8080815F569109015F5698FF9F00FA',auditType.houseContract,auditStatus.chuShen,auditStatus.fuShen,auditStatus.fanShen,auditStatus.chuShen,auditStatus.boHui)

    #receipt('apartmentContract','FF8080815F613E71015F61C030F3031E')
    get_cookie()
