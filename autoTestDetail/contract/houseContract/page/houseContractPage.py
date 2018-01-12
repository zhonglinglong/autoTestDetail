# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By




houseSearchMould = {
        'residential_name_loc' : (By.ID,'residential_name_house_code_search'),
        'status' : (By.ID,'is_active_search'),
        'search_button_loc' : (By.ID,'search_btn'),
        'tr_house' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),
        'add_house_contract_button' : (By.CSS_SELECTOR,'#edit_btn + button')
    }
contractSearchMould = {
        'residential_name_loc':(By.CSS_SELECTOR,'#residential_name_search + span > input:nth-child(1)'),
        'contract_num_loc': (By.CSS_SELECTOR, '#contract_num_search + span > input:nth-child(1)'),
        'search_button_loc': (By.ID, 'search_btn'),
        'tr_contract': (By.CSS_SELECTOR, 'tr[datagrid-row-index="0"]'),
        'edit_loc': (By.ID, 'edit_btn')
    }
addHouseContractMould = {
        'edit_loc' : (By.CSS_SELECTOR,'#edit_btn + button'), #列表页加载的等待元素
        'delete_button': (By.ID, 'del_btn'),  # 删除
        'newsign_button':(By.CSS_SELECTOR,'.dialog-button.messager-button span>span'),  #开发房源新签委托
        'continue_button':(By.ID,'continue_btn'),  # 续签
        'delete_button_confirm': (By.CSS_SELECTOR, '.dialog-button.messager-button > a:nth-child(1) > span'),  # 删除确认
        #合同信息
        'tab_info_loc' : (By.CSS_SELECTOR ,'.tabs-inner'), #0-合同信息、1-租金明细、2-业主信息、3-资料上传
        'inside_space_loc' : (By.CSS_SELECTOR ,'#first_contract_base > table > tbody > tr:nth-child(3) > td:nth-child(4) > span > input:nth-child(1)'), #使用面积
        'rent_loc' : (By.CSS_SELECTOR, 'input#rent + span > input:nth-child(1)'),   #房租
        'parking_loc' : (By.CSS_SELECTOR, 'input#parking+ span > input:nth-child(1)'),  #车位费
        'service_fee_loc' : (By.CSS_SELECTOR, 'input#year_service_fee + span > input:nth-child(1)'),    #服务费
        'pledge_loc' : (By.ID,'pledge'),     #抵押情况-有
        'oldcontract_loc':(By.CSS_SELECTOR,'#parent_contract_base p>input:nth-child(3)'),  # 原合同不并入新合同
        'contract_num_loc' : (By.CSS_SELECTOR,'input#contract_num + span >input:nth-child(1)'),  #合同编号
        'payment_cycle_loc_1' : (By.CSS_SELECTOR,'input#payment_cycle + span > span > a'), #付款周期
        'payment_cycle_loc_2': (By.CSS_SELECTOR, 'body > div:nth-child(44) > div >div:nth-child(1)'),  # 月付
        'payment_cycle_month_loc':(By.ID,'_easyui_combobox_i17_0'),  # 月付
        'contract_strategy1.1_loc': (By.CSS_SELECTOR, '#contract_strategy_table0 input.erp-table-input'),  # 第一年租金策略
        'contract_strategy1_loc': (By.CSS_SELECTOR, '#contract_strategy_table0 input.textbox-text.validatebox-text'),# 第一年租金策略
        'contract_strategy2.1_loc':(By.CSS_SELECTOR,'#contract_strategy_table1 input.erp-table-input'),  #第二年租金策略
        'contract_strategy2_loc': (By.CSS_SELECTOR, '#contract_strategy_table1 input.textbox-text.validatebox-text'),# 第二年租金策略
        'contract_strategy3.1_loc':(By.CSS_SELECTOR,'#contract_strategy_table2 input.erp-table-input'),# 第三年租金策略
        'contract_strategy3_loc':(By.CSS_SELECTOR,'#contract_strategy_table2 input.textbox-text.validatebox-text'),  #第三年租金策略
        'next_loc_1' : (By.ID,'form_btn'), #合同信息下一步
        'page1_save_button':(By.ID,'form_save'),
        #租金明细
        'rent_detail_selectAll' : (By.CLASS_NAME,'check-all'),  #租金明细全选
        'rent_audit_loc' : (By.ID,'payableAudit'),  #租金审核
        'audit_pass_loc' : (By.CSS_SELECTOR,'[value="AUDITED"]'),   #审核通过
        'rent_audit_confirm' : (By.CSS_SELECTOR,'[onclick="customer_pay.AuditButtonConfirm()"]'),    #租金审核确认
        'next_loc_2': (By.ID, 'form_next_btn'),  # 租金明细下一步
        'add_detail_button':(By.CSS_SELECTOR,'#customer_pay .erp-table-operate>a>span'), # 新增租金明细
        'message_close_loc':(By.CSS_SELECTOR,'.panel.window.messager-window a>span>span'),  #关闭数据被其他用户刷新提示
        'detail_button':(By.CSS_SELECTOR,'.erp-table>tbody>tr:last input[type=\"checkbox\"]'),  #款项记录
        'money_type_loc':'.erp-table>tbody>tr:last input[data-field=\"money_type\"]',  #款项名称
        'rent_start_date_loc':'.erp-table>tbody>tr:last input[data-field=\"rent_start_date\"]',  #开始时间
        'rent_end_date_loc':'.erp-table>tbody>tr:last input[data-field=\"rent_end_date\"]',  #结束时间
        'payable_date_loc':'.erp-table>tbody>tr:last input[data-field=\"payable_date\"]',  #应付时间
        'payable_amount_loc':(By.CSS_SELECTOR,'.erp-table>tbody>tr input[data-field=\"payable_amount\"]+span>input'),  #应付金额
        'rent_save_button':(By.CSS_SELECTOR,'#play_button #form_save'), # 保存

        #业主信息
        'addlandlord_button':(By.CSS_SELECTOR, '.datagrid-toolbar a>span'), # 新增业主
        'landlord_name_loc' : (By.CSS_SELECTOR,'td[field="landlord_name"]>div>table>tbody>tr>td>span>input:nth-child(1)'),  #业主姓名
        'landlord_card_loc': (By.CSS_SELECTOR, 'td[field="id_card"]>div>table>tbody>tr>td>span>input:nth-child(1)'),  #业主证件号码
        'landlord_phone_loc': (By.CSS_SELECTOR, 'td[field="phone"]>div>table>tbody>tr>td>span>input:nth-child(1)'),  # 业主联系电话
        'landlord_address_loc': (By.CSS_SELECTOR, 'td[field="mailing_address"]>div>table>tbody>tr>td>span>input:nth-child(1)'), #业主通讯地址
        'signFlag_loc': (By.CSS_SELECTOR, 'td[field="signFlag"]>div>input'),    #是否签约人
        #签约人信息
        'address_loc':(By.CSS_SELECTOR,'input#address + span > input:nth-child(1)'),    #签约人通讯地址
        'email_loc': (By.CSS_SELECTOR, 'input#email + span > input:nth-child(1)'),  # 签约人电子邮件
        'other_contact_loc': (By.CSS_SELECTOR, 'input#other_contact + span > input:nth-child(1)'),  # 签约人其他联系方式
        #紧急联系人
        'emergency_name_loc': (By.CSS_SELECTOR, 'input#emergency_name + span > input:nth-child(1)'),  # 联系人姓名
        'emergency_phone_loc': (By.CSS_SELECTOR, 'input#emergency_phone + span > input:nth-child(1)'),  # 联系人电话
        'emergency_id_card_loc': (By.CSS_SELECTOR, 'input#emergency_id_card + span > input:nth-child(1)'),  # 证件号
        'emergency_address_loc': (By.CSS_SELECTOR, 'input#emergency_address + span > input:nth-child(1)'),  # 通讯地址
        #收款人信息
        'account_bank_loc': (By.CSS_SELECTOR, 'input#account_bank + span > input:nth-child(1)'),  # 收款支行
        'account_num_loc': (By.CSS_SELECTOR, 'input#account_num + span > input:nth-child(1)'),  # 收款账号
        'close_loc':(By.ID,'close'), #确认无误
        'bank_loc':(By.CSS_SELECTOR,'input#bank span > inputnth-child(1)'), # 收款银行
        'next_loc_3':(By.CSS_SELECTOR,'#owner_button > div > p > button#form_btn'),    #业主信息下一步
        # 资料上传
        'submit_loc' : (By.CSS_SELECTOR, '#imageupload_button > div > p > button'),
        #审核相关
        'zujincofirm_loc':(By.CSS_SELECTOR,'div.panel.window.messager-window a>span>span'), #租金策略不符提示
        'chushen_loc' : (By.CSS_SELECTOR,'button[status="PASS"]'),  #初审，index=1
        'fushen_loc': (By.CSS_SELECTOR, 'button[status="APPROVED"]'),  # 复审，index=1
        'fanshen_loc':(By.ID,'current_audit_general_button'),  # 反审
        'bohui_loc': (By.CSS_SELECTOR, 'button[status="REJECTED"]'),  # 驳回，index=1
        'contract_audit_content' : (By.ID,'iszCommonWorkflowContext'),  #合同审核意见
        'contract_audit_confirm' : (By.ID,'iszCommonWorkflowPageSure'), #合同审核确认
        'recreate_button':(By.ID,'form_recreate'), # 重新生成租金明细
        'message_loc':(By.CSS_SELECTOR,'.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)'),  # 未审核提示
        'rentdif_cofirm_loc':(By.CSS_SELECTOR,'.dialog-button.messager-button span>span')  #租金策略不同提示

    }

