import os
import requests
from requests.exceptions import RequestException
from pythonping import ping


def trigger_github_action():
    github_token = os.environ.get("GITHUB_TOKEN")  # 从环境变量中获取GitHub token
    repo = "leung7963/socks5-for-serv00"  # 替换为要触发的GitHub仓库
    workflow_id = "nezha.yaml"  # 替换为要触发的工作流ID或文件名
    api_url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_id}/dispatches"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "ref": "main"  # 触发工作流的分支
    }

    try:
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 204:
            print("GitHub Action triggered successfully.")
        else:
            print(f"Failed to trigger GitHub Action: {response.status_code} - {response.text}")
    except RequestException as e:
        print(f"Error triggering GitHub Action: {e}")


def test_icmp_latency(host):
    try:
        domain, port = host.split(':')  # 分离域名和端口
        result = ping(target=domain, count=1, timeout=10)  # 发送1次ICMP请求，超时时间设为10秒
        latency = result.rtt_avg_ms  # 获取平均往返时间（以毫秒为单位）
        print(f"{host}: ICMP Latency: {latency:.2f} ms")
        return latency
    except ValueError:
        print(f"Invalid host format: {host}. Skipping.")
        return None
    except Exception as e:
        print(f"{host}: ICMP Error: {e}")
        return None


def batch_test_hosts(hosts_file_path):
    hosts = []
    with open(hosts_file_path, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if line:
                hosts.append(line)

    failed_hosts = False
    for host in hosts:
        latency = test_icmp_latency(host)
        if latency is None:
            print(f"{host}: failed.")
            failed_hosts = True
        else:
            print(f"{host} Latency: {latency:.2f} ms")

    if failed_hosts:
        print("Some hosts failed. Triggering GitHub Action.")
        trigger_github_action()
    else:
        print("All hosts succeeded. No need to trigger GitHub Action.")


# 指定存储域名和端口信息的文件路径，这里假设文件在当前目录下名为hosts.txt，你可按需修改
hosts_file_path = "hosts.txt"
# 执行批量测试
batch_test_hosts(hosts_file_path)