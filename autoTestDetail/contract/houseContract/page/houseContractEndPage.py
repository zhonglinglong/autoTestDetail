# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By


searchMould = {
        'export_button' : (By.ID,'export_excel_btn'),
        'contract_num_loc' : (By.CSS_SELECTOR,'#contract_num_search + span > input:nth-child(1)'),   #委托合同号
        'contract_search_button_loc' : (By.ID,'search_btn'),    #委托合同列表页的搜索
        'end_contract_num_loc' : (By.CSS_SELECTOR,'#contract_num_wt + span > input:nth-child(1)'),  #委托合同终止列表页的合同号
        'end_search_button_loc': (By.ID, 'end_search_btn'), #委托合同终止列表页的搜索
        'end_reset_btn' : (By.ID,'end_reset_btn'),
        'tr_contract_end' : (By.CSS_SELECTOR, '#ContractReceivable_table_wt > div:nth-child(1) > div:nth-child(2) > div.datagrid-view > div.datagrid-view2 > div.datagrid-body > table > tbody > tr:nth-child(1)'),  # 列表页
    }
addContractEndMould = {
        'detail_button' : (By.CSS_SELECTOR,'[onclick="HouseEnd.detailDialog(0)"]'), #详情 index:0-操作列中、1-右键中
        'delete_button' : (By.CSS_SELECTOR,'[onclick="HouseEnd.detailDialog(0)"] + button'),    #删除
        'delete_button_confirm' : (By.CSS_SELECTOR,'.dialog-button.messager-button > a:nth-child(1) > span'),   #删除确认
        'tab_info' : (By.CLASS_NAME,'tabs-inner'),  #index 0-出租合同终止结算、1-委托合同终止结算
        'tr_contract': (By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),  # 列表页第一行
        'end_button_loc' : (By.CSS_SELECTOR,'[onclick=\'contractIndex.end("0")\']'),    #0为操作列中，1为右键中
        'check_loc' : (By.ID,'end_type'),   #用来确认双击是否成功的元素-结算类型
        'end_num_loc':(By.CSS_SELECTOR,'#end_contract_num+span>input'),#终止协议号
        #结算-收款明细
        'penalty_loc': (By.CSS_SELECTOR, '#penalty + span > input:nth-child(1)'),  # 违约金陪入
        'return_rent_loc': (By.CSS_SELECTOR, '#return_rent + span > input:nth-child(1)'),  # 返还房租
        'no_charge_loc': (By.CSS_SELECTOR, '#no_charge + span > input:nth-child(1)'),  # 未扣款项
        'fitment_charge_loc': (By.CSS_SELECTOR, '#fitment_charge + span > input:nth-child(1)'),  # 装修扣款
        'other_loc': (By.CSS_SELECTOR, '#other + span > input:nth-child(1)'),  # 其他
        'penalty_remark_loc': (By.CSS_SELECTOR, '#penalty_remark + span > input:nth-child(1)'),
        'return_rent_remark_loc': (By.CSS_SELECTOR, '#return_rent_remark + span > input:nth-child(1)'),
        'no_charge_remark_loc': (By.CSS_SELECTOR, '#no_charge_remark + span > input:nth-child(1)'),
        'fitment_charge_remark_loc': (By.CSS_SELECTOR, '#fitment_charge_remark + span > input:nth-child(1)'),
        'other_remark_loc': (By.CSS_SELECTOR, '#other_remark + span > input:nth-child(1)'),
        'financial_money_loc':(By.CSS_SELECTOR,'#financial_provide_money+span>input'),#核算业绩金额
        #结算-代垫费用退款明细
        'tool_bar' : (By.CSS_SELECTOR,'.datagrid-toolbar > table > tbody > tr > td > a > span'), #0-新增、1-删除
        'return_money_loc' : (By.CSS_SELECTOR,'[field="return_money"] > div > table > tbody > tr > td > span > input:nth-child(1)'),    #退款金额
        #打款信息
        'pay_name_loc' : (By.CSS_SELECTOR,'#pay_name + span > input:nth-child(1)'), #姓名
        'pay_bank_loc' : (By.CSS_SELECTOR,'#pay_bank  + span > input:nth-child(1)'),    #开户银行
        'pay_bank_no_loc': (By.CSS_SELECTOR, '#pay_bank_no  + span > input:nth-child(1)'),  # 银行卡号
        'company_no_loc': (By.CSS_SELECTOR, '#company_no  + span > input:nth-child(1)'),  # 还款公司
        'add_end_image_loc':(By.ID,'contractFileUpload'),
        'end_image_loc':(By.CSS_SELECTOR,'.imgItem'),  # 终止协议电子版图片
        'remark_loc' : (By.ID,'remark'), #备注
        'submit_loc' : (By.ID,'form_save_btn'),    #提交
        # 审核相关
        'chushen_loc': (By.CSS_SELECTOR, 'button[status="PASS"]'),  # 初审
        'fushen_loc': (By.CSS_SELECTOR, 'button[status="REVIEW"]'),  # 复审
        'bohui_loc': (By.CSS_SELECTOR, 'button[status="RE_JECT"]'),  # 驳回
        'fanshen_loc':(By.ID,'current_audit_general_button'),  #反审
        'contract_audit_content': (By.ID, 'iszCommonWorkflowContext'),  # 合同审核意见
        'contract_audit_confirm': (By.ID, 'iszCommonWorkflowPageSure'),  # 合同审核确认
        'close_detail_loc':(By.CSS_SELECTOR,'.panel.window>div:nth-child(1)>.panel-tool'),  # 关闭详情
        'save_loc':(By.ID,'form_submit_btn')
    }
typeMould = {
        'end_audit_status' : '#audit_status_search',
        'end_date' : '#end_date',
        'end_type' : '#end_type',   #终止类型
        'pay_object_loc':'#pay_object', # 个人/公司
        'return_type_loc' : '[field="return_type"] > div > table > tbody > tr > td > input',    #退款项目
        'bear_type_loc' : '[field="bear_type"] > div > table > tbody > tr > td > input',    #承担方
        'bear_name' : '[field="bear_name"] > div > table > tbody > tr > td > input',    #承担方姓名
        'money_start_date' : '[field="start_date"] > div > table > tbody > tr > td > input',  #费用开始时间
        'money_end_date' : '[field="end_date"] > div > table > tbody > tr > td > input',  #费用结束时间
        'explain' : '[field="explain"] > div > table > tbody > tr > td > input',  # 情况说明
        'dispute': '[field="dispute"] > div > table > tbody > tr > td > input',  # 是否纠纷
        'receivable_date' : '#receivable_date',  #应收日期
        'pay_type' : '#pay_type'    #打款类型
    }