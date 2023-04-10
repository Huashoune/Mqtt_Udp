from paho.mqtt import client as mqtt
import time
import socket

ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip.connect(("8.8.8.8", 80))
ip = (str)(ip.getsockname()[0])  #获取本机ip

UDP_HOST = '0.0.0.0'
UDP_PORT = 8082
MQTT_HOST ='43.143.48.34'
MQTT_PORT = 1883
MQTT_USER = 'eryuan'
MQTT_PASS = 'bayes123'
CLIENT_ID = 'BAYES_MQTTTOUDP'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
bindAddr = (UDP_HOST, UDP_PORT)  # 用于客户端的地址和端口绑定
s.bind(bindAddr)    # 将socket绑定地址和端口,实际使用中只需要绑定端口即可,地址由电脑确定


def on_connect(client, userdata, flags, rc):
    """一旦连接成功, 回调此方法"""
    rc_status = ["连接成功", "协议版本错误", "无效的客户端标识", "服务器无法使用", "用户名或密码错误", "无授权"]
    # time.sleep(1)
    print("MQTT转UDP:", rc_status[rc],"当前ip为:",ip,"端口为:",UDP_PORT)

def mqtt_connect():
    mqttClient = mqtt.Client(CLIENT_ID)
    mqttClient.on_connect = on_connect  # 返回连接状态的回调函数
    mqttClient.username_pw_set(MQTT_USER, MQTT_PASS)  # mqtt服务器账号密码
    mqttClient.connect(MQTT_HOST, MQTT_PORT, 60)
    mqttClient.loop_start()  # 启用线程连接
    return mqttClient


# 发布消息
def mqtt_publish():
    """发布主题为'mqtt/demo',内容为'Demo text',服务质量为1"""
    mqttClient = mqtt_connect()
    while(True):
        data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（服务端）地址,得到服务端发来的数据和地址
        data = data.decode()  # 解码数据
        # print('[Recieved data]:', data, '[Server addr]:', addr)
        print('接收到UDP数据:', data, '来自:', addr)
        mqttClient.publish('bayes/Keeps', data, 1)
        # mqttClient.loop_stop()