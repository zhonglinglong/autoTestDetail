# -*- coding:utf8 -*-

import  pymysql
from common.base import consoleLog,get_conf
import time


"""
按照业务逻辑顺序以及主外键约束，清理数据需按照以下顺序执行，否则会造成主表数据删除，其他关联表数据删不掉或者部分表删除报错。前面为模块名称，后面为产生数据的表名
step1：user（sys_user_role、sys_user）
step2：residential（residential_buiding_no、residential_buiding_floor、residential_buiding_unit、residential_buiding、residential）
setp3：house（house_audit_status_change、house_configuration、house_develop_relation、follow_house、house_rent、house、house_develop_configuration、house_develop）
step4：house_contract（house_contract_payable、house_contract_rental_detail、house_contract_rent_detail，house_contract_rent_info，house_contract_sign，house_contract_res，house_contract_landlord，house_contract_attachment，house_contract）
step5：fitment（house_room_configuration、house_room_feature、house_room_func、house_room_tag、house_room、apartment、fitment_room、fitment_house）
setp6：apartment_contract（）
"""

conn = pymysql.connect(host=get_conf('db','host'), user=get_conf('db','user'), password=get_conf('db','password'), db=get_conf('db','db'), charset=get_conf('db','charset'), port=get_conf('db','port',int))
cursor = conn.cursor()

"""
sql = {
    #系统用户
    'user_01' : (
        "delete from sys_user_role where user_id in (select user_id from sys_user where user_name = 'AutoTest')",
        "delete from sys_user where user_name = 'AutoTest'"
    ),
    #楼盘字典栋座
    'residential_02' : (
        "DELETE from residential where residential_name = 'AutoTest'",
        "DELETE from residential_building where building_name = 'AutoTest'",
        "DELETE from residential_building_unit where unit_name = 'AutoTest'",
        "DELETE from residential_building_floor where floor_name = 'AutoTest'",
        "DELETE from residential_building_house_no where house_no = 'AutoTest'"
    ),
    #新增房源，审核房源，开发自营房源的数据
    'house_03' : (
        "DELETE from house_audit_status_change where house_id in (SELECT house_id from house where residential_id in (SELECT residential_id from residential where residential_name = 'AutoTest'))",
        "DELETE from house_configuration where house_id  in (SELECT house_id from house where residential_id in (SELECT residential_id from residential where residential_name = 'AutoTest'))",
        "DELETE from house_develop_relation where house_id  in (SELECT house_id from house where residential_id in (SELECT residential_id from residential where residential_name = 'AutoTest'))",
        "DELETE from follow_house where object_id in (SELECT house_id from house where residential_id in (SELECT residential_id from residential where residential_name = 'AutoTest'))",
        "DELETE from house_rent where residential_id in (SELECT residential_id from residential where residential_name = 'AutoTest')",
        "DELETE from house where residential_id in (SELECT residential_id from residential where residential_name = 'AutoTest')",
        "DELETE from house_develop_configuration where house_develop_id in (SELECT house_develop_id from house_develop where residential_name = 'AutoTest')",
        "DELETE from house_develop where residential_name = 'AutoTest（auto）'"
    ),
    #委托合同
    'house_contract_04' : (
        "DELETE from house_contract_payable where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_rental_detail where contract_id in(SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_rent_detail where rent_info_id in (SELECT rent_info_id from house_contract_rent_info where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest'))",
        "DELETE from house_contract_rent_info where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_sign where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_res where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_landlord where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_attachment where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from workflow_process where object_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from house_contract_loss_achievement_detail where loss_achieve_id in (select loss_achieve_id from house_contract_loss_achievement where house_contract_num = 'AutoTest')",
        "DELETE from house_contract_loss_achievement where  house_contract_num = 'AutoTest'",
        "DELETE from house_contract where contract_num = 'AutoTest'",
        "DELETE from query_house_contract where contract_num = 'AutoTest'"
    ),
    #设计工程
    'fitment_05' : (
        "DELETE from house_room_configuration where room_id in (SELECT room_id from house_room where house_id in (SELECT house_id from house_contract where contract_num = 'AutoTest'))",
        "DELETE from house_room_feature where room_id in (SELECT room_id from house_room where house_id in (SELECT house_id from house_contract where contract_num = 'AutoTest'))",
        "DELETE from house_room_func where room_id in (SELECT room_id from house_room where house_id in (SELECT house_id from house_contract where contract_num = 'AutoTest'))",
        "DELETE from house_room_tag where room_id in (SELECT room_id from house_room where house_id in (SELECT house_id from house_contract where contract_num = 'AutoTest'))",
        "DELETE from house_room where house_id in (SELECT house_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from apartment where house_id in (SELECT house_id from house_contract where contract_num = 'AutoTest')",
        "DELETE from fitment_room where fitment_id in (SELECT fitment_id from fitment_house where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest'))",
        "DELETE from fitment_house where contract_id in (SELECT contract_id from house_contract where contract_num = 'AutoTest')"
    ),
    #租前客户
    'customer_person_06':(
        "DELETE from follow_customer where object_id in (SELECT customer_id from customer where customer_name = 'AutoTest')",
        "DELETE from customer_view where customer_id in (SELECT customer_id from customer where customer_name = 'AutoTest')",
        "DELETE from customer_tel where customer_id in (SELECT customer_id from customer where customer_name = 'AutoTest')",
        "DELETE from customer_distribution_record where customer_id in (SELECT customer_id from customer where customer_name = 'AutoTest')",
        "DELETE from customer_business_circle where customer_id in (SELECT customer_id from customer where customer_name = 'AutoTest')",
        "DELETE from customer where customer_name = 'AutoTest'"
    ),
    #出租合同、成交客户，业绩
    'apartment_contract_07':(
        "DELETE from customer_person where person_id in (SELECT person_id from customer_person_relation where customer_id in (SELECT customer_id from customer where customer_name = 'AutoTest'))",
        "DELETE from customer_person_relation where customer_id in (SELECT customer_id from customer where customer_name = 'AutoTest')",
        "DELETE from apartment_contract_achievement_detail where achievement_id in (SELECT achievement_id from apartment_contract_achievement where contract_num = 'AutoTest')",
        "DELETE from apartment_contract_achievement where contract_num = 'AutoTest'",
        "DELETE from apartment_contract_attachment where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE from apartment_contract_check_in where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE from apartment_contract_relation where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE from apartment_contract_receivable where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE from apartment_contract_rent_info where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE FROM apartment_contract_rent_detail WHERE rent_info_id IN ( SELECT rent_info_id FROM apartment_contract_rent_info WHERE contract_id IN ( SELECT contract_id FROM apartment_contract WHERE contract_num = 'AutoTest' ))",
        "DELETE from apartment_contract_rental_detail where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE from contract_achievement_detail where achieve_id in (select achieve_id from contract_achievement where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest'))",
        "DELETE from contract_achievement where contract_id in (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')",
        "DELETE from apartment_contract where contract_num = 'AutoTest'",
        "DELETE from query_apartment_contract where contract_num = 'AutoTest'"
    ),
    #出租合同终止结算
    'apartment_contract_end_08':(
        "DELETE from back_original_achievement_detail where achieve_id in (SELECT achieve_id from back_achievement where end_id = (SELECT end_id from apartment_contract_end where contract_id = (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')))",
        "DELETE from back_house_contract_achievement_detail where achieve_id in (SELECT achieve_id from back_achievement where contract_num = 'AutoTest')",
        "DELETE from back_achievement_detail where achieve_id in (SELECT achieve_id from back_achievement where contract_num = 'AutoTest')",
        "DELETE from back_achievement where contract_num = 'AutoTest'",
        "DELETE from breach_original_achievement_detail where achieve_id in (SELECT achieve_id from breach_achievement where contract_num = 'AutoTest')",
        "DELETE from breach_achievement_detail where achieve_id in (SELECT achieve_id from breach_achievement where contract_num = 'AutoTest')",
        "DELETE from breach_achievement where contract_num = 'AutoTest'",
        "DELETE from apartment_contract_end where contract_id IN (SELECT contract_id from apartment_contract where contract_num = 'AutoTest')"
    ),
    #委托合同终止结算
    'house_contract_end_09':(
        "DELETE from house_contract_loss_achievement_detail where loss_achieve_id in (SELECT loss_achieve_id from house_contract_loss_achievement where house_contract_num = 'AutoTest')",
        "DELETE from house_contract_loss_achievement where house_contract_num = 'AutoTest'",
        "DELETE from house_contract_end where contract_id = (SELECT contract_id from house_contract where contract_num = 'AutoTest')",
    )
}

@log
def clear_data(success):
    try:
        if success == 1:
            for values in ['user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    execute(value)
                    conn.commit()
            consoleLog('用户模块测试数据清理完毕')
        elif success == 2:
            for values in ['residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('楼盘、用户模块测试数据清理完毕')
        elif success == 3:
            for values in ['house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('房源、楼盘、用户模块测试数据清理完毕')
        elif success == 4:
            for values in ['house_contract_04','house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('委托合同、房源、楼盘、用户模块测试数据清理完毕')
        elif success == 5:
            for values in ['fitment_05','house_contract_04','house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('设计工程、委托合同、房源、楼盘、用户模块测试数据清理完毕')
        elif success == 6:
            for values in ['customer_person_06','fitment_05','house_contract_04','house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('租前客户、设计工程、委托合同、房源、楼盘、用户模块测试数据清理完毕')
        elif success == 7:
            for values in ['apartment_contract_07','customer_person_06','fitment_05','house_contract_04','house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('出租合同、租前客户、设计工程、委托合同、房源、楼盘、用户模块测试数据清理完毕')
        elif success == 8:
            for values in ['apartment_contract_end_08','apartment_contract_07','customer_person_06','fitment_05','house_contract_04','house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('出租合同终止、出租合同、租前客户、设计工程、委托合同、房源、楼盘、用户模块测试数据清理完毕')
        elif success == 9:
            for values in ['house_contract_end_09','apartment_contract_end_08','apartment_contract_07','customer_person_06','fitment_05','house_contract_04','house_03','residential_02','user_01']:
                for value in sql.get(values):
                    consoleLog(value)
                    cursor.execute(value)
                    conn.commit()
            consoleLog('委托合同终止、出租合同终止、出租合同、租前客户、设计工程、委托合同、房源、楼盘、用户模块测试数据清理完毕')
    except:
        consoleLog('清理测试数据出现异常，请手动清理以下模块产生的数据： %s 、 当前执行SQL： %s 、%s',level='e') % (values,value,Exception.message)
    finally:
        pass
"""

