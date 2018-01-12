# -*- coding:utf8 -*-
from selenium.webdriver.common.by import By



customerSignMould = {
        #签约从租客端发起，选择租客
        'search_customer_name_loc' : (By.ID,'customer_code_name_mobile_search'),    #租客姓名查询
        'search_button_loc' : (By.ID,'search_btn'), #查询按钮
        'tr_customer' : (By.CSS_SELECTOR,'[datagrid-row-index="0"]'),
        'sign_button' : (By.CSS_SELECTOR,'[onclick="CustomerIndex.signAvailability(0)"]'),  #index:0-操作列中、1-右键中
        #选择房源
        'share': (By.CSS_SELECTOR,'#search_panel_customer_book_availability_source > div > div > div > ul > li:nth-child(2) > a > span'),#合租按钮
        'entire': (By.CSS_SELECTOR,'#search_panel_customer_book_availability_source > div > div > div > ul > li > a > span'),#整租按钮
        'house_search_btn' : (By.CSS_SELECTOR,'[onclick="CustomerBookSignSource.searchSource()"]'), #选择房源的查询按钮
        'search_apartment_loc' : (By.ID,'residential_name_house_code_search'),  #楼盘名称查询
        'search_apartment_button_loc' : (By.ID,'search_btn'),   #查询按钮 【2】
        'apartment_loc' : (By.CSS_SELECTOR,'.tabs-panels>div:nth-child(2) [datagrid-row-index="0"]'),   #合租第一条房源
        'entire_apartment_loc': (By.CSS_SELECTOR,'.tabs-panels>div:nth-child(1) [datagrid-row-index="0"]'),   #整租第一条房源
        'newsign_button_loc':(By.CSS_SELECTOR,'.panel.window.messager-window a>span'),
        'add_image_loc': (By.ID, 'imgFileUpload'),
        'image_loc': (By.CSS_SELECTOR, '.imgItem'),  # 下定协议
    }
searchContractMould = {
        'contract_num_loc' : (By.CSS_SELECTOR,'#apartment_contract_num + span > input:nth-child(1)'),   #承租合同号：为0时-合租页面中，为1时，整租页面中
        'search_button_loc' : (By.ID,'apartment_search_btn'),   #搜索
        'tr_contract' : (By.CSS_SELECTOR,'tr[datagrid-row-index="0"]'),  #列表页第一行
        'resign_loc':(By.CSS_SELECTOR,'tr[datagrid-row-index="0"] #edit_btn:nth-child(5)'), # 续签：为0时-合租页面中，为1时，整租页面中
        'delete_loc':(By.CSS_SELECTOR,'.datagridRightMenu.menu-top.menu #data_perm_btn'),#删除
        'message_loc':(By.CSS_SELECTOR,'.panel.window.messager-window>div:nth-child(2)>div:nth-child(2)'),#信息提示
        'message_close_loc':(By.CSS_SELECTOR,'.panel.window.messager-window>div>a>span>span'),#关闭提示
        'entire_loc':(By.CSS_SELECTOR,'div.tabs-header.tabs-header-noborder>div.tabs-wrap>ul>li:nth-child(2)>a>span'),#整租模块
        'entire_contract_num_loc':(By.CSS_SELECTOR,'body.panel-noscroll>div>div>div:nth-child(2) #apartment_contract_num + span > input:nth-child(1)'),#整租承租合同号
        'entire_tr_contract':(By.CSS_SELECTOR,'body.panel-noscroll>div>div>div:nth-child(2) tr[datagrid-row-index="0"]'),#整租列表第一行
        'entire_search_button_loc' : (By.ID,'apartment_entire_search_btn'),   #整租搜索
        'entire_tab_button' : (By.CLASS_NAME,'tabs-last')       #整租tab按钮
    }
