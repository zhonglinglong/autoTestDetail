# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By


searchMouid={
        'tr_contract':(By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),#列表第一行
        'earnest_code_loc':(By.ID, 'earnest_code_search'),#定金编号
        'apartment_code_loc':(By.ID,'residential_name_object_code_search'),#房源编号
        'search_button_loc':(By.ID, 'search_btn'),#搜索
        'confirm_button_loc':(By.ID, 'confirm_btn'),#确认
        'sign_loc':(By.ID, 'sign_btn'),#签约
        'breach_loc':(By.ID,'breach_btn'),#违约
        'delete_loc':(By.ID,'del_btn'),  # 删除
        'del_confirm_loc':(By.CSS_SELECTOR,'.panel.window.messager-window span>span'),  # 删除确定
}
confirmMould={
        'earnest_money_loc': (By.CSS_SELECTOR, '#earnest_money + span > input'),#确认金额
        'payway': '#payment_way',#支付方式
        'name_loc': (By.CSS_SELECTOR, '#receipt_name+span>input'),#收据名称
        'company': '#company',#公司
        'receipt_date': '#ALIPAY #receipt_date',#收款日期
        'submit_loc': (By.CSS_SELECTOR, 'div#base_button>div>p>button'),#提交
        'breach_reason_loc': (By.ID,'breach_reason'),#违约原因
        'breach_money_loc': (By.CSS_SELECTOR,'.edit_page_table>tbody>tr>td>span>input'),#违约金额
        'breach_detail_loc':(By.CSS_SELECTOR,'.panel-noscroll>div.panel.window')#违约详情
}
# 定金转入违约金模块
depositToBreachMould = {
        # 查询模块
        'tr_earnest':(By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),#列表第一行
        'search_button': (By.ID,'search_btn'),  # 搜索
        'address_search_loc': (By.ID,'residential_name_house_code_search'),  # 楼盘名称
        'earnest_code_search_loc': (By.ID,'earnest_code_search'),  # 定金编号
        'audit_button': (By.ID,'detail_btn'),  # 审核
        'reset_loc':(By.ID,'del_btn'),  # 重置
        'confirm_loc':(By.CSS_SELECTOR,'.panel.window.messager-window span>span'),  # 确定
        # 定金转入违约金审核
        'earnest_money_loc': (By.CSS_SELECTOR,'#earnest_money + span > input'),  # 收款金额
        'payment_way_loc': (By.ID,'ALIPAY'),  # 收款方式：支付宝
        #支付宝收款方式下的模块标签
        'receipt_date_loc': '#ALIPAY_DIV #receipt_date',  # 收款日期
        'company_loc': '#ALIPAY_DIV #company',  # 收款公司：ISZTECH
        'alipay_card_loc': (By.CSS_SELECTOR,'#alipay_card + span > input'),  # 支付宝账号
        'operation_total_loc': (By.CSS_SELECTOR,'#ALIPAY_DIV #operation_total + span > input'),  # 收款金额
        'shenhe_loc':(By.ID,'audit_btn'),  # 审核
        'remark_loc':(By.CSS_SELECTOR,'#ALIPAY_DIV #remark'),  # 备注
}
