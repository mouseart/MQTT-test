# MQTT-Based Face Detection and Image Display System

**[English]** | **[中文简体](README-CN.md)**

## Project Introduction

This project is a face detection and image display system based on Flask and MQTT. The system receives **[face detection](https://sensecraft.seeed.cc/ai/#/model/detail?id=60769&tab=public)** results from devices via the MQTT protocol and dynamically displays images based on the detection results. When a face is detected, the system randomly selects an image to display; if no face is detected for more than 5 seconds, the system automatically switches to a black screen.

## Features

- **Face Detection**: Receives face detection results via MQTT and updates the system status in real-time.
- **Image Display**: Randomly selects an image to display when a face is detected.
- **Automatic Black Screen**: Automatically switches to a black screen if no face is detected for more than 5 seconds.
- **Cross-Platform**: Supports both macOS and Windows operating systems.

## Technology Stack

- **Flask**: Used to build the web application, providing status query and image display functionality.
- **MQTT**: Used to receive face detection results from devices.
- **Python**: The primary programming language of the project.

## Installation and Usage

### Environment Requirements

- Python 3.x
- Flask
- paho-mqtt

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mouseart/MQTT-test.git
   cd MQTT-test
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project**

   ```bash
   python app.py
   ```

4. **Access the Application**

   Open your browser and visit `http://localhost:5001` to see the system status and image display.

### Configuration

- **Static Images**: Place the images you want to display in the `static` directory. Supported formats include `.png`, `.jpg`, `.jpeg`, and `.gif`.

## Configuring the MQTT Broker

By default, the project uses the public MQTT broker `broker.emqx.io`. If you need to use your own MQTT broker, follow these steps:

### 1. Modify the MQTT Configuration in `app.py`

In the `app.py` file, locate the following code segment:

```python
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.emqx.io", 1883, 60)  # Default public MQTT broker
    client.loop_start()
```

Replace `"broker.emqx.io"` with your own MQTT broker address. For example, if your MQTT broker address is `mqtt.example.com` and the port is `1883`, modify it as follows:

```python
client.connect("mqtt.example.com", 1883, 60)
```

### 2. Configure the MQTT Topic

By default, the project subscribes to the topic `sscma/v0/seeed-leon/tx`. If you need to change the subscription topic, locate the following code segment in the `app.py` file:

```python
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to MQTT broker")
        client.subscribe("sscma/v0/seeed-leon/tx")  # Subscribe to the topic
    else:
        print(f"Connection failed, return code: {rc}")
```

Replace `"sscma/v0/seeed-leon/tx"` with your own MQTT topic.

### 3. Run the Project

After completing the configuration, restart the project:

```bash
python app.py
```

### 4. Verify the Connection

Ensure that your MQTT broker is running and that the client can successfully connect to the server. You can check the connection status in the logs of `app.py`.

## Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a new branch (`git checkout -b feature/YourFeatureName`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeatureName`)
5. Create a Pull Request

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file.

## Contact

If you have any questions or suggestions, please contact [mouseart2003@gmail.com](mailto:mouseart2003@gmail.com).

---

Thank you for your attention and support!