addApartmentContractMould = {
        'delete_button_confirm': (By.CSS_SELECTOR, '.dialog-button.messager-button > a:nth-child(1) > span'),  # 删除确认
        'deposit_manage':(By.NAME,'dispostIn'), #原合同押金处理方案
        #合同信息
        'tab_info_loc': (By.CSS_SELECTOR, '.tabs-inner'),  # 0-合租、1-整租、2-合同信息、3-应收款项、4-租客详情
        'contract_num_loc' : (By.CSS_SELECTOR,'#contract_num + span > input:nth-child(1)'),  #合同编号
        'deposit_loc' : (By.CSS_SELECTOR,'#deposit + span > input:nth-child(1)'),    #应收押金
        #合同租金
        'rent_strategy_menu_loc': (By.CSS_SELECTOR, '#contract_strategy_table > div > a > span > span:nth-child(1)'),    #租金策略：[0]为新增，[1]为删除
        'rent_strategy1_end_loc':'#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input',#第一条租金策略结束日期
        'rent_strategy2_money_loc':(By.CSS_SELECTOR,'#contract_strategy_table > table > tbody > tr:nth-child(2)>td:nth-child(6) > span>input'), #第二条租金策略月租金
        'rent_strategy2_end_loc':'#contract_strategy_table > table > tbody > tr:nth-child(2) > td:nth-child(8) > input',#第二条租金策略结束日期
        'rent_strategy_price_loc': (By.CSS_SELECTOR, '#contract_strategy_table > table > tbody > tr > td:nth-child(6) > input'),    #月租金
        'rent_strategy_contain_loc': (By.CSS_SELECTOR, '#contract_strategy_table > table > tbody > tr > td:nth-child(9) > div > button'),   #月租金包含按钮
        'contain_fee_loc': (By.CSS_SELECTOR, '#money_add + span > input:nth-child(1)'),     #月租金包含费用金额
        'contain_fee_save_loc': (By.CSS_SELECTOR, '#apartmentContract_money_panel_add > div > p > button'),     #月租金包含的保存
        'agent_fee_loc': (By.CSS_SELECTOR, '#agency_fee + span > input:nth-child(1)'),  # 中介服务费
        'remark_loc': (By.ID, 'remark'),    #备注
        'save_button': (By.ID,'form_save'),
        'next_loc_1': (By.CSS_SELECTOR, '#base_button > div > p > button#form_btn'),   #第一页的下一步
        'next_loc_2': (By.CSS_SELECTOR, '#base_button > div > p > button#form_next_btn'),   #第二页的下一步
        #租客详情
        'sign_name_loc' : (By.CSS_SELECTOR,'#sign_name + span > input:nth-child(1)'),  #签约人姓名
        'sign_id_no_loc' : (By.CSS_SELECTOR,'#sign_id_no + span > input:nth-child(1)'),    #签约人证件号
        'sign_phone_loc' : (By.CSS_SELECTOR,'#sign_phone + span > input:nth-child(1)'),   #签约人联系电话
        'sign_address_loc': (By.CSS_SELECTOR,'#postal_address + span > input:nth-child(1)'),  #签约人通讯地址
        #紧急联系人
        'urgent_customer_name_loc': (By.CSS_SELECTOR,'#urgent_customer_name + span > input:nth-child(1)'),    #紧急联系人姓名
        'urgent_phone_loc': (By.CSS_SELECTOR,'#urgent_phone + span > input:nth-child(1)'),    #紧急联系人电话
        'urgent_id_card_loc': (By.CSS_SELECTOR,'#urgent_id_card + span > input:nth-child(1)'),    #紧急联系人证件号
        'urgent_postal_address_loc': (By.CSS_SELECTOR,'#urgent_postal_address + span > input:nth-child(1)'),  #紧急联系人地址
        #承租人信息
        'trade_loc': (By.CSS_SELECTOR,'#trade + span > input:nth-child(1)'),  #行业
        'email_loc': (By.CSS_SELECTOR,'#email + span > input:nth-child(1)'),  #电子邮件
        'tent_contact_address_loc': (By.CSS_SELECTOR,'#tent_contact_address + span > input:nth-child(1)'),    #联系地址
        #入住人信息
        'del_person_loc' : (By.CSS_SELECTOR,'#check_person_info > div > div > div:nth-child(1) > table > tbody > tr > td:nth-child(3) > a > span'),    #删除入住人按钮
        'add_person_loc': (By.CSS_SELECTOR,'#check_person_info > div > div > div:nth-child(1) > table > tbody > tr > td:nth-child(1) > a > span > span:nth-child(1)'),  # 新增入住人按钮
        'person_count_loc' : (By.CSS_SELECTOR,'#check_person_info > div > div > div.datagrid-view > div:nth-child(2) > div:nth-child(2) > table > tbody > tr '),   #入住人个数
        'person_name_loc' : (By.CSS_SELECTOR,'td[field="customer_name"] > div > table > tbody > tr > td > span > input:nth-child(1)'),        #入住人姓名
        'person_cardType_loc': (By.CSS_SELECTOR,'td[field="id_card"] > div > table > tbody > tr > td > span > input:nth-child(1)'),       # 入住人证件号码
        'person_phone_loc' : (By.CSS_SELECTOR,'td[field="phone"] > div > table > tbody > tr > td > span > input:nth-child(1)'),    #入住人联系电话
        # 审核相关
        'chushen_loc': (By.CSS_SELECTOR, 'button[status="PASS"]'),  # 初审
        'fushen_loc': (By.CSS_SELECTOR, 'button[status="APPROVED"]'),  # 复审，index=1
        'fanshen_loc':(By.ID,'current_audit_general_button'), #反审
        'bohui_loc': (By.CSS_SELECTOR, 'button[status="REJECTED"]'),  # 驳回
        'contract_audit_content': (By.ID, 'iszCommonWorkflowContext'),  # 合同审核意见
        'contract_audit_confirm': (By.ID, 'iszCommonWorkflowPageSure'),  # 合同审核确认
        'submit_loc' : (By.CSS_SELECTOR,'#owner_button > div > p > button#form_submit')   #合同提交
    }

