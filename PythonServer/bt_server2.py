import os

from bluetooth import BluetoothError

import controller
import bluetooth as bt

from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor


class BluetoothServer(object):
    def __init__(self):
        # Arbitrary service UUID to advertise
        self.uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"
        self.car = controller.Car()
        self.client_sock = None
        self.server_sock = None
        self.button = TouchSensor(INPUT_1)
        self.counter = 0
        self.start()

    def start(self):
        # Make device visible
        print("WELCOME")
        os.system("hciconfig hci0 piscan")

        self.server_sock = bt.BluetoothSocket(bt.RFCOMM)  # Create a new server socket using RFCOMM protocol

        port = 1
        self.server_sock.bind(("", port))  # Bind to port 1 - else phone won't connect
        self.server_sock.listen(1)  # Start listening

        # Get the port the server socket is listening
        port = self.server_sock.getsockname()[1]

        # Start advertising the service
        bt.advertise_service(self.server_sock, "RaspiBtSrv",
                             service_id=self.uuid,
                             service_classes=[self.uuid, bt.SERIAL_PORT_CLASS],
                             profiles=[bt.SERIAL_PORT_PROFILE])

        # Outer loop: listen for connections from client
        print("Waiting for connection on RFCOMM channel %d" % port)

        try:
            # This will block until we get a new connection
            self.client_sock, client_info = self.server_sock.accept()
            print("Accepted connection from " + str(client_info))

            # Track strings delimited by '.'
            msg = ''

            while True:
                data = self.client_sock.recv(1).decode('utf-8')
                if self.client_sock is None:
                    self.restart()
                else:
                    if data == '.' and len(msg) > 0:
                        self.handle_message(msg)
                        msg = ''
                    else:
                        msg += data

                if self.button.is_pressed:  # Stops the server and motors
                    self.stop()

        except KeyboardInterrupt:
            if self.client_sock is not None:
                self.client_sock.close()

            self.server_sock.close()
            print("Server going down")
            exit(0)

        except BluetoothError:
            self.restart()

    def handle_message(self, msg):
        print(str(self.counter), ":", msg)
        self.counter = self.counter + 1
        self.car.take_action(msg)

    def restart(self):
        print("\nClient disconnected")
        print("Restarting...\n")
        self.server_sock.close()
        self.start()

    def stop(self):
        print("\nStopping!")
        self.car.stop()
        self.server_sock.close()


if __name__ == '__main__':
    server = BluetoothServer()
