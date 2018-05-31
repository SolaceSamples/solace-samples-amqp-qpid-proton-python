from __future__ import print_function, unicode_literals
import optparse
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

# Helper Functions
def get_options():
    #parse cmd arguments
    parser = optparse.OptionParser(usage="usage: %prog [options]",
        description="Sends messages to a topic on the amqp broker")
    parser.add_option("-u", "--url", action="store", default="amqp://localhost:5672",
        help="Url to connect to amqp broker (default %default)")
    parser.add_option("-t", "--topic", action="store", default="a/topic",
        help="Topic to send message (default %default)")
    parser.add_option("-m", "--messages", type="int", default=100,
        help="number of messages to receive (default %default)")
    
    (options, args) = parser.parse_args()
    return options

#Proton event Handler class

class MessageProducer(MessagingHandler):

    def __init__(self, url, address, count):
        super(MessageProducer, self).__init__()

        # the solace message broker amqp url
        self.url = url 
        # the prefix amqp address for a solace topic
        self.topic_address = address 
        
        self.total = count
        self.sent = 0
        self.confirmed = 0

    def on_start(self, event):
        # creates and establishes amqp connection
        conn = event.container.connect(url = self.url)
        # creates sender link to transfer message to the broker
        event.container.create_sender(conn, self.topic_address)
   
    def on_link_opened(self, event):
        print("sender link established", event.sender, "recvr", event.receiver)
 
    def on_sendable(self, event):
        while event.sender.credit and self.sent < self.total:
            event.sender.send(Message(body="hello "+str(self.sent)))
            self.sent += 1
    
    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            print('confirmed all messages')
            event.connection.close()

    def on_transport_error(self, event):
        print('Tranpsport failure for amqp broker:', self.url)
        MessagingHandler.on_transport_error(self, event)

# get program options
options = get_options()
"""
The amqp address can be a topic or a queue.
Use 'topic://' prefix in the amqp address for the amqp sender
target address to indicate which topic message are sent to.
"""
amqp_address = 'topic://' + options.topic

try:
    Container(MessageProducer(options.url, amqp_address, options.messages)).run()
except KeyboardInterrupt: pass

