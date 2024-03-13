# abilityExec

1、可被查询的能力列表，记录开放平台后端能力版本等情况
2、开放能力自动化测试的相关用例


# 用法

## 本地调试

 在e397环境 用例依赖库安装

首先配置pip源
cat ~/.pip/pip.conf
内容如下

[global]
index-url =  http://119.23.154.208/repository/ones/simple 
[install]
trusted-host=119.23.154.208


执行下边的命令：
LTS版本（1.3.0），所以这里指定安装1.3.0版本
```shell
安装 falcons
echo y | pip uninstall falcons && pip install falcons==1.3.0

安装 atcions
echo y | pip uninstall ones_actions && pip install ones_actions
```


Latest版本
```shell
安装 falcons
echo y | pip uninstall falcons && pip install falcons

安装 atcions
echo y | pip uninstall ones_actions && pip install ones_actions
```

安装 gitlab下载依赖
```shell

pip install python-gitlab

# pip3 uninstall gitlab
# pip3 install python-gitlab

备注：如果之前两个都安装，建议都删除，再重新安装python-gitlab

```

安装 playwright
```shell

playwright install

备注：如果运行代码涉及ui部分，调试时本地需要下载playwright

```

## 插件下载


在 `plugin_init.py`文件的`install_List`变量中 中添加需要被下载插件的配置文件路径，如ability/apiAbility/projectPre/1.0.0.yaml


## 环境配置填写
在 `env_config.yaml` 文件按照格式填写属性信息。

或使用 login.py 登录

```shell

python3 login.py http://39.108.103.2:10020 shenzhen2@ones.ai cX9ZGUGB UpGPTSLV

在login.py 文件后面分别填写ONES实例地址、管理员账号、管理员密码、测试团队UUID

```



## 用例编写

1.定义被测接口

新建一个测试模块， `test_some_api.py`, 添加如下代码

```python
...
from falcons.ops import ProjectOps


class SomeApi(ProjectOps):
    uri = 'api/uri/address/{some_variable_value}'
    name = 'API NAME'
    api_type = 'POST'


...

```

2.定义测试参数

继续在定义接口的参数，使用 `generate_param`，可快速生成测试参数对象。

```python
...
from falcons.ops import generate_param


def normal_param():
    """一条测试用例数据"""
    return generate_param({'some': 'test param value'})


...

```

3.测试用例实现

添加一个 `Test`开头的类来管理测试用例

```python
from falcons.ops import ProjectOps
from falcons.check import Checker
from falcons.ops import generate_param
from falcons.com.nick import step, story, feature, parametrize


class SomeApi(ProjectOps):
    uri = 'api/uri/address/{some_variable_value}'
    name = 'API NAME'
    api_type = 'POST'


def normal_param():
    """一条测试用例数据"""
    return generate_param({'some': 'test param value'})


@feature('SOME API TEST CASES')
class TestSomeApi(Checker):
    @story('测试用例正常返回-200')
    @parametrize('param', normal_param())
    def test_case_demo_1(self, param, token):
        with step('发起SomeApi接口请求'):
            resp = self.call(SomeApi, param, token)

        with step('检查接口响应值'):
            resp.check_response('some', param.json_value('some'))
```


## TO BE CONTINUED

基于`Pytest`,`Selenium`, `Allure`。
