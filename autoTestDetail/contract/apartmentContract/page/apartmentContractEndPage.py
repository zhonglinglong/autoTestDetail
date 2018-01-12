# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By



searchMould = {
        'contract_num_loc' : (By.CSS_SELECTOR,'#contract_num_search + span > input:nth-child(1)'),   #承租合同号
        'search_button_loc' : (By.ID,'search_btn'),
        'tr_contract_end' : (By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),  # 列表页第一行
    }
addContractEndMould = {
        'contract_num_loc': (By.CSS_SELECTOR, '#apartment_contract_num + span > input:nth-child(1)'),  # 承租合同号
        '':(By.CSS_SELECTOR),
        'search_button_loc': (By.ID, 'apartment_search_btn'),  # 搜索
        'tr_contract': (By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),  # 列表页第一行
        'end_button_loc' : (By.CSS_SELECTOR,'[onclick=\'apartmentContractList.end("0")\']'),    #0为操作列中，1为右键中
        'delete_button': (By.CSS_SELECTOR, '[onclick="ApartmentEnd.detailDialog(0)"] + button'),  # 删除
        'delete_button_confirm': (By.CSS_SELECTOR, '.dialog-button.messager-button > a:nth-child(1) > span'),  # 删除确认
        'before_end_loc' : (By.CSS_SELECTOR,'[onclick="apartmentContractList.isEndTpye(\'PREEND\')"]'),    #预约终止
        'before_end_continue_loc':(By.CSS_SELECTOR,'#owner_button .btn.blue.btn-sm'), #我已知晓
        'apartment_num_loc': (By.CSS_SELECTOR, '#apartment_code + span > input:nth-child(1)'),  # 承租合同号
        'submit_button_loc':(By.CSS_SELECTOR,'#base_button>div>p>button'),  # 提交
        'now_end_loc': (By.CSS_SELECTOR, '[onclick="apartmentContractList.isEndTpye(\'NORMAL\')"]'),  # 立刻终止
        'end_reason_loc' : (By.CSS_SELECTOR,'#end_reason + span > input:nth-child(1)'), #终止原因
        'end_num_loc':(By.CSS_SELECTOR,'#end_contract_num + span> input:nth-child(1)'),#终止合同号
        'receipt_num_loc' : (By.CSS_SELECTOR,'#receipt_bank_no + span > input:nth-child(1)'),   #收款卡号
        'bank_loc' : (By.CSS_SELECTOR,'#receipt_bank_location + span > input:nth-child(1)'),    #开户银行
        'cardconfirm_close_loc':(By.ID,'close'), #银行卡确认无误
        'project_type_loc':(By.CSS_SELECTOR,'[field="project_type"] + td'), # 款项类型
        'weiyuejin_loc' : (By.CSS_SELECTOR,'[field="project_type"] + td'),   #违约金 index=12
        'zhuanzufei_loc' : (By.CSS_SELECTOR,'[field="project_type"] + td'),   #转租费 index=19
        'payable_deposit_loc': (By.CSS_SELECTOR,'[datagrid-row-index="0"] > [field="payable_money"] > div > table > tbody > tr > td > span > input:nth-child(1)'),    #押金应付
        'receivable_money_loc' : (By.CSS_SELECTOR,'[datagrid-row-index="11"] > [field="receivable_money"] > div > table > tbody > tr > td > span > input:nth-child(1)'),    #违约金应收
        'payable_money_loc': (By.CSS_SELECTOR,'[datagrid-row-index="11"] > [field="payable_money"] > div > table > tbody > tr > td > span > input:nth-child(1)'),    #违约金应付
        'zhuanzu_money_loc' : (By.CSS_SELECTOR,'[datagrid-row-index="20"] > [field="receivable_money"] > div > table > tbody > tr > td > span > input:nth-child(1)'),    #转租费应收
        'add_end_image_loc': (By.ID, 'contractFileUpload'),
        'end_image_loc': (By.CSS_SELECTOR, '.imgItem'),  # 终止协议电子版图片
        'remark_loc' : (By.ID,'remark'), #备注
        'submit_loc' : (By.ID,'form_submit_btn'),    #新增终止的提交
        # 审核相关
        'chushen_loc': (By.CSS_SELECTOR, 'button[status="PASS"]'),  # 初审
        'fushen_loc': (By.CSS_SELECTOR, 'button[status="REVIEW"]'),  # 复审
        'bohui_loc': (By.CSS_SELECTOR, 'button[status="RE_JECT"]'),  # 驳回
        'fanshen_loc': (By.CSS_SELECTOR, 'button[status="REAUDIT"]'),  # 反审
        'save_button':(By.ID,'form_submit_btn'), # 保存
        'submit_button':(By.ID,'form_submit_btn'),
        'contract_audit_content': (By.ID, 'iszCommonWorkflowContext'),  # 合同审核意见
        'contract_audit_confirm': (By.ID, 'iszCommonWorkflowPageSure'),  # 合同审核确认
    }
typeMould = {
        'end_date' : '#end_date',
        'end_type' : '#end_type',   #终止类型
        'receipt_type_loc' : '#contractEndPayerAgintType',   #收款人类型
        'receipt_name_loc' : '#receipt_name',    #收款人姓名
        'pay_type_loc':'#pay_object',#个人/公司
    }

