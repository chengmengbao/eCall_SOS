# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019/9/23 20:19
# @Author  : Paul Chan
# @Email   : paul_chengmengbao@163.com
# @File    : mqtt_client.py
# @Software: PyCharm

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
# from eCall_SOS.settings import MQTTHOST, MQTTPORT

# mqtt broken ip
mqtthost = "172.16.48.42"
# mqtt broken port
mqttport = 1883


# 实例化一个mqtt客户端
mqttClient = mqtt.Client()


# 连接MQTT Broken成功后-回调该函数
def on_connect(client, userdata, flags, rc):
    print("Connection returned " + str(rc))


# 消息收到-回调函数
def on_message(client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))


# 将一条消息发布给代理，然后彻底断开连接
def publish_single(topic_str, msg_str, qos, hostname=mqtthost, port=mqttport):
    publish.single(topic_str, msg_str, qos=qos, hostname=hostname, port=port)


# 连接MQTT服务器
def mqtt_connect():
    mqttClient.connect(mqtthost, mqttport, 60)


# publish 消息
# client.publish('application/gateway/b827ebffffcb7850/reboot', payload='04', qos=0)
def publish_msg(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)
    # mqttClient.loop_start()


# subscribe 消息
def on_subscribe():
    mqttClient.subscribe("chat", 1)
    mqttClient.on_message = on_message  # 消息到来处理函数

# 测试代码
if __name__ == '__main__':
    import time
    client_id = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    client = mqtt.Client(client_id)    # ClientId不能重复，所以使用当前时间
    # client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtthost, mqttport, 60)
    client.publish("test", "你好 MQTT", qos=0, retain=False)  # 发布消息
    # publish.single("test", "你好 MQTT", qos = 1,hostname=HOST,port=PORT, client_id=client_id,auth = {'username':"admin", 'password':"123456"})

