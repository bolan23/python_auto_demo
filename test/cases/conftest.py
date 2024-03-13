import pytest
from falcons.action import PrjAction
from falcons.com.env import User
from falcons.com.meta import EnvContext


def pytest_addoption(parser):
    """Add run options here"""

    # -*-*-*-*-*-*-*-*-*-*-*-*-测试环境配置参数-*-*-*-*-*-*-*-*-*-*-*-*-
    parser.addoption('--host', dest='host', default='', help='指定执行环境')

    parser.addoption('--sprint', dest='sprint', type=str, default='', help='指定后端分支号')
    parser.addoption('--sprint-front', dest='sprint_front', type=str, default='', help='指定前端分支号，前后端分支不一致时传这个值')

    parser.addoption('--member', dest='member', type=str, default='', help='指定测试账号信息')
    parser.addoption('--private', dest='private', type=int, default=1, help='是否私有部署环境 默认1 是，0 否')

    parser.addoption('--ones-debug', dest='ones-debug', type=int, default=1,
                     help='是否调试模式（在IDE中执行）：是： 1，否：0，默认是')

    # -*-*-*-*-*-*-*-*-*-*-*-*-测试环境配置参数-*-*-*-*-*-*-*-*-*-*-*-*-


def _set_env(config):
    """初始化环境信息"""
    _ops = config.getoption

    env_ops = {
        'host': _ops("--host"),
        'sprint': _ops("--sprint"),
        'sprint_front': _ops("--sprint-front"),
        'member': _ops('--member'),
        'private': _ops('--private'),
        'debug': _ops('--ones-debug'),

    }

    return env_ops


def _set_member(env):
    """初始化测试账号"""
    # host:https://devapi.myones.net/project/SP1087a
    # uuid:7CU6yrju
    # user_token:eR5HVehugUpOVXpq018NQgIaXD7cKHfLt3EVRINDFYslCZjAEE02xvEL6Ihb2qhT
    # teamuuid:DajfVCqW
    # org_uuid:7CU6yrju
    # member_uuid:PRdEzWKV
    user_info = env.get('member').split(',')
    assert len(user_info) == 5, f'请检查测试账号信息是否完整！{user_info}'

    u = User('some@ones.ai', 'password')  # 用户名和密码不关注

    u.owner_uuid = user_info[0]
    u.token = user_info[1]
    u.team_uuid = user_info[2]
    u.org_uuid = user_info[3]
    u.member_uuid = user_info[4]

    EnvContext.user = u


def load_env_config():
    """初始化测试账号"""
    # host: https://devapi.myones.net/project/SP1087a
    # uuid: 7CU6yrju
    # user_token: eR5HVehugUpOVXpq018NQgIaXD7cKHfLt3EVRINDFYslCZjAEE02xvEL6Ihb2qhT
    # team_uuid: DajfVCqW
    # org_uuid: 7CU6yrju
    # member_uuid: PRdEzWKV
    import yaml
    import os
    _p = os.path
    path = _p.dirname(__file__)
    try:
        with open(f'{_p.join(path, "env_config.yaml")}', 'r') as f:
            env = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'未查到环境配置文件:env_config.yaml')
    conf = yaml.safe_load(env)

    # Host setup
    gen_host(conf)

    u = User('some@ones.ai', 'password')  # 用户名和密码不关注

    u.owner_uuid = conf['member_uuid']
    u.token = conf['user_token']
    u.org_uuid = conf['org_uuid']
    u.team_uuid = conf['team_uuid']
    u.member_uuid = conf['member_uuid']

    EnvContext.user = u


def pytest_configure(config):
    """Set runtime env globally..."""
    env_ops = _set_env(config)

    is_debug = env_ops.pop('debug')
    if is_debug:  # 直接读取环境 yaml 配置文件
        load_env_config()
    else:  # 从pytest传参数中获取

        # User setup
        _set_member(env_ops)
        # Host setup
        gen_host(env_ops)


def gen_host(conf: dict):
    """Host setup"""
    EnvContext.host = conf['host']
    EnvContext.sprint = conf['sprint']
    EnvContext.sprint_front = conf['sprint_front']

    label = 'private' if conf['private'] else 'dev'

    EnvContext.label = label


@pytest.hookspec(firstresult=True)
def pytest_collection(session):
    """
    pytest_collection 这个fixture 在用例收集阶段执行
    pytest 收集用例执行前 如有一下数据需要生成请在这里处理
    :param session:
    :return:
    """
    # 如有需要自行添加
    p_uuid = PrjAction.new_project()
    EnvContext.project_uuid = p_uuid


def pytest_collection_modifyitems(items):
    """终端显示中文乱码问题"""
    for item in items:  # stdout  中文乱码问题
        item.name = item.name.encode().decode('unicode-escape')
        item._nodeid = item._nodeid.encode().decode('unicode-escape')


# -*******-*******-*******-*******-*******-*******-*******-*******-*******-*******


@pytest.fixture(scope='session', autouse=True)
def clean_data():
    """
    在全局用例执行完成后执行测试数据清理动作
    :return:
    """

    yield

    # 测试数据清理动作 如有需要自行添加
    p_uuid = EnvContext.project_uuid
    PrjAction.delete_project(p_uuid)

# -*******-*******-*******-*******-*******-*******-*******-*******-*******-*******
