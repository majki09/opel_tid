import isotp
import logging
import time
import threading

import can
# from opel_display import OpelDisplayPayload

# from can.interfaces.socketcan import SocketcanBus
# from can.interfaces.kvaser import KvaserBus


class ThreadedApp:
    def __init__(self):
        self.exit_requested = False
        # self.bus = KvaserBus(channel=0, can_filters=[{"can_id": 0x6c1, "can_mask": 0x0}], bitrate=94117)
        self.bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        addr = isotp.Address(isotp.AddressingMode.Normal_11bits, rxid=0x6c1, txid=0x2c1)
        self.stack = isotp.CanStack(self.bus, address=addr, error_handler=self.my_error_handler)

    def start(self):
        self.exit_requested = False
        self.thread = threading.Thread(target=self.thread_task)
        self.thread.start()

    def stop(self):
        self.exit_requested = True
        if self.thread.is_alive():
            self.thread.join()

    def my_error_handler(self, error):
        logging.warning('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))

    def thread_task(self):
        while self.exit_requested == False:
            self.stack.process()  # Non-blocking
            time.sleep(self.stack.sleep_time())  # Variable sleep time based on state machine state

    def shutdown(self):
        self.stop()
        self.bus.shutdown()


if __name__ == '__main__':
    log_filename = ".\\log.log"
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s.%(msecs)03d \t %(message)s",
                        datefmt='%H:%M:%S',
                        filename=log_filename,
                        filemode='w')
    # SERIALS log file
    log_handler_serials = logging.FileHandler(filename=".\\payloads.log",
                                              mode='w')
    formatter_serials = logging.Formatter("%(asctime)s.%(msecs)03d \t %(message)s")
    formatter_serials.datefmt = "%H:%M:%S"
    log_handler_serials.setFormatter(formatter_serials)
    log_handler_serials.setLevel(logging.DEBUG)

    log_payloads = logging.getLogger("PAYLOADS")
    logging.getLogger("PAYLOADS").addHandler(log_handler_serials)
    logging.info("START")

    app = ThreadedApp()
    app.start()

    print('Waiting for payload - maximum 5 sec')
    t1 = time.time()
    while time.time() - t1 < 30:
        if app.stack.available():
            payload = app.stack.recv()
            print("Received payload : %s" % payload)
            log_payloads.info(payload)
            # print(f"TEXT:", payload[42:-2].decode("utf_16_be"))
            # odp = OpelDisplayPayload(payload)
            # break
        time.sleep(0.2)

    print("Exiting")
    app.shutdown()
