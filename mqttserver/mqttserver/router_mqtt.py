#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of waiting for a message to be published.


import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, rc):
    topic="wifidog/ser_pub/40/#"
    print("on_connect create subtopic[%s] " % topic)
    mqttc.subscribe(topic, qos=0)

def on_message(mqttc, obj, msg):
    print("get sub response topic[%s] [%s]" % (str(msg.topic),str(msg.payload)))
    
    topic="wifidog/cli_pub/40/req?40"
    msg="client40 GOT, Success!!!"
    
    print("send back topic[%s] msg[%s]" % (topic,msg))
    mqttc.publish(topic, msg, qos=0)

#def on_publish(mqttc, obj, mid):
#    print("on_publish mid=" + str(mid))
#    pass


#def on_subscribe(mqttc, obj, mid, granted_qos):
#    print("Subscribed: mid =" + str(mid) + " qos=" + str(granted_qos))


#def on_log(mqttc, obj, level, string):
#    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
#mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("localhost", 1883, 60)

mqttc.loop_start()

#print("ping\r\n")
#(rc, mid) = mqttc.publish("wifidog/", "client11", qos=2)

infot = mqttc.publish("wifidog/ser_pub/40/req?40", "ver", qos=0)
infot.wait_for_publish()

mqttc.loop_forever()