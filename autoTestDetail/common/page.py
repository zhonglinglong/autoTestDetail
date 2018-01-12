# -*- coding:utf8 -*-

#系统管理
userPage = 'http://isz.ishangzu.com/isz_base/jsp/user/userManage.jsp'     #用户管理
resPage = 'http://isz.ishangzu.com/isz_base/jsp/user/resManage.jsp'     #资源管理
rolePage = 'http://isz.ishangzu.com/isz_base/jsp/user/roleManage.jsp'   #角色管理
depPage = 'http://isz.ishangzu.com/isz_base/jsp/user/departManage.jsp'      #部门管理
accreditPage = 'http://isz.ishangzu.com/isz_base/jsp/user/loginAuth.jsp'        #授权管理
positonPage = 'http://isz.ishangzu.com/isz_base/jsp/user/positionList.jsp'      #岗位管理
#客户管理
customerListPage = 'http://isz.ishangzu.com/isz_customer/jsp/customer/customerList.jsp'    #租前客户
customerFollowPage = 'http://isz.ishangzu.com/isz_customer/jsp/customer/customerFollowList.jsp'     #租客跟进
customerViewPage = 'http://isz.ishangzu.com/isz_customer/jsp/customer/customerViewList.jsp'     #租客带看
#楼盘管理
areaPage = 'http://isz.ishangzu.com/isz_house/jsp/districtbusinesscircle/districtBusinessCircle.jsp'    #区域商圈
residentiaPage = 'http://isz.ishangzu.com/isz_house/jsp/residential/residentialList.jsp'    #楼盘字典
auditResidentiaPage = 'http://isz.ishangzu.com/isz_house/jsp/residential/auditResidentialList.jsp'  #楼盘维护
bussinessCirclePage = 'http://isz.ishangzu.com/isz_base/jsp/depbusinesscircle/depBussinessCircleList.jsp'   #门店商圈
transferPage = 'http://isz.ishangzu.com/isz_house/jsp/house/transfer/transferList.jsp'  #转移房源
storePage = 'http://isz.ishangzu.com/isz_house/jsp/store/storeList.jsp'     #门店管理
storeMapPage = 'http://isz.ishangzu.com/isz_house/jsp/store/storeMap.jsp'   #门店楼盘
#房源管理
houseAddPage = 'http://isz.ishangzu.com/isz_house/jsp/house/develop/houseDevelopinfoAdd.jsp'    #新增房源
houseAuditPage = 'http://isz.ishangzu.com/isz_house/jsp/house/develop/houseDevelopList.jsp?from=waitAudit'    #审核房源
devHousePage = 'http://isz.ishangzu.com/isz_house/jsp/house/devhouse/houseList.jsp'   #开发自营房源
resHousePage = 'http://isz.ishangzu.com/isz_house/jsp/house/rent/houseIndex.jsp?from=manageHouseResource'   #资料房源
validHousePage = 'http://isz.ishangzu.com/isz_house/jsp/house/invalid/houseIndex.jsp'   #失效房源
truHousePage = 'http://isz.ishangzu.com/isz_house/jsp/house/trusteeship/houseIndex.jsp'      #托管中的房源
apartmentPage = 'http://isz.ishangzu.com/isz_house/jsp/apartment/apartmentList.jsp?from='    #自营房源
customerAptPage = 'http://isz.ishangzu.com/isz_house/jsp/apartment/apartmentList.jsp?for_customer=1'    #为客配房
#设计工程
designSharePage = 'http://isz.ishangzu.com/isz_house/jsp/design/designShareList.jsp'  # 品牌合租
designEntirePage = 'http://isz.ishangzu.com/isz_house/jsp/design/designEntireList.jsp'  # 品牌整租
designManageSharePage = 'http://isz.ishangzu.com/isz_house/jsp/design/designManageShareList.jsp' #托管合租
#合同管理
generalConractPage = 'http://isz.ishangzu.com/isz_contract/jsp/generalcontract/generallist.jsp'     #普单合同
entrustContractPage = 'http://isz.ishangzu.com/isz_contract/jsp/entrustcontract/contractList.jsp'       #委托合同
apartmentContractPage = 'http://isz.ishangzu.com/isz_contract/jsp/contract/apartmentContract.jsp'       #出租合同
apartmentAchievementPage = 'http://isz.ishangzu.com/isz_achievement/jsp/achievement/apartmentAchievementList.jsp'   #正常出房
backAchievementPage = 'http://isz.ishangzu.com/isz_achievement//jsp/achievement/back/contractAchievementBackList.jsp'       #结算扣回
vacancyAchievementPage = 'http://isz.ishangzu.com/isz_achievement/jsp/achievement/vacancy/apartmentVacancyAchievementList.jsp'      #空置亏损
defaultAchievementPage = 'http://isz.ishangzu.com/isz_achievement/jsp/achievement/default/apartmentDefaultAchievementList.jsp'      #违约业绩
vacancyDatePage = 'http://isz.ishangzu.com/isz_achievement/jsp/achievement/vacancyList.jsp'     #空置日期变更表
contractEndPage = 'http://isz.ishangzu.com/isz_contract/jsp/end/end.jsp'      #终止结算
achievementPage = 'http://isz.ishangzu.com/isz_contract/jsp/contractachievement/achievementIndex.jsp'       #业绩分成
achievementDepPage = 'http://isz.ishangzu.com/isz_contract/jsp/contractachievement/achievementDepList.jsp'      #部门业绩排行榜
achievementUserPage = 'http://isz.ishangzu.com/isz_contract/jsp/contractachievement/achievementUserList.jsp'    #个人业绩排行榜
achievementListPage = 'http://isz.ishangzu.com/isz_achievement/jsp/achievement/achievementList.jsp?type=issuing'    #核发业绩排行榜
achievementListPrePage = 'http://isz.ishangzu.com/isz_achievement/jsp/achievement/achievementList.jsp'  # 预发业绩排行榜
earnestPage='http://isz.ishangzu.com/isz_contract/jsp/earnest/earnestList.jsp'  # 下定列表
earnestBreachPage='http://isz.ishangzu.com/isz_contract/jsp/earnest/earnestBreachList.jsp'#违约金列表
#财务管理
houseContractPayPage = 'http://isz.ishangzu.com/isz_finance/jsp/house/housepay.jsp?tab=1&entrust_type='   #委托合同应付
apartmentContractPayPage = 'http://isz.ishangzu.com/isz_finance/jsp/contractReceivable/apartmentContractReceivableList.jsp'     #出租合同应收
reimbursementExpenseListPage = 'http://isz.ishangzu.com/isz_finance/jsp/expense/reimbursementExpenseList.jsp'   #报销费用
reimbursementExpenseItemListPage = 'http://isz.ishangzu.com/isz_finance/jsp/expense/reimbursementExpenseItemList.jsp'   #报销单详情汇总
houseContractEndPayPage = 'http://isz.ishangzu.com/isz_finance/jsp/houseContractEnd/houseContractEndFlowShouldList.jsp?tab=8&type='     #委托合同终止结算收付
apartmentContractEndPayPage = 'http://isz.ishangzu.com/isz_finance/jsp/apartmentContractEnd/apartmentContractEndFlowShouldList.jsp?tab=3&type=&entrust_type='   #出租合同终止结算收付
depositToReceiptPage= 'http://isz.ishangzu.com/isz_finance/jsp/earnest/turnToReceiptList.jsp'   #定金转入合同实收
depositToBreachPage= 'http://isz.ishangzu.com/isz_finance/jsp/earnest/turnToBreachList.jsp'   #定金转入违约金

