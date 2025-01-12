import paho.mqtt.client as mqtt
import json
import time
import sys
import threading
from queue import Queue
import os

class DisplayController:
    def __init__(self):
        # 初始化显示状态
        self.display_image = False
        self.last_face_time = 0
        self.running = True
        
        # 创建消息队列
        self.message_queue = Queue()
        
        # 启动显示线程
        self.display_thread = threading.Thread(target=self._display_loop)
        self.display_thread.daemon = True
        self.display_thread.start()

    def clear_terminal(self):
        """清除终端内容"""
        os.system('clear')

    def process_mqtt_message(self, message):
        """处理MQTT消息"""
        try:
            if isinstance(message, bytes):
                message = message.decode('utf-8')
            print(f"原始MQTT消息: {message}")  # 打印原始消息
            data = json.loads(message)
            if data["type"] == 1 and data["name"] == "INVOKE" and data["code"] == 0:
                face_detected = data["data"]["count"] > 0
                print(f"收到消息: {'检测到人脸' if face_detected else '未检测到人脸'}")
                self.message_queue.put(face_detected)
        except Exception as e:
            print(f"处理消息时出错: {e}")

    def _display_loop(self):
        """显示控制循环"""
        self.clear_terminal()
        
        while self.running:
            try:
                current_time = time.time()
                display_changed = False
                
                # 处理消息队列
                while not self.message_queue.empty():
                    face_detected = self.message_queue.get_nowait()
                    if face_detected:
                        if not self.display_image:
                            print("开始显示图片（文本模式）")
                            display_changed = True
                        self.last_face_time = current_time
                        self.display_image = True
                    else:
                        if self.display_image:
                            print("未检测到人脸，关闭图片（文本模式）")
                            display_changed = True
                        self.display_image = False
                
                # 检查是否需要切换显示
                if self.display_image and current_time - self.last_face_time > 1:
                    print("1秒内未检测到人脸，关闭图片（文本模式）")
                    self.display_image = False
                    display_changed = True
                
                # 更新显示
                if display_changed:
                    self.clear_terminal()
                    if self.display_image:
                        print("正在显示图片（文本模式）")
                    else:
                        print("正在显示黑屏（文本模式）")
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"显示循环出错: {e}")
                time.sleep(0.1)
                continue

    def stop(self):
        """停止显示控制器"""
        print("正在停止显示控制器...")
        self.running = False
        if self.display_thread and self.display_thread.is_alive():
            self.display_thread.join(timeout=2.0)
        print("程序已完全退出")

def main():
    controller = None
    client = None
    
    try:
        # 创建显示控制器
        controller = DisplayController()
        
        # 设置MQTT客户端
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("成功连接到MQTT代理")
                topic = "sscma/v0/seeed-leon/tx"
                client.subscribe(topic)
                print(f"已订阅主题: {topic}")
            else:
                print(f"连接失败，返回码: {rc}")
        
        def on_message(client, userdata, msg):
            print(f"收到MQTT消息，主题: {msg.topic}")
            controller.process_mqtt_message(msg.payload)
        
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        
        # 连接到MQTT代理
        broker = "broker.emqx.io"
        port = 1883
        print(f"正在连接到MQTT代理: {broker}:{port}")
        
        client.connect(broker, port, 60)
        client.loop_start()
        
        # 等待用户退出
        print("程序运行中，按 Ctrl+C 退出...")
        while controller.running:
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序出错: {e}")
    finally:
        if client:
            client.loop_stop()
            client.disconnect()
        if controller:
            controller.stop()
        print("程序已完全退出")

if __name__ == "__main__":
    main()