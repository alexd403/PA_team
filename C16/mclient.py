import socket
import select
import sys

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 65535
    BUFFER_SIZE = 1024
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.connect((host, port))
        connected = True
        while connected:
            sockets_list = [sys.stdin, server]
            read_sockets, _, _ = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == server:
                    message = socks.recv(BUFFER_SIZE)
                    if message:
                        print(message.decode('utf-8'))
                    else:
                        print("Conexión cerrada")
                        connected = False
                        break
                else:
                    message = sys.stdin.readline()
                    server.send(bytes(message, 'utf-8'))
                    sys.stdout.write("<Tú>")
                    sys.stdout.write(message)
                    sys.stdout.flush()
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        server.close()