typeMould = {
        #合同信息
        'sign_date' : '#sign_date',  #签约日期
        'rent_start_date' : '#rent_start_date',     #承租起算日
        'rent_end_date' : '#rent_end_date',     #承租到期日
        'rent_end_date2':'#first_contract_info #rent_end_date', # 重新打开的承租到期日
        'payment_date' : '#payment_date',   #首次付款日
        'payment_type': '#payment_type',    #付款方式
        'payment_cycle' : '#payment_cycle',     #付款周期
        #合同租金
        'rent_strategy_start_loc': '#contract_strategy_table > table > tbody > tr > td:nth-child(7) > input',   #租金策略开始日
        'rent_strategy_end_loc': '#contract_strategy_table > table > tbody > tr > td:nth-child(8) > input',     #租金策略结束日
        'contain_fee_type': '#fee_type',    #月租金包含费用类型
        #其他费用
        'agency_fee': '#agency_fee',        #中介服务费
        #签约人
        'sign_id_type': '#sign_id_type',        #签约人证件类型
        'sign_is_customer': '#sign_is_customer',    #是否承租人
        #紧急联系人
        'urgent_card_type': '#urgent_card_type',    #紧急联系人证件类型
        #承租人信息
        'customer_type': '#customer_type',  #租客类型
        'gender': '#gender',    #租客性别
        'education': '#education',  #学历
        'yesNo': '#yesNo',  #是否入住
        #入住人信息
        'cardType': 'td[field="cardType"] > div > table > tbody > tr > td > input',   #入住人证件类型
        'sex': 'td[field="sex"] > div > table > tbody > tr > td > input',   #入住人性别
        'staydate': 'td[field="staydate"] > div > table > tbody > tr > td > input'    #入住日期
    }

alertInfo = (By.CSS_SELECTOR,'.messager-icon.messager-info')       #info级别的弹窗提示
saveBtn = (By.CSS_SELECTOR,'.search-button-wrapper #form_save')         #详情页中的保存，为数组，位置分别对应详情页的tab页
editTab = (By.CSS_SELECTOR,'.tabs-inner span:nth-child(1)')             #详情页中的tab，为数组，前两个为整租、合租，后三个为详情中的tab