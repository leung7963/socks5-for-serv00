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


def batch_test_hosts(proxies):
    failed_hosts = False
    for proxy in proxies:
        ip, port, _, _ = proxy
        host = f"{ip}:{port}"
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


def load_proxies_from_env():
    proxy_data = os.environ.get("PROXY_DATA", "")
    proxies = []
    for line in proxy_data.splitlines():
        line = line.strip()  # 移除换行符和多余的空白
    return proxies


# 执行加载代理信息并进行批量测试
proxies = load_proxies_from_env()
batch_test_hosts(proxies)