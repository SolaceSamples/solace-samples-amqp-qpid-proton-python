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
    parser.add_option("-o", "--username", default=None,
        help="username for authentication (default %default)")
    parser.add_option("-p", "--password", default=None,
        help="password for authentication (default %default)")

    (options, args) = parser.parse_args()
    return options


"""
DTEConsumer class is a proton event handler
This class establishes a connection and revceiver link
attached to solace Durable Topic Endpoint
"""
class DTEConsumer(MessagingHandler):

    def __init__(self, url, dte_name, address, count, username, password):
        super(DTEConsumer, self).__init__()
        
        # amqp broker host url
        self.url = url
        
        # amqp node address representing a topic
        self.topic_address = address
        
        # name of the Durable Topic endpoint
        self.dte_name = dte_name
        
        # authentication credentials
        self.username = username
        self.password = password
        
        # messaging counters
        self.expected = count
        self.received = 0

    def on_start(self, event):
        # select anonymous or plain authentication
        if self.username:
            # establish amqp connection to solace pubsub+ broker with plain authentication
            conn = event.container.connect(url=self.url,
                                           user=self.username,
                                           password=self.password,
                                           allow_insecure_mechs=True)
        else:
            # establish amqp connection to solace pubsub+ broker with anonymous authentication
            conn = event.container.connect(url=self.url)
        # attach amqp receiver link to a solace Durable Topic Endpoint
        # name=self.dte_name sets the Link name to the subscription name
        # self.topic_address sets the topic and indicates the durability of the topic endpoint 
        if conn:
            event.container.create_receiver(conn, source=self.topic_address, name=self.dte_name)
    
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


# get application options
options = get_options()
"""
To consume from a DTE over amqp a subscription name
and a topic are required.

To achieve this the following must be done:

1) Set the amqp address to 'dsub://<topic_name>'. 
   The prefix 'dsub://' indicates the topic endpoint to bind to is a durable topic endpoint.

2) Set the amqp Link name to the subscription name.
"""
# add the 'dsub://' prefix to the given topic 
amqp_address = 'dsub://' + options.topic

try:
    print("waiting to receive", options.messages,"messages")
    # start the proton Container event loop with the DTEConsumer event handler
    Container(DTEConsumer(options.url, 
                          options.dte_name, 
                          amqp_address, 
                          options.messages, 
                          options.username, 
                          options.password)
    ).run()
except KeyboardInterrupt: pass
