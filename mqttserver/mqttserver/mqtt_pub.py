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

class eotumqtt:

    subtopic=None
    pubtopic=None
    pubmsg=None
    userdata="test"
    host="127.0.0.1"
    port=8891

    is_connect=0
    is_response=0
    
    response=None


    def __init__(self,subtopic="#",pubtopic="sendwifi",pubmsg="pubsxxx"):
        # If you want to use a specific client id, use
        # mqttc = mqtt.Client("client-id")
        # but note that the client id must be unique on the broker. Leaving the client
        # id parameter empty will generate a random id for you.
        mqttc = mqtt.Client()
        self.subtopic=subtopic
        self.pubtopic=pubtopic
        self.pubmsg=pubmsg
        mqttc.on_message = self.on_message
        mqttc.on_connect = self.on_connect
        mqttc.on_publish = self.on_publish
        mqttc.on_subscribe = self.on_subscribe
        mqttc.message_callback_add("#", self.on_debug)
        # Uncomment to enable debug messages
        # mqttc.on_log = on_log
        mqttc.connect("localhost", 1883, 60)
        mqttc.loop_start()

        #print("ping\r\n")
        #(rc, mid) = mqttc.publish("wifidog/", "client11", qos=2)

        #infot = mqttc.publish("wifidog/ser_pub/40/req?40", "ver", qos=0)
        #infot.wait_for_publish()

        mqttc.loop_forever()      

    def on_connect(self,mqttc, obj, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.mqttc=mqttc
        self.is_connect=1
        mqttc.subscribe(self.subtopic)
        mqttc.publish(self.pubtopic, payload=self.pubmsg, qos=0, retain=False)

    def on_message(self,mqttc, obj, msg):

        self.is_response=1
        print("sub call back :" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        self.response= "sub call back :" + msg.topic + " " + str(msg.qos) + " " + str(msg.payload)
        # This callback will be called for messages that we receive that do not
        # match any patterns defined in topic specific callbacks, i.e. in this case
        # those messages that do not have topics $SYS/broker/messages/# nor
        # $SYS/broker/bytes/#
        
        self.mqttc.disconnect()
        
    def disconnect(self):
        self.mqttc.disconnect()

    def on_publish(self,mqttc, obj, mid):
        print("on_publish mid=" + str(mid))
        pass


    def on_subscribe(self,mqttc, obj, mid, granted_qos):
        print("Subscribed: mid =" + str(mid) + " qos=" + str(granted_qos))


    def on_log(self,mqttc, obj, level, string):
        print(string)
        
    def on_debug(self,mosq, obj, msg):
        # This callback will only be called for messages with topics that match
        # $SYS/broker/bytes/#
        print(obj)
        print("Recive : topic= " + msg.topic + " qos=" + str(msg.qos) + " payload=" + str(msg.payload))


    
if __name__=="__main__":
    client=eotumqtt("subwifi")
    #mqtt=eotumqtt(userdata="userdata",pubmsg="pubmsgtest")
    while true:
        if client.is_connect==1 and client.is_response==1:
            print "result :\n"
            print client.response