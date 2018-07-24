# !/usr/bin/env python
import sys, os
from src.daemon import Daemon
from src.server import bind_server
TCP_IP = '0.0.0.0'
TCP_PORT = 6379
BUFFER_SIZE = 65536
SPAWN = 10000
PID_FILE = '/tmp/pyredis.pid'

script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)


class PyRedisDaemon(Daemon):
        def run(self):
           bind_server(TCP_IP, TCP_PORT, SPAWN)


def main():
    if len(sys.argv) == 3:
        if sys.argv[1] == 'start' and sys.argv[2] == 'debug':
            # short circuit for debug mode, run with pyredis start debug and it will not launch as a daemon nor redirect output
            bind_server(TCP_IP, TCP_PORT, SPAWN)
        else:
            print("Unknown command")
            sys.exit(2)

    daemon = PyRedisDaemon(PID_FILE)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print("Starting pyredis...")
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print("Stopping pyredis...")
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print("Restarting pyredis...")
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: {0} start|stop|restart".format(sys.argv[0]))
        sys.exit(2)


if __name__ == "__main__":
    main()


