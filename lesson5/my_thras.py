from threading import Thread
import time

class MyThread(Thread):

    def __init__(self, is_daemon):
        super().__init__(daemon=is_daemon)
        self.result = None


    def run(self):
        time.sleep(3)
        self.result = 3



a = MyThread(False)
a.start()
a.join()
print(a.result)

