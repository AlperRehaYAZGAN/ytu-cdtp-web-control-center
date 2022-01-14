import UDP
import Camera
from multiprocessing import Process

#udpsend = UDP.UDPCom(port=12344, bind=False)
#udprec = UDP.UDPCom(bind=True)
cam = Camera.Camera(bind=False)


if __name__ == '__main__':
    t1 = Process(target=cam.SendCamera, daemon=True)
    #t2 = Process(target=udprec.UDP_Receive, daemon=True)
    #t3 = Process(target=udpsend.UDP_Send, args=(udprec.queue,), daemon=True)


    t1.start()
    #t2.start()
    #t3.start()

    t1.join()
    #t2.join()
    #t3.join()
