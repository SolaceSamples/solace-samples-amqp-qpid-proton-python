from __future__ import print_function, unicode_literals
import optparse
import proton
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

import logging

# Helper Functions
def get_options():
    #parse cmd arguments
    parser = optparse.OptionParser(usage="usage: %prog [options]",
        description="Consumes messages from a solace Durable Topic Endpoint(DTE)")
    parser.add_option("-u", "--url", action="store", default="amqp://localhost:5672",
        help="Url to connect to amqp broker (default %default)")
    parser.add_option("-t", "--topic", action="store", default="a/topic",
        help="Topic for the DTE (default %default)")
    parser.add_option("-n", "--dte_name", action="store", default="mydte",
        help="DTE name (default %default)")
    parser.add_option("-m", "--messages", type="int", default=100,
        help="number of messages to receive (default %default)")
    
    (options, args) = parser.parse_args()
    return options

class DTEConsumer(MessagingHandler):

    def __init__(self, url, dte_name, address, count):
        super(DTEConsumer, self).__init__()
        self.url = url
        self.topic_address = address
        self.expected = count
        self.received = 0
        self.dte_name = dte_name

    def on_start(self, event):
        conn = event.container.connect(url = self.url)
        event.container.create_receiver(conn, self.topic_address, name=self.dte_name)
    
    def on_message(self, event):
        if self.received < self.expected:
            print(event.message.body)
            self.received += 1
            if self.received == self.expected:
                print('Received all messages')
                event.receiver.close()
                event.connection.close()
    
    def on_transport_error(self, event):
        print("transport failure for borker:", self.url)
        MessagingHandler.on_transport_error(self, event)

proton.log.setLevel(10)
#proton.handlers.log.setLevel(10)

options = get_options()
amqp_address = 'dsub://' + options.topic

try:
    print("waiting to receive", options.messages,"messages")
    Container(DTEConsumer(options.url, options.dte_name, amqp_address, options.messages)).run()
except KeyboardInterrupt: pass
