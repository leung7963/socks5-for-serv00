import socket
import os


def trigger_github_action():
    # 清除全局代理设置，确保不使用代理
    socks.set_default_proxy()  # 清除之前设置的代理
    socket.socket = socks.socksocket  # 恢复原始 socket 连接

    github_token = os.environ.get("GITHUB_TOKEN")  # 从环境变量中获取 GitHub token
    repo = "leung7963/socks5-for-serv00"  # 替换为要触发的 GitHub 仓库
    workflow_id = "nezha.yaml"  # 替换为要触发的工作流 ID 或文件名
    api_url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "ref": "main"  # 触发工作流的分支
    }
    
    try:
        # 请求 GitHub API 时不使用代理
        response = requests.post(api_url, json=data, headers=headers)
        
        if response.status_code == 204:
            print("GitHub Action triggered successfully.")
        else:
            print(f"Failed to trigger GitHub Action: {response.status_code} - {response.text}")
    except RequestException as e:
        print(f"Error triggering GitHub Action: {e}")
        
        
def test_connection(domain, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)  # 设置超时时间，单位秒
        result = sock.connect_ex((domain, port))
        sock.close()
        if result == 0:
            print(f"{domain}:{port} 连接成功")
        else:
            print(f"{domain}:{port} 连接失败")
    except socket.gaierror:
        print(f"{domain}:{port} 域名解析出错")
    except socket.timeout:
        print(f"{domain}:{port} 连接超时")


# 获取GitHub环境变量中存放的域名和端口信息字符串
domains_ports_str = os.environ.get('PROXY_DATA')
if domains_ports_str:
    lines = domains_ports_str.splitlines()
    for line in lines:
        domain, port = line.strip().split(':')
        port = int(port)
        test_connection(domain, port)
else:
    print("未获取到有效的DOMAINS_PORTS环境变量内容")