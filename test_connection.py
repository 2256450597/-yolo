"""
网络连接诊断工具
用于测试客户端和服务器之间的 Socket 连接
"""
import socket
import sys

def test_server_connection(host='localhost', port=50000):
    """测试服务器连接"""
    print(f'正在测试连接到 {host}:{port}...')
    print('=' * 60)
    
    try:
        # 创建 Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3.0)
        
        # 尝试连接
        print(f'1. 创建 Socket: ✅')
        print(f'2. 设置超时: ✅')
        print(f'3. 尝试连接到 {host}:{port}...')
        
        result = s.connect_ex((host, port))
        
        if result == 0:
            print(f'✅ 连接成功！')
            print(f'   服务器 {host}:{port} 正在运行')
            
            # 发送测试数据
            test_data = '{"frame_id": 0, "objects": []}\n'
            s.sendall(test_data.encode('utf-8'))
            print(f'✅ 测试数据发送成功')
            
            s.close()
            return True
        else:
            error_code = socket.errorTab.get(result, 'Unknown')
            print(f'❌ 连接失败！')
            print(f'   错误代码: {result} ({error_code})')
            print(f'   可能原因:')
            print(f'   1. 服务器未启动（运行 python detection_server.py）')
            print(f'   2. 端口 {port} 未被监听')
            print(f'   3. 防火墙阻止了连接')
            s.close()
            return False
            
    except socket.timeout:
        print(f'❌ 连接超时！')
        print(f'   服务器 {host}:{port} 无响应')
        return False
    except ConnectionRefusedError:
        print(f'❌ 连接被拒绝！')
        print(f'   服务器 {host}:{port} 拒绝连接')
        print(f'   可能原因: 服务器未启动或端口未监听')
        return False
    except OSError as e:
        print(f'❌ 连接错误: {e}')
        return False
    except Exception as e:
        print(f'❌ 未知错误: {e}')
        return False

def check_port_status(port=50000):
    """检查端口状态"""
    print(f'\n检查端口 {port} 状态...')
    import subprocess
    try:
        result = subprocess.run(
            ['netstat', '-ano', '|', 'findstr', f':{port}'],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f'端口 {port} 被以下进程占用:')
            print(result.stdout)
        else:
            print(f'端口 {port} 未被占用')
    except Exception as e:
        print(f'无法检查端口状态: {e}')

if __name__ == '__main__':
    host = 'localhost'
    port = 50000
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f'错误：无效的端口号，使用默认端口 50000')
    
    print('=' * 60)
    print('Socket 连接诊断工具')
    print('=' * 60)
    
    # 检查端口状态
    check_port_status(port)
    
    print('\n')
    # 测试连接
    success = test_server_connection(host, port)
    
    print('=' * 60)
    if success:
        print('✅ 诊断完成：连接正常')
    else:
        print('❌ 诊断完成：连接失败，请检查服务器状态')
    print('=' * 60)

