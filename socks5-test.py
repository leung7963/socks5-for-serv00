import socket


def test_connection(domain_port_str):
    try:
        domain, port_str = domain_port_str.split(':')
        port = int(port_str)
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
    except ValueError:
        print(f"{domain_port_str} 端口格式转换出错，请检查格式")



# 获取GitHub环境变量中存放的域名和端口信息字符串
domains_ports_str = os.environ.get('PROXY_DATA')
if domains_ports_str:
    lines = domains_ports_str.splitlines()
    for line in lines:
        domain, port = line.strip().split(' ')
        port = int(port)
        test_connection(domain, port)
else:
    print("未获取到有效的DOMAINS_PORTS环境变量内容")