def serach(sql,needConvert = True,oneCount = True):
    """
    返回查询结果
    :param sql: 查询sql
    :param needConvert: 转换为Unicode、int以及datetime之类的时间数据
    :param oneCount: 返回结果是单条还是多条
    :return:list格式的查询结果
    """
    cursor.execute(sql)
    conn.commit()
    def convert(data):
        if type(data[0]) is tuple:
            if len(data[0]) == 1:
                return [i for i in data]
        elif data is None:
            consoleLog(u'查询无结果')
            return data
        for x, y in enumerate(data):
            if type(data[x]) is tuple or type(data[x]) is list:
                data[x] = list(y)
                convert(data[x])
        return data
    try:
        value = convert(list(cursor.fetchone()) if oneCount else list(cursor.fetchall()))
    except TypeError,e:
        consoleLog(e.message + '\n' + u'当前执行sql：%s' % sql.decode('utf-8'),level='e')
    else:
        if needConvert:
            if value is None:
                consoleLog(u'查询无结果')
                return value
            else:
                for x in range(len(value)):
                    if type(value[x]) is not list:
                        if type(value[x]) is not unicode and type(value[x]) is not int:
                            value[x] = str(value[x])
                    else:
                        for y in range(len(value[x])):
                            if type(value[x][y]) is not unicode and type(value[x][y]) is not int:
                                value[x][y] = str(value[x][y])
                return value
        else:
            return value

def waitData(sql,wantReturnCount,index = 1):
    """
    等待部分异步的数据的同步，如签完合同后的业绩的创建、宽表数据的创建等，默认与预期数量不一致的情况下，查询十次，每次等待10S，一旦一致，跳出
    :param sql: 待查询的sql
    :param wantReturnCount: 希望返回的数量
    :param index: 默认第几次查询，为了递归调用传参，使用时无需关心
    :return:和逾期数量对比，一致为True，不同为Flase
    """
    while index <= 20:
        count = get_count(sql)
        if count == 0 or count != wantReturnCount:
            time.sleep(5)
            index += 1
            if waitData(sql,wantReturnCount,index):
                return True
            return False
        else:
            return True


def get_count(sql):
    """返回查询数量"""
    count = cursor.execute(sql)
    return count

if __name__ == '__main__':
    test = serach("SELECT * from sys_user where user_name = '吴俊'", oneCount=False)
    print test
