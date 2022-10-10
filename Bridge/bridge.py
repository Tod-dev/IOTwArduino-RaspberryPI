import serial
import numpy as np

PORT = 'COM5'


class Bridge():
    def setup(self):
        self.ser = serial.Serial(PORT, 9600, timeout=0)
        # self.ser.open()
        self.inbuffer = []
        self.listOfValues = np.array([], dtype=np.int32)

    def loop(self):
        while (True):
            if self.ser.in_waiting >= 0:
                # data available in serial port
                # read one single byte
                lastchar = self.ser.read(1)

                # rebuild the packet
                if lastchar == b'\xfe':
                    # EOL
                    print("\nValue received")
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
            val = int.from_bytes(self.inbuffer[i+2], byteorder='little')
            stringValue = "Senso %d: %d" % (i, val)
            print(stringValue)


if __name__ == 'main':
    br = Bridge()
    br.setup()
    br.loop()
