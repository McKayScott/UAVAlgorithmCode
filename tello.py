import socket
import threading
import time
#from stats import Stats
import sys
from datetime import datetime
import time
import argparse

class Tello(object):
    def __init__(self):
        """
        Constructor.
        """
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))

        # thread for receiving cmd ack
        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.tello_ip = '192.168.10.1'
        self.tello_port = 8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.log = []

        self.MAX_TIME_OUT = 15.0

    def send_command(self, command):
        """
        Send a command to the ip address. Will be blocked until
        the last command receives an 'OK'.
        If the command fails (either b/c time out or error),
        will try to resend the command
        :param command: (str) the command to send
        :param ip: (str) the ip of Tello
        :return: The latest command response
        """
        #self.log.append(Stats(command, len(self.log)))

        self.socket.sendto(command.encode('utf-8'), self.tello_address)
        print(f'sending command: {command} to {self.tello_ip}')

        start = time.time()
        while self.log == []:
            now = time.time()
            diff = now - start
            if diff > self.MAX_TIME_OUT:
                print(f'Max timeout exceeded... command {command}')
                return
        self.log.pop()
        print(f'Done!!! sent command: {command} to {self.tello_ip}')

    def _receive_thread(self):
        """
        Listen to responses from the Tello.
        Runs as a thread, sets self.response to whatever the Tello last returned.
        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(1024)
                print(f'from {ip}: {self.response}')

                self.log.append(1)#.add_response(self.response)
            except Exception as exc:
                print(f'Caught exception socket.error : {exc}')

    def on_close(self):
        """
        On close.
        :returns: None.
        """
        pass

    def get_log(self):
        """
        Gets the logs.
        :returns: Logs.
        """
        return self.log

def parse_args(args):
    """
    Parses arguments.
    :param args: Arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser('Tello Flight Commander', 
        epilog='One-Off Coder https://www.oneoffcoder.com')

    parser.add_argument('-f', '--file', help='command file', required=True)
    return parser.parse_args(args)


def start(file_name):
    """
    Starts sending commands to Tello.
    :param file_name: File name where commands are located.
    :return: None.
    """
    start_time = str(datetime.now())

    with open(file_name, 'r') as f:
        commands = f.readlines()

    tello = Tello()
    for command in commands:
        if command != '' and command != '\n':
            command = command.rstrip()

            if command.find('delay') != -1:
                sec = float(command.partition('delay')[2])
                print(f'delay {sec}')
                time.sleep(sec)
                pass
            else:
                tello.send_command(command)

    # with open(f'log/{start_time}.txt', 'w') as out:
    #     log = tello.get_log()

        # for stat in log:
        #     stat.print_stats()
        #     s = stat.return_stats()
        #     out.write(s)


if __name__ == '__main__':
    #args = parse_args(sys.argv[1:])
    file_name = 'tello_commands.txt'

    start(file_name)