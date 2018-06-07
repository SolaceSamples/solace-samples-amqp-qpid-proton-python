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

# helper function
def get_options():
    parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
    parser.add_option("-u", "--url", default="localhost:5672",
                  help="amqp message broker host url (default %default)")
    parser.add_option("-a", "--address", default="examples",
                  help="node address to which messages are sent (default %default)")
    parser.add_option("-m", "--messages", type="int", default=100,
                  help="number of messages to send (default %default)")
    parser.add_option("-o", "--username", default=None,
                  help="username for authentication (default %default)")
    parser.add_option("-p", "--password", default=None,
                  help="password for authentication (default %default)")
    parser.add_option("-q", "--qos", default="non-persistent",
                  help="Selects the message QoS for published messages. Valid values are [persistent or 2] for persistent messages. Valid values are [non-persistent or 1] for non-persistent messages. (default %default)" )
    opts, args = parser.parse_args()
    return opts



"""
Proton event handler class
Demonstrates how to create an amqp connection and a sender to publish messages.
"""
class Send(MessagingHandler):
    def __init__(self, url, address, messages, username, password, QoS=1):
        super(Send, self).__init__()
    
        # amqp broker host url
        self.url = url

        # target amqp node address
        self.address = address

        # authentication credentials
        self.username = username
        self.password = password

        # the message durability flag must be set to True for persistent messages
        self.message_durability = True if QoS==2 else False

        # messaging counters        
        self.sent = 0
        self.confirmed = 0
        self.total = messages

    def on_start(self, event):
        # select connection authenticate
        if self.username:
            # creates and establishes an amqp connection with the user credentials
            conn = event.container.connect(url=self.url, 
                                           user=self.username, 
                                           password = self.password, 
                                           allow_insecure_mechs=True)
        else:
            # creates and establishes an amqp connection with anonymous credentials
            conn = event.container.connect(url=self.url)
        if conn:
            # attaches sender link to transmit messages
            event.container.create_sender(conn, target=self.address)

    def on_sendable(self, event):
        while event.sender.credit and self.sent < self.total:
            # creates message to send
            msg = Message(id=(self.sent+1), 
                          body='sequence'+str(self.sent+1), 
                          durable=self.message_durability)
            # sends message
            event.sender.send(msg)
            self.sent += 1

    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            print("all messages confirmed")
            event.connection.close()

    def on_rejected(self, event):
        self.confirmed += 1
        print("Broker", self.url, "Reject message:", event.delivery.tag)
        if self.confirmed == self.total:
            event.connection.close()

    # catches event for socket and authentication failures
    def on_transport_error(self, event):
        print("Transport error:", event.transport.condition)
        MessagingHandler.on_transport_error(self, event)

    def on_disconnected(self, event):
        if event.transport and event.transport.condition :
            print('disconnected with error : ', event.transport.condition)
            event.connection.close()

        self.sent = self.confirmed

# get application options
opts = get_options()

# determine Quality of Service for sending messages
if str(opts.qos) == "non-persistent" or  opts.qos==1:
    QoS=1 # non-persistent
elif str(opts.qos) == "persistent" or  opts.qos==2:
    QoS=2 # persistent
else:
    # TODO add QOS for direct (0)
    # default to non-persistent
    QoS=1


"""
The amqp address can be a topic or a queue.
Do not use a prefix or use 'queue://' in the amqp address for 
the amqp sender link target address to indicate which queue 
messages are sent to.
"""

try:
    # start proton event reactor
    Container(Send(opts.url, opts.address, opts.messages, opts.username, opts.password, QoS)).run()
except KeyboardInterrupt: pass
