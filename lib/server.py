__author__ = "Jannis Dickel"

import socket


class Server:
    html_str = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>LED-Lamp</title>
                </head>

                <body>
                    <h1>Pico W HTTP Server</h1>
                    <p>Hello, World!</p>
                    <p>%s</p>
                </body>
                </html>
                """

    def __init__(self, port: int, host_ip="0.0.0.0") -> None:
        self.address = socket.getaddrinfo(host_ip, port)[0][-1]
        self.socket = socket.socket()
        self.socket.setblocking(False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.address)
        self.socket.listen(1)
        print(f"Listening on {self.address}")

    # def start(self) -> None:
    #     self.socket.listen(1)
    #     print(f"Listening on {self.address}")
    #
    # def _accept(self):
    #     client, address = self.socket.accept()
    #     print(f"client connected from {address}")
    #     return client

    def run(self) -> (int, int, int):
        while True:
            print("waiting")
            try:
                # client = self._accept()
                client, addr = self.socket.accept()
                print("Client connected from {addr}")
                request = client.recv(1024)
                print(f"Request: {request}")
                request = str(request)
                pos: int = request.find("?color=")
                # if pos != 5:
                #     raise OSError("Got a wrong path variable")
                #
                # color = tuple(map(int, request.split(" ")[1][8:].split(";")))
                # print(color)

                response = self.html_str % "Changed color"
                client.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
                client.send(response)
                client.close()

            except OSError:
                client.close()
                print("Connection closed")