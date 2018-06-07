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

from __future__ import print_function
import optparse
from proton.handlers import MessagingHandler
from proton.reactor import Container

# helper function

def get_options():
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("-u", "--url", default="localhost:5672",
                  help="amqp message broker host url (default %default)")
    parser.add_option("-a", "--address", default="examples",
                  help="node address from which messages are received (default %default)")
    parser.add_option("-m", "--messages", type="int", default=100,
                  help="number of messages to receive; 0 receives indefinitely (default %default)")
    parser.add_option("-o", "--username", default=None,
                  help="username for authentication (default %default)")
    parser.add_option("-p", "--password", default=None,
                  help="password for authentication (default %default)")

    opts, args = parser.parse_args()

    return opts

"""
Proton event handler class
Creates an amqp connection using ANONYMOUS or PLAIN authentication.
Then attaches a receiver link to conusme messages from the broker.
"""
class Recv(MessagingHandler):
    def __init__(self, url, address, count, username, password):
        super(Recv, self).__init__()

        # amqp broker host url
        self.url = url

        # amqp node address
        self.address = address

        # authentication credentials
        self.username = username
        self.password = password
        
        # messaging counters
        self.expected = count
        self.received = 0

    def on_start(self, event):
        # select authentication options for connection
        if self.username:
            # basic username and password authentication
            conn = event.container.connect(url=self.url, 
                                           user=self.username, 
                                           password=self.password, 
                                           allow_insecure_mechs=True)
        else:
            # Anonymous authentication
            conn = event.container.connect(url=self.url)
        # create receiver link to consume messages
        if conn:
            event.container.create_receiver(conn, source=self.address)

    def on_message(self, event):
        if event.message.id and event.message.id < self.received:
            # ignore duplicate message
            return
        if self.expected == 0 or self.received < self.expected:
            print(event.message.body)
            self.received += 1
            if self.received == self.expected:
                print('received all', self.expected, 'messages')
                event.receiver.close()
                event.connection.close()

    # the on_transport_error event catches socket and authentication failures
    def on_transport_error(self, event):
        print("Transport error:", event.transport.condition)
        MessagingHandler.on_transport_error(self, event)

    def on_disconnected(self, event):
        print("Disconnected")

# parse arguments and get options
opts = get_options()

"""
The amqp address can be a topic or a queue.
Do not use a prefix or use 'queue://' in the amqp address for
the amqp receiver source address to receiver messages from a queue.
"""

try:
    Container(Recv(opts.url, opts.address, opts.messages, opts.username, opts.password)).run()
except KeyboardInterrupt: pass



