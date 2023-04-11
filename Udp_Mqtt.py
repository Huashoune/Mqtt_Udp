from paho.mqtt import client as mqtt
from socket import *


UDP_HOST = '192.168.0.238'
UDP_PORT = 3964
MQTT_HOST ='43.143.48.34'
MQTT_PORT = 1883
MQTT_USER = 'eryuan'
MQTT_PASS = 'bayes123'
CLIENT_ID = 'BAYES_UDPTOMQTT'


udp_socket = socket(AF_INET, SOCK_DGRAM)
dest_addr = (UDP_HOST, UDP_PORT)
def on_connect(client, userdata, flags, rc):
    """一旦连接成功, 回调此方法"""
    rc_status = ["连接成功", "协议版本错误", "无效的客户端标识", "服务器无法使用", "用户名或密码错误", "无授权"]
    print("UDP转MQTT:", rc_status[rc],"当前ip为:",UDP_HOST,"端口为:",UDP_PORT)


def on_message(client, userdata, msg):
    """一旦订阅到消息, 回调此方法"""
    # print("主题:" + msg.topic + " 消息:" + str(msg.payload.decode('gb2312')))
    res=str(msg.payload.decode('gb2312'))
    print("接收到MQTT主题:" + msg.topic + " 消息:" +res)

    # 将十六进制消息解码为二进制数据
    binary_data = bytes.fromhex(res)

    print("Udp转Mqtt,ip:", UDP_HOST, "端口:", UDP_PORT)
    data = res
    udp_socket.sendto(binary_data, dest_addr)  # 发送数据

    # udp_socket.sendto(data.encode('gbk'), dest_addr)  #发送数据
    # udp_socket.close()


def mqtt_connect():
    """连接MQTT服务器"""
    # client_id = time.strftime('BayesLift', time.localtime(time.time()))
    mqttClient = mqtt.Client(CLIENT_ID)
    mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
    mqttClient.on_message = on_message  # 返回订阅消息回调函数
    mqttClient.username_pw_set(MQTT_USER, MQTT_PASS)  # mqtt服务器账号密码
    mqttClient.connect(MQTT_HOST, MQTT_PORT, 60)
    mqttClient.loop_start()  # 启用线程连接
    return mqttClient


def on_subscribe():
    """订阅主题：mqtt/demo"""
    mqttClient = mqtt_connect()
    mqttClient.subscribe("bayes/lift", 1)
    while True:
        pass
