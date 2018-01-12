## old：为避免每次版本迭代上线后，回归不全导致未改动的模块产生新的问题，同时为了解放重复的流程回归测试，所以有了这个业务流程自动化回归项目的初版。

## new：与另一版本不同，当前项目为细化用例的自动化


### 项目基于 Python2.7、selenium3.0 框架

### 主要目录：（和后台系统中的项目保持一致）
* base
> 各目录中的 __init__.py 是为了声明当前目录是一个Package，便于其他模块import调用

* Base.py
> 对webDriver类中的常用方法的二次封装以及其他的常用方法的定义

* Page.py
> 各web页面的实际地址

* SQL.py
> 对数据库的操作

* conf.ini
> 数据库连接、host、执行环境等信息的配置

* test.py
> 轮询指定目录下所有test开头的用例文件，并按照指定线程开始执行用例

* test.log
> 每次用例执行完毕后将生成此文件（相当于测试报告），共jenkins调用打印

* user
> 系统中用户管理模块中的各page

* house
> 系统中的房源管理模块中的各page.......


### 注意事项（必须遵循项）

* 文件目录规则如   contract/apartment_contract/apartmentContractPage.py、testAddHouse.py

* 定位页面的文件按照需要放入各目录（包）中

* 定位页面的文件需以 Page 结尾，如 houseContractPage.py

* 定位页面只允许有元素定位代码，不可包含其他任何代码

    * 测试用例文件无需为类，只定义函数，需 from common.Base import Base

    * Base类中定义了上下文管理器用来传递实例，所以用例中实例化Base类时，需使用with语句

    * 需引入装饰器 log ，需添加  """方法说明，简要描述当前方法的作用"""

    * 如果存在可能的未知异常，捕获后不要处理，让其向上抛出， log 装饰器接收后，会作相应处理

    * 只关心业务逻辑，需要调用的方法、页面、定位都从 xxPage 及 Base 中引用

* 测试结果体现在 test.log 文件中，jenkins 会打印此文件的内容，每次构建完毕后，需关注 jenkins 的Console Output

