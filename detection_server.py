"""
检测结果服务器端
功能：接收客户端发送的检测结果数据，进行存储和显示
"""
import socket
import json
import threading
from datetime import datetime
from collections import defaultdict

class DetectionServer:
    """检测结果服务器类（纯 TCP Socket，不依赖任何 Web 框架）"""
    
    def __init__(self, host='localhost', port=50000):
        """
        初始化服务器
        
        参数:
            host: 服务器主机地址
            port: 服务器端口号
        """
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        # 存储检测结果（内存存储）
        self.detection_results = []
        # 按类别统计（可选）
        self.class_statistics = defaultdict(int)
        # 按帧号索引的检测结果
        self.frame_detections = {}
    
    def start(self):
        """启动服务器"""
        try:
            # 创建Socket对象
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置端口复用（允许端口被快速重用）
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 绑定地址和端口（纯 Socket TCP，不涉及 Web 服务）
            try:
                self.socket.bind((self.host, self.port))
            except OSError as bind_error:
                if bind_error.winerror == 10013 or bind_error.errno == 13:
                    print(f'❌ 错误：端口 {self.port} 被占用或需要管理员权限')
                    print(f'   解决方案：')
                    print(f'   1. 检查是否有其他程序占用了端口 {self.port}')
                    print(f'   2. 或者尝试使用其他端口（修改代码中的 port 参数）')
                    print(f'   3. 在 Windows 上检查端口占用：netstat -ano | findstr :{self.port}')
                else:
                    print(f'❌ 绑定端口时出错：{bind_error}')
                raise
            # 开始监听，最大连接数为5
            self.socket.listen(5)
            self.running = True
            
            print(f'=' * 60)
            print(f'✅ 检测结果服务器已启动（纯 TCP Socket）')
            print(f'📍 监听地址: {self.host}:{self.port}')
            print(f'⏳ 等待客户端连接...')
            print(f'=' * 60)
            
            # 接受客户端连接
            while self.running:
                try:
                    # 接受客户端连接（纯 Socket TCP 通信）
                    client_socket, client_address = self.socket.accept()
                    print(f'\n✅ 客户端已连接：{client_address}')
                    print(f'   开始接收检测结果数据...')
                    
                    # 为每个客户端创建新线程处理
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        print(f'接受连接时出错：{e}')
        except Exception as e:
            print(f'启动服务器时出错：{e}')
        finally:
            self.stop()
    
    def handle_client(self, client_socket, client_address):
        """
        处理客户端连接
        
        参数:
            client_socket: 客户端Socket对象
            client_address: 客户端地址
        """
        try:
            # 设置接收超时（避免无限等待）
            client_socket.settimeout(30.0)  # 30秒超时
            # 创建缓冲区
            buffer = ''
            
            while self.running:
                try:
                    # 接收数据
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    
                    # 解码数据并添加到缓冲区
                    buffer += data.decode('utf-8')
                except socket.timeout:
                    # 超时，但连接仍然有效，继续等待
                    continue
                
                # 按换行符分割数据（纯 Socket TCP 通信，每行是一个 JSON 对象）
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if line:
                        # 检查是否是有效的 JSON 数据（以 { 开头）
                        # 过滤掉非 JSON 数据（如 HTTP 请求头等）
                        if line.startswith('{'):
                            # 处理接收到的 JSON 数据
                            self.process_detection_data(line, client_address)
                        else:
                            # 忽略非 JSON 数据（可能是 HTTP 请求或其他协议）
                            pass
        except Exception as e:
            print(f'处理客户端 {client_address} 数据时出错：{e}')
        finally:
            # 关闭客户端连接
            client_socket.close()
            print(f'客户端 {client_address} 已断开连接')
    
    def process_detection_data(self, json_data, client_address):
        """
        处理接收到的检测结果数据
        
        参数:
            json_data: JSON格式的字符串数据
            client_address: 客户端地址
        """
        try:
            # 解析JSON数据
            detection_data = json.loads(json_data)
            
            # 添加时间戳
            detection_data['timestamp'] = datetime.now().isoformat()
            detection_data['client_address'] = str(client_address)
            
            # 存储检测结果
            self.detection_results.append(detection_data)
            
            # 按帧号索引存储
            frame_id = detection_data.get('frame_id', -1)
            self.frame_detections[frame_id] = detection_data
            
            # 更新类别统计（可选）
            for obj in detection_data.get('objects', []):
                class_name = obj.get('class', 'unknown')
                self.class_statistics[class_name] += 1
            
            # 显示检测结果（终端输出）
            self.display_detection_result(detection_data)
            
        except json.JSONDecodeError as e:
            # JSON 解析错误（可能是数据格式不正确）
            print(f'⚠ JSON解析错误：{e}')
            if len(json_data) > 100:
                print(f'   原始数据（前100字符）：{json_data[:100]}...')
            else:
                print(f'   原始数据：{json_data}')
        except Exception as e:
            print(f'处理检测数据时出错：{e}')
    
    def display_detection_result(self, detection_data):
        """
        显示检测结果（终端输出）
        
        参数:
            detection_data: 检测结果字典
        """
        frame_id = detection_data.get('frame_id', -1)
        objects = detection_data.get('objects', [])
        timestamp = detection_data.get('timestamp', '')
        
        print(f'\n[{timestamp}] 帧号: {frame_id}')
        print(f'检测到 {len(objects)} 个对象:')
        
        for obj in objects:
            class_name = obj.get('class', 'unknown')
            x = obj.get('x', 0)
            y = obj.get('y', 0)
            w = obj.get('w', 0)
            h = obj.get('h', 0)
            print(f'  {class_name}: x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f}')
        
        # 显示统计信息（可选）
        if self.class_statistics:
            print(f'累计统计: {dict(self.class_statistics)}')
    
    def save_results_to_file(self, filename='detection_results.json'):
        """
        将检测结果保存到文件
        
        参数:
            filename: 保存的文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.detection_results, f, ensure_ascii=False, indent=2)
            print(f'检测结果已保存到文件：{filename}')
        except Exception as e:
            print(f'保存结果到文件时出错：{e}')
    
    def get_statistics(self):
        """
        获取统计信息
        
        返回:
            dict: 统计信息字典
        """
        return {
            'total_frames': len(self.frame_detections),
            'total_detections': len(self.detection_results),
            'class_statistics': dict(self.class_statistics)
        }
    
    def stop(self):
        """停止服务器"""
        self.running = False
        if self.socket:
            self.socket.close()
        print('服务器已停止')
    
    def clear_results(self):
        """清空检测结果"""
        self.detection_results.clear()
        self.frame_detections.clear()
        self.class_statistics.clear()
        print('检测结果已清空')


def main():
    """主函数"""
    import sys
    
    # 默认端口 50000，可以通过命令行参数指定
    port = 50000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f'错误：无效的端口号 "{sys.argv[1]}"，使用默认端口 50000')
    
    # 创建服务器实例（纯 TCP Socket 服务器）
    print(f'正在启动服务器，使用端口：{port}')
    server = DetectionServer(host='localhost', port=port)
    
    try:
        # 启动服务器
        server.start()
    except KeyboardInterrupt:
        print('\n正在停止服务器...')
        # 保存结果到文件
        server.save_results_to_file()
        # 显示统计信息
        stats = server.get_statistics()
        print(f'\n统计信息：{stats}')
        # 停止服务器
        server.stop()
    except Exception as e:
        print(f'\n服务器启动失败：{e}')
        print(f'\n提示：')
        print(f'  1. 检查端口 {port} 是否被占用')
        print(f'  2. 尝试使用其他端口：python detection_server.py 9999')
        print(f'  3. 检查防火墙设置')


if __name__ == '__main__':
    main()

