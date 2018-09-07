from __future__ import print_function

import sys
import os
import threading
from random import randint

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class SendHandler(MessagingHandler):
    def __init__(self, conn_url, address, message_body, priority = 0):
        super(SendHandler, self).__init__()

        self.conn_url = conn_url
        self.address = address
        self.message_body = message_body
        self.priority = priority

    def on_start(self, event):
        conn = event.container.connect(self.conn_url)
        event.container.create_sender(conn, self.address)

    def on_link_opened(self, event):
        print("SEND: Opened sender for target address '{0}'".format
              (event.sender.target.address))

    def on_sendable(self, event):
        message = Message(self.message_body)
        message.priority = self.priority
        event.sender.send(message)

        print("SEND: Sent message '{0}'".format(message.body))

        event.sender.close()
        event.connection.close()

def main():
    threading.Timer(5.0, main).start()

    handler = SendHandler(os.getenv('ACTIVEMQ_ADDRESS'), 'python-queue', 'Open Innovation Labs!', randint(0, 9))
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass