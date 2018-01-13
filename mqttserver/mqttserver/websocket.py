from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import time,json

from mqttserver import eotumqtt


class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        d=json.loads(self.data)
        print(d)
        subtopic="wifidog/cli_pub/%s/#" % d['router']
        pubtopic="wifidog/ser_pub/%s/test" % d['router']
        msg=d['mission']
        newmqtt = eotumqtt( subtopic,pubtopic,msg)
        #newmqtt = eotumqtt( "wifidog/cli_pub/40/#","wifidog/ser_pub/40/test","asdfnihao ---")
        
        senddata=newmqtt.response
        print("get result : [%s]" % senddata)
        self.sendMessage(senddata.decode('utf-8'))
        

    def handleConnected(self):
        print('---------connected')

    def handleClose(self):
        print('---------closed')

server = SimpleWebSocketServer('127.0.0.1', 1889, SimpleEcho)
server.serveforever()