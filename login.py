import http
import sys
import requests
import yaml


def login_dev(private_host, user_email, user_password, team_uuid):
    headers = {
        'Content-Type': 'application/json',
    }
    data = '{ "email": "' + user_email + '", "password":"' + user_password + '"}'
    res = requests.post(private_host + '/project/api/project/auth/login', headers=headers, data=data)
    if res.status_code == http.HTTPStatus.OK:
        login_data = res.json()
        env_config = {
            "host": private_host,
            "user_uuid": login_data['user']['uuid'],
            "user_token": login_data['user']['token'],
            "team_uuid": team_uuid,
            "org_uuid": login_data['org']['uuid'],
            "member_uuid": login_data['user']['uuid'],
            "private": True,
            "sprint": "",
            "sprint_front": "",
        }
        try:
            # 打开文件
            with open('test/cases/env_config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(data=env_config, stream=f, allow_unicode=True)
        except IOError as ai:
            print("\nWrong content written to lifeCycle.yaml file", ai)
            return None
        except AttributeError as aa:
            print("\nWrong content written to lifeCycle.yaml file", aa)
            return None
    else:
        print("登录测试环境失败!!!")
        sys.exit()


if __name__ == '__main__':
    host = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    team_uuid = sys.argv[4]
    print("host:", host)
    print("email:", email)
    print("password:", password)
    print("team_uuid:", team_uuid)
    login_dev(host, email, password, team_uuid)


