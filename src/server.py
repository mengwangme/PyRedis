from gevent.server import StreamServer
from src.command_parser import parse_command
import socket
from src.command_handler import handle_command, resp_error


def read_from_client(s, address):
    """
    this is the function that handles incoming commands, and sends them off to be parsed and then handled
    finally, it will print the output back to the socket
    :param s:
    :param address:
    :return:
    """
    while True:
        try:
            data = s.recvfrom(65536)
            if data is not None and data[0] is not None:
                try:
                    command_arr = parse_command(data[0].decode('utf-8'), 0)
                    response = handle_command(command_arr)
                    s.send(bytes(response, 'utf-8'))
                except socket.error:
                    raise
                except Exception as e:
                    s.send(bytes(resp_error("An unspecified error occurred. {0}".format(str(e))), 'utf-8'))
        except socket.error:
            print(socket.error)
            break
    s.close()


def bind_server(ip, port, spawn_limit):
    """
    when called, this will bind a tcp server server using gevent for concurrency
    :return:
    """
    try:
        server = StreamServer((ip, port), read_from_client, spawn=spawn_limit)  # creates a new server
        server.start()
        server.serve_forever()
    except Exception as e:
        print(str(e))
        server.close() if server is not None and server.started else None