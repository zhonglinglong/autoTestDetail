# -*- coding:utf8 -*-
from common.base import log,consoleLog,Base,set_conf,get_conf
from common import page
from common import sqlbase
import time
from house.apartment   import  apartmentPage
from selenium.common.exceptions import NoSuchElementException

@log
def addHouserent():
    """自营房源 房源定价"""
    try:
        base=Base()
        base.open(page.apartmentPage, apartmentPage.apartmentMould['tr_apartment'])

        #配置文件读取房源信息
        houseCode = get_conf('houseInfo', 'houseCode')
        consoleLog(u'确认测试房源 %s 是否被定价' % houseCode)
        sql = "SELECT * from apartment where apartment_code like '%s%%' and (rent_price = 0 or rent_price is null) and deleted = 0 and is_active = 'Y' and rent_status = 'WAITING_RENT'" % houseCode.encode('utf-8')

        if sqlbase.get_count(sql) > 0:
            base.input_text(apartmentPage.apartmentMould['residential_name'], houseCode)
            for i in range(5):
                base.click(apartmentPage.apartmentMould['search_btn'])
                time.sleep(1)
                try:
                    test = base.driver.find_element(*apartmentPage.apartmentMould['tr_house'])
                    break
                except NoSuchElementException:
                    consoleLog(u'尝试第%s次查找，但未找到apartment-core的solr增量数据' % int(i + 1), level='w')
                    time.sleep(5)
            base.dblclick(apartmentPage.apartmentMould['tr_apartment'], checkLoc=base.apartmentMould['make_price_btn'])
            base.click(apartmentPage.apartmentMould['make_price_btn'])
            base.input_text(apartmentPage.apartmentMould['share_rent_price'], 2222, index=0)
            base.input_text(apartmentPage.apartmentMould['share_rent_price'], 1111, index=1)
            base.click(apartmentPage.apartmentMould['save_btn'])
            base.click(apartmentPage.apartmentMould['form_btn'])
            consoleLog(u'新增自营房源月租金成功')
        else:
            consoleLog(u'测试房源未找到，随机查找一条未被定价的公寓')
            sql = "SELECT aa.apartment_code,aa.apartment_id FROM apartment aa INNER JOIN house_contract hc ON aa.house_contract_id = hc.contract_id WHERE aa.rent_status = 'WAITING_RENT' " \
                  "AND aa.is_active = 'Y' AND aa.city_code = '330100' AND aa.rent_price is null AND hc.deleted = 0 AND hc.contract_status = 'EFFECTIVE' " \
                  "AND hc.entrust_type = 'SHARE' ORDER BY RAND() LIMIT 1"  #查询合租房源
            if sqlbase.get_count(sql) != 0:
                apartmentCode = sqlbase.serach(sql)[0]
                sql = "SELECT fh.rooms from apartment aa INNER JOIN house_contract hc on aa.house_contract_id = hc.contract_id INNER JOIN fitment_house fh on fh.contract_id = hc.contract_id where aa.apartment_code = '%s'" % apartmentCode
                consoleLog(u'确认随机房源的公寓数量')
                apartmentCount = sqlbase.serach(sql)[0]
                base.input_text(apartmentPage.apartmentMould['residential_name'], apartmentCode)
                base.click(apartmentPage.apartmentMould['search_btn'])
                base.staleness_of(apartmentPage.apartmentMould['tr_house'])
                base.dblclick(apartmentPage.apartmentMould['tr_apartment'], checkLoc=base.apartmentMould['make_price_btn'])
                base.click(apartmentPage.apartmentMould['make_price_btn'])
                if apartmentCount > 1:
                    for i in range(apartmentCount):
                        base.input_text(apartmentPage.apartmentMould['share_rent_price'], 2222, index=i)
                base.click(apartmentPage.apartmentMould['save_btn'])
                # base.click(base.apartmentMould['form_btn'])
                consoleLog(u'新增随机自营房源 %s 月租金成功' % apartmentCode, level='w')
                houseContractInfo = "SELECT contract_num,contract_id from house_contract hc INNER JOIN apartment aa on hc.contract_id = aa.house_contract_id " \
                                    "where aa.apartment_code = '%s' and hc.deleted = 0 ORDER BY hc.create_time desc LIMIT 1" % apartmentCode
                # 写入配置文件
                set_conf('houseInfo', apartmentCode=apartmentCode, apatmentID=sqlbase.serach(sql)[1])
                set_conf('houseContractInfo', contractnum=sqlbase.serach(houseContractInfo)[0], contractid=sqlbase.serach(houseContractInfo)[1])
            else:
                consoleLog(u'未找到未被定价的合租房源，略过定价', level='w')
    finally:
        base.driver.quit()

addHouserent()