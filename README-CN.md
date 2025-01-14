# 基于MQTT 的人脸检测与图片展示系统

**[English](README.md)** | **[中文简体]**

## 项目简介

本项目是一个基于 Flask 和 MQTT 的人脸检测与图片展示系统。系统通过 MQTT 协议接收来自设备的**[人脸检测](https://sensecraft.seeed.cc/ai/#/model/detail?id=60769&tab=public)**结果，并根据检测结果动态展示图片。当检测到人脸时，系统会随机选择一张图片进行展示；如果超过 5 秒未检测到人脸，系统会自动切换到黑屏状态。

## 功能特性

- **人脸检测**: 通过 MQTT 接收人脸检测结果，实时更新系统状态。
- **图片展示**: 当检测到人脸时，随机选择一张图片进行展示。
- **自动黑屏**: 如果超过 5 秒未检测到人脸，系统会自动切换到黑屏状态。
- **跨平台**: 支持 macOS 和 Windows 操作系统。

## 技术栈

- **Flask**: 用于构建 Web 应用，提供状态查询和图片展示功能。
- **MQTT**: 用于接收来自设备的人脸检测结果。
- **Python**: 项目的主要编程语言。

## 安装与使用

### 环境要求

- Python 3.x
- Flask
- paho-mqtt

### 安装步骤

1. **克隆仓库**

   ```bash
   git clone https://github.com/mouseart/MQTT-test.git
   cd MQTT-test
   ```
2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```
3. **运行项目**

   ```bash
   python app.py
   ```
4. **访问应用**

   打开浏览器，访问 `http://localhost:5001`，即可看到系统状态和图片展示。

### 配置文件

- **静态图片**: 将需要展示的图片放入 `static` 目录下，支持 `.png`, `.jpg`, `.jpeg`, `.gif` 格式。

## 配置 MQTT 代理服务器

默认情况下，项目使用公共的 MQTT 代理服务器 `broker.emqx.io`。如果你需要使用自己的 MQTT 代理服务器，可以按照以下步骤进行配置：

### 1. 修改 `app.py` 文件中的 MQTT 配置

在 `app.py` 文件中，找到以下代码段：

```python
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.emqx.io", 1883, 60)  # 默认使用公共 MQTT 代理
    client.loop_start()
```

将 `client.connect("broker.emqx.io", 1883, 60)` 中的 `"broker.emqx.io"` 替换为你自己的 MQTT 代理服务器地址。例如，如果你的 MQTT 代理服务器地址是 `mqtt.example.com`，端口是 `1883`，则修改为：

```python
client.connect("mqtt.example.com", 1883, 60)
```

### 2. 配置 MQTT 主题

默认情况下，项目订阅的主题是 `sscma/v0/seeed-leon/tx`。如果你需要更改订阅的主题，可以在 `app.py` 文件中找到以下代码段：

```python
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("成功连接到MQTT代理 / Successfully connected to MQTT broker")
        client.subscribe("sscma/v0/seeed-leon/tx")  # 订阅主题 / Subscribe to the topic
    else:
        print(f"连接失败，返回码: {rc} / Connection failed, return code: {rc}")
```

将 `client.subscribe("sscma/v0/seeed-leon/tx")` 中的 `"sscma/v0/seeed-leon/tx"` 替换为你自己的 MQTT 主题。

### 3. 运行项目

完成配置后，重新运行项目：

```bash
python app.py
```

### 4. 验证连接

确保你的 MQTT 代理服务器正在运行，并且客户端能够成功连接到服务器。你可以在 `app.py` 的日志中查看连接状态。

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建新的分支 (`git checkout -b feature/YourFeatureName`)
3. 提交你的更改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/YourFeatureName`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有任何问题或建议，请联系 [mouseart2003@gmail.com](mouseart2003@gmail.com)。

---

感谢您的关注与支持！
