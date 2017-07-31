###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

import sys

from twisted.internet import reactor, ssl
from twisted.web.server import Site
from twisted.web.static import File

import txaio

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory, \
    listenWS


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    #import sys

    #from twisted.python import log
    #from twisted.internet import reactor

    #log.startLogging(sys.stdout)

	txaio.start_logging(level='debug')

    #factory = WebSocketServerFactory(u"ws://140.86.39.208:9000")
    
    # SSL Server Context: load server key and certificate
    # We use this for both WS and Web!
	contextFactory = ssl.DefaultOpenSSLContextFactory('ssl_certs/server.key', 'ssl_certs/server.crt')
    
	factory = WebSocketServerFactory(u"wss://140.86.39.208:9000")
    
    #factory.protocol = MyServerProtocol
    
    #factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...
	
	factory.protocol = MyServerProtocol
	listenWS(factory, contextFactory)
	
	webdir = File(".")
	webdir.contentTypes['.crt'] = 'application/x-x509-ca-cert'
	web = Site(webdir)
	
    #reactor.listenTCP(9000, factory)
    
	reactor.listenSSL(8080, web, contextFactory)
    
	reactor.run()

