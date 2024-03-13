import os
import shutil

import requests
import yaml
import gitlab

privateToken = 'saxxjoNqcb3ydvE2nL1y'
gitlabUrl = 'https://gitlab.plugins.myones.net'

# 需要下载的能力插件文件的配置文件路径
install_List = [
    # app
    "/ability/app/project/task_event_handler/1.0.0.yaml",
    "/ability/app/project/customize_project_components/1.0.0.yaml",
    "/ability/app/project/dashboard_card/1.0.0.yaml",
    "/ability/app/project/intercept_item_actions/1.0.0.yaml",
    "/ability/app/wiki/wiki_macro/1.0.0.yaml",
    "/ability/app/project/customize_project_components/1.0.0.yaml",
    "/ability/app/project/customize_issue_fields/1.0.0.yaml",
    "/ability/app/devops/integration_code_repository/1.0.0.yaml"
    # platform
    "/ability/platform/sidebar_menu/1.0.0.yaml",
    "/ability/platform/ones_notice/email_interception/1.0.0.yaml",
    "/ability/platform/independent_hosting_service/1.0.0.yaml",
    "/ability/platform/item_mutation/1.0.0.yaml",
    "/ability/platform/get_plugin_ability_config/1.0.0.yaml"
]

opkPath = './test/tmp/opk/'
pluginPath = './test/tmp/plugins/'
lifecyclePath = './test/tmp/lifecycle/'


def getGitlabLinks(url, project_name, file_type):
    path = ''
    if file_type == 'yaml':
        path = pluginPath + project_name + '-plugin.yaml'
    if file_type == 'opk':
        path = opkPath + project_name + '.opk'
    if 1 != os.path.exists(path):
        print('正在下载..' + path + ' 文件')
        res = requests.get(url, headers={
            'private-token': privateToken
        })
        if res.status_code == 200:
            with open(path, 'wb') as f:
                f.write(res.content)
        else:
            print('下载' + path + '失败')


def emptyFolder(pathName):
    if 1 == os.path.exists(pathName):
        shutil.rmtree(pathName)


# private token or personal token authentication (self-hosted GitLab instance)
def download_opk():
    gl = gitlab.Gitlab(url=gitlabUrl, private_token=privateToken)
    # 下载能力插件对应的配置路径
    wd = os.getcwd()
    emptyFolder(opkPath)
    os.makedirs(opkPath)
    emptyFolder(pluginPath)
    os.makedirs(pluginPath)
    emptyFolder(lifecyclePath)
    os.makedirs(lifecyclePath)

    for i in install_List:
        try:
            # 打开文件
            with open(wd + i, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            # 拿到release
            if 'release' in data:
                release = data['release']
                # 解析拿到 project ID
                release_array = release.split('/')
                if len(release_array) > 8:
                    project_id = release_array[6]
                    version = release_array[8]
                    project_name = release_array[6] + '-' + release_array[8]
                    project = gl.projects.get(project_id)
                    # 解析拿到 release版本
                    release = project.releases.get(version)
                    # 拿到release link
                    links = release.links.list()
                    for link in links:
                        if '.yaml' in link.name:
                            getGitlabLinks(link.url, project_name, 'yaml')
                        # 下载 opk 到test/tmp/opk
                        if '.opk' in link.name:
                            getGitlabLinks(link.url, project_name, 'opk')
                else:
                    print('解析' + release + '失败或文件内容有误！')
        except IOError as ie:
            print('File Error :', ie)
        except (Exception,):
            print('未知错误')


if __name__ == '__main__':
    download_opk()
