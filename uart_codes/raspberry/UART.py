import collections
import serial
from crccheck.crc import Crc32Mpeg2
from multiprocessing import Queue, Process
import time


class SerialCom:
    def __init__(self, port="/dev/ttyTHS1", baud=115200, msgsize=40, bufsize=400):
        while True:
            try:
                self.s = serial.Serial(port, baud)
                break
            except:
                print("port yok!")

        self.msgsize = msgsize
        self.readsize = msgsize * 2
        self.cBuffer = collections.deque(maxlen=bufsize)
        self.q = Queue(10)
        self.sendmsg = []
        self.come = [0] * 10

        self.header1 = 0b0100
        self.header2 = 0b0101

    def isEmpty(self):
        if len(self.cBuffer) == 0:
            return True
        return False

    def findHeader(self):
        for i in range(len(self.cBuffer)):
            if self.isEmpty():
                return None

            elif self.cBuffer.popleft() == self.header1:
                if self.isEmpty():
                    return None

                elif self.cBuffer.popleft() == self.header2:
                    return True

            else:
                pass

        return False

    def readCBuffer(self):
        if self.findHeader():
            packet = [self.header1, self.header2] + [0] * (self.msgsize - 2)
            packet = bytearray(packet)

            for i in range(2, self.msgsize):
                try:
                    packet[i] = self.cBuffer.popleft()
                except:
                    pass

            crc = Crc32Mpeg2.calc(packet)

            if crc == 0x00000000:
                packet = packet[2:-4]
                return packet

            else:
                return None

        else:
            pass

    def readSerialPort(self):
        while True:
            if self.s.inWaiting() >= self.readsize:
                coming = self.s.readline(self.readsize)
                for i in range(self.readsize):
                    try:
                        self.cBuffer.append(coming[i])
                    except:
                        pass

                comingmsg = self.readCBuffer()

                try:
                    self.q.put(comingmsg, timeout=0.0001)
                except:
                    pass

                if self.s.inWaiting() >= 4094:
                    self.s.flushInput()

            else:
                pass

    def writeSerialPort(self, q):
        while True:
            try:
                self.sendmsg = q.get(timeout=0.001)
            except:
                pass

            if len(self.sendmsg) > 0:
                self.sendmsg.insert(0, self.header1)
                self.sendmsg.insert(1, self.header2)

                calcCrc = Crc32Mpeg2.calc(self.sendmsg)

                first = (calcCrc >> 24) & 0xFF
                second = (calcCrc >> 16) & 0xFF
                third = (calcCrc >> 8) & 0xFF
                fourth = (calcCrc & 0xFF)

                self.sendmsg.append(fourth)
                self.sendmsg.append(third)
                self.sendmsg.append(second)
                self.sendmsg.append(first)
                time.sleep(.001)
                self.s.write(self.sendmsg)
                print(list(self.sendmsg))
                self.sendmsg = []


if __name__ == "__main__":
    port = SerialCom()

    t1 = Process(target=port.readSerialPort)
    t2 = Process(target=port.writeSerialPort, args=(port.q,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()