typeMould = {
        #合同信息
        'property_type' : '#property_type', #产权类型
        'apartment_type' : '#apartment_type',   #公寓类型
        'reform_way': '#reform_way',    #改造方式
        'entrust_type': '#entrust_type',    #合同类型
        'sign_body': '#sign_body',  #签约公司
        'sign_date':'#sign_date',   #签约日期
        'owner_sign_date': '#owner_sign_date',  #业主交房日
        'fitment_start_date': '#fitment_start_date',    #装修起算日
        'fitment_end_date': '#fitment_end_date',    #装修截止日
        'entrust_start_date': '#entrust_start_date',    #委托起算日
        'entrust_end_date': '#entrust_end_date',    #委托到期日
        'delay_date': '#delay_date',    #延长到期日
        'freeType': '#freeType',    #免租期类别
        'free_start_date': '#free_start_date',  #免租开始日
        'free_end_date':'#free_end_date',    #免租到期日
        'first_pay_date': '#first_pay_date',    #首次付款日
        'second_pay_date': '#second_pay_date',  #第二次付款日
        'payment_cycle': '#payment_cycle',   #付款周期
        #业主信息
        'ownerCardType':'td[field="ownerCardType"] > div > table > tbody > tr > td > input',    #业主证件类型
        #签约人信息
        'gender':'#gender',  #性别
        'card_type':'#card_type',   #签约人证件类型
        #紧急联系人
        'emergency_card_type': '#emergency_card_type',  # 证件类型
        #收款人信息
        'account_name': '#account_name',  # 证件类型
        'pay_object' :'#pay_object'  # 个人/公司

    }