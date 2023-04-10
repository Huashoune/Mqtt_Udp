import time
from Udp_Mqtt import on_subscribe
from Mqtt_Udp import mqtt_publish
#导入线程模块
import threading

if __name__ == '__main__':
    # 扩展： 获取当前线程
    # print("当前执行的线程为：", threading.current_thread())
    # 创建subscribe的线程
    # target： 线程执行的函数名
    subscribe_thread = threading.Thread(target=on_subscribe)

    # 创建publish的线程
    publish_thread = threading.Thread(target=mqtt_publish)

    # 开启线程
    subscribe_thread.start()
    time.sleep(1)
    publish_thread.start()

