# 人脸检测与图片展示系统

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
