from flask import Flask, render_template, jsonify, send_from_directory
import paho.mqtt.client as mqtt
import threading
import time
import json
import os
import random

app = Flask(__name__)

# 全局变量存储当前状态 / Global variables to store current state
current_state = "no_face"  # 初始状态为无人脸 / Initial state is no face detected
last_face_time = 0  # 上次检测到人脸的时间 / Time when the last face was detected
confidence = 0.0  # 置信度 / Confidence level
current_image = None  # 当前显示的图片 / Currently displayed image

# 获取 static 目录下的所有图片文件 / Get all image files in the static directory
def get_image_list():
    static_dir = os.path.join(app.root_path, 'static')
    return [f for f in os.listdir(static_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# MQTT 回调函数 / MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("成功连接到MQTT代理 / Successfully connected to MQTT broker")
        client.subscribe("sscma/v0/seeed-leon/tx")  # 订阅主题 / Subscribe to the topic
    else:
        print(f"连接失败，返回码: {rc} / Connection failed, return code: {rc}")

def on_message(client, userdata, msg):
    global current_state, last_face_time, confidence, current_image
    try:
        payload = msg.payload.decode("utf-8")
        print(f"原始MQTT消息: {payload} / Raw MQTT message: {payload}")  # 打印完整的MQTT消息 / Print the complete MQTT message
        data = json.loads(payload)
        if data["type"] == 1 and data["name"] == "INVOKE" and data["code"] == 0:
            # 检查 boxes 是否为空 / Check if boxes is empty
            if data["data"]["boxes"]:  # 检测到人脸 / Face detected
                current_state = "face_detected"
                last_face_time = time.time()
                # 提取置信度信息（假设置信度在 boxes 的第一个元素中） / Extract confidence information (assuming confidence is in the 5th position of the first box)
                confidence = data["data"]["boxes"][0][4]  # 置信度在 boxes 的第五个位置 / Confidence is in the 5th position of the box
                print(f"检测到人脸，置信度: {confidence:.2f} / Face detected, confidence: {confidence:.2f}")
                # 随机选择一张图片 / Randomly select an image
                images = get_image_list()
                if images:
                    current_image = random.choice(images)
                    print(f"随机选择的图片: {current_image} / Randomly selected image: {current_image}")
            else:  # 未检测到人脸 / No face detected
                current_state = "no_face"
                current_image = None
                print("未检测到人脸 / No face detected")
    except Exception as e:
        print(f"处理MQTT消息时出错: {e} / Error processing MQTT message: {e}")

# 启动 MQTT 客户端 / Start MQTT client
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()

# Flask 路由 / Flask routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def get_status():
    global current_state, last_face_time, current_image
    # 如果超过 5 秒未检测到人脸，自动切换到黑屏 / If no face is detected for more than 5 seconds, automatically switch to black screen
    if current_state == "face_detected" and time.time() - last_face_time > 5:
        current_state = "no_face"
        current_image = None
    return jsonify({"status": current_state, "image": current_image})

@app.route('/static/<filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# 启动 Flask 应用 / Start Flask application
if __name__ == "__main__":
    # 启动 MQTT 客户端线程 / Start MQTT client thread
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    # 启动 Flask 应用 / Start Flask application
    app.run(host="0.0.0.0", port=5001)