import asyncio
from typing import Optional

import h11
import logging

logging.basicConfig(level=logging.DEBUG)


class HTTPProtocol:
    def __init__(self):
        self.connection = h11.Connection(h11.SERVER)

    def eof_received(self):
        return

    def connection_lost(self, exc: Optional[Exception]) -> None:
        return

    def pause_writing(self) -> None:
        pass

    def resume_writing(self) -> None:
        pass

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):

        self.connection.receive_data(data)

        while True:
            event = self.connection.next_event()
            if isinstance(event, h11.Request):
                self.send_response(event)
            elif (
                    isinstance(event, h11.ConnectionClosed)
                    or event is h11.NEED_DATA or event is h11.PAUSED
            ):
                break

        if self.connection.our_state is h11.MUST_CLOSE:
            self.transport.close()

    def send_response(self, event):
        body = b"%s %s" % (event.method.upper(), event.target)
        headers = [
            ('content-type', 'text/plain'),
            ('content-length', str(len(body))),
        ]
        response = h11.Response(status_code=200, headers=headers)
        self.send(response)
        self.send(h11.Data(data=body))
        self.send(h11.EndOfMessage())
        asyncio.get_event_loop().call_later(5, self.call_to_close)

    def send(self, event):
        data = self.connection.send(event)
        self.transport.write(data)

    def call_to_close(self):
        self.transport.close()


async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(HTTPProtocol, host, port)
    await server.serve_forever()


asyncio.run(main('0.0.0.0', 5000))
