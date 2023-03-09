import can
import isotp
import logging
import time

from opel_display import OpelDisplayPayload


def my_error_handler(error):
    logging.warning('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))


bus = can.interface.Bus(channel='can0', bustype='socketcan')
addr = isotp.Address(isotp.AddressingMode.Normal_11bits, rxid=0x2c1, txid=0x6c1)

stack = isotp.CanStack(bus, address=addr, error_handler=my_error_handler)

odp = OpelDisplayPayload()
new_payload = odp.build("siema Heniu!")


# stack.send(b'Hello, this is a long payload sent in small chunks')
# stack.send(bytearray(b'@\x00A\x03\x10\x10\x00\x1b\x00[\x00c\x00m\x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00T\x00E\x00s\x00T\x00\x00'))
# stack.send(bytearray(b'\xc0\x007\x03\x10\x1a\x00\x1b\x00[\x00f\x00S\x00_\x00d\x00m\x00F\x00M\x00 \x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00 \x00J\x00E\x00D\x00Y\x00N\x00K\x00A\x00\x00'))
# stack.send(bytearray(b'@\x00A\x03\x10\x16\x00\x1b\x00[\x00c\x00m\x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00J\x00a\x00s\x00i\x00e\x00c\x00z\x00k\x00o\x00!\x00\x00'))
stack.send(new_payload)

while stack.transmitting():
    stack.process()
    time.sleep(stack.sleep_time())

print("Payload transmission done.")

bus.shutdown()
