#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

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
    parser.add_option("-o", "--username", default=None,
        help="username for authentication (default %default)")
    parser.add_option("-p", "--password", default=None,
        help="password for authentication (default %default)")

    (options, args) = parser.parse_args()
    return options

"""
Proton event Handler class
Establishes an amqp connection and creates an amqp sender link to transmit messages
"""
class MessageProducer(MessagingHandler):

    def __init__(self, url, address, count, username, password):
        super(MessageProducer, self).__init__()

        # the solace message broker amqp url
        self.url = url 
        # the prefix amqp address for a solace topic
        self.topic_address = address 
        
        # authentication credentials
        self.username = username
        self.password = password

        self.total = count
        self.sent = 0
        self.confirmed = 0

    def on_start(self, event):
        # select authentication from SASL PLAIN or SASL ANONYMOUS
        if self.username:
            # creates and establishes amqp connection using PLAIN authentication
            conn = event.container.connect(url=self.url, 
                                           user=self.username, 
                                           password=self.password, 
                                           allow_insecure_mechs=True)
        else:
            # creates and establishes amqp connection using ANONYMOUS authentication
            conn = event.container.connect(url=self.url)
        if conn:
            # creates sender link to transfer message to the broker
            event.container.create_sender(conn, target=self.topic_address)
   
    def on_sendable(self, event):
        while event.sender.credit and self.sent < self.total:
            # the durable property on the message sends the message as a persistent message
            event.sender.send(Message(body="hello "+str(self.sent), durable=True))
            self.sent += 1
    
    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            print('confirmed all messages')
            event.connection.close()

    def on_rejected(self, event):
        self.confirmed += 1
        print("Broker", self.url, "Reject message:", event.delivery.tag, "Remote disposition:", event.delivery.remote.condition)
        if self.confirmed == self.total:
            event.connection.close()
    # receives socket or authentication failures
    def on_transport_error(self, event):
        print("Transport failure for amqp broker:", self.url, "Error:", event.transport.condition)
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
    # starts the proton container event loop with the MessageProducer event handler
    Container(MessageProducer(options.url, amqp_address, options.messages, options.username, options.password)).run()
except KeyboardInterrupt: pass

