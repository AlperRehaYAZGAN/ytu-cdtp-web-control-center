import socket
from multiprocessing import Queue, Process


class UDPCom:
    def __init__(self, client="192.168.1.30", server="192.168.1.29", port=12345, bind=True):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (server, port)
        self.client_addr = (client, port)
        self.queue = Queue(10)

        if bind:
            while True:
                try:
                    self.sock.bind(self.server_addr)
                    print("Ethernet connection established.")
                    break
                except:
                    print("Ethernet connection doesn't exist.")

    def UDP_Send(self, q):
        while True:
            try:
                sendmsg = q.get(timeout=0.0001)
                # print(sendmsg)
                self.sock.sendto(sendmsg, self.client_addr)
            except:
                pass

    def UDP_Receive(self):
        while True:
            recvmsg, gelenadres = self.sock.recvfrom(1024)
            recvmsg = bytearray(recvmsg)
            jd = list(recvmsg)
            # print(jd)
            self.queue.put(recvmsg)


if __name__ == "__main__":
    receive = UDPCom(bind=True)
    t1 = Process(target=receive.UDP_Receive)

    t1.start()
    t1.join()