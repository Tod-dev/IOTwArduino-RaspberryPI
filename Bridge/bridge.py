import serial
import numpy as np

PORT = '/dev/pts/4'

'''
LINUX SETUP TO EMULATE SERIAL PORT:
(terminal 1 ): open ports -> socat -d -d pty,raw,echo=0 pty,raw,echo=0
(terminal 2 ): send package -> echo -n -e \\xff\\x02\\x0A\\x14\\xfe > /dev/pts/3
(optional, test: terminal 3:) read data -> cat < /dev/pts/3
'''


class Bridge:
    def setup(self):
        self.ser = serial.Serial(PORT, 9600, timeout=0)
        # self.ser.open()
        self.inbuffer = []
        self.listOfValues = np.array([], dtype=np.int32)

    def loop(self):
        while True:
            if self.ser.in_waiting > 0:
                # data available in serial port
                # read one single byte
                lastchar = self.ser.read(1)
                print("\nByte received: ", lastchar)
                # rebuild the packet
                if lastchar == b'\xfe':
                    # EOL
                    print("\nValue received")
                    print(self.inbuffer)
                    self.useData()
                    self.inbuffer = []
                else:
                    self.inbuffer.append(lastchar)

    def useData(self):
        # use the packet reaceived
        if len(self.inbuffer) <= 3:
            return False
        # split packet
        if self.inbuffer[0] != b'\xff':
            return False

        numBytes = int.from_bytes(self.inbuffer[1], byteorder='little')
        for i in range(numBytes):
            val = int.from_bytes(self.inbuffer[i + 2], byteorder='little')
            stringValue = "Sensor%d: %d" % (i, val)
            print(stringValue)


print("init")
br = Bridge()
br.setup()
br.loop()
