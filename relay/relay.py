import threading, queue
import time
import logging

from relay.moxa_1214_api import MoxaRelay

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

class RelayMonitor(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self._ip = ip
        self._relay = MoxaRelay(ip)
        self._queue = queue.Queue()
        self._interval = 1
        self._stopped = threading.Event()
        self._alive = False

    def stop(self):
        self._stopped.set()



    def run(self):

        self._alive = True
        LOG.debug(f'Start monitoring for relay [{self._ip}]')
        print(f'Start monitoring for relay [{self._ip}]')
        n = 0
        start_time = time.time()
        while 1:
            self._relay.pull_status()
            self._log_status()
            self._update_status()
            n+= 1
            dt = n*self._interval + start_time - time.time()
            dt = 0 if dt < 0 else dt
            if self._stopped.wait(dt):
                break
        self._alive = False
        print('RUN EXIT')

    @property
    def alive(self):
        return self._alive

    def _update_status(self):
        update = 0
        while True:
            try:
                data = self._queue.get_nowait()
            except queue.Empty:
                break

            if data:
                pin,v = data
                update = 1
                self._relay.set_pin(pin, v)

        if update:
            LOG.debug('UPDATE') #TODO
            self._relay.push_status()  
        
        return update        #TODO maybe return error                 

    def _log_status(self):
        status = ''
        for i in range(6):
            status += str(self._relay.get_pin(i))
        print(f'Realy {self._ip} status {status}')

    def get_state(self, pin):
        return self._relay.get_pin(pin)

    def set_state(self, pin, v):
        self._queue.put((pin, v))


            
if __name__ == "__main__":
    format = "%(asctime)s <%(thread)s> [%(levelname)5s] "\
    "%(module)12s:%(funcName)17s:: %(message)s"
    logging.basicConfig(format=format)
    r = RelayMonitor("192.168.4.116")
    r.start()

    for pin in range(5):
        LOG.debug(f'pin:{pin} state:{r.get_state(pin)}')
    time.sleep(2.46)
    r.set_state(0, 1)
    LOG.debug(f'SET PIN')
    for pin in range(5):
        LOG.debug(f'pin:{pin} state:{r.get_state(pin)}')
    time.sleep(1.0)
    for pin in range(5):
        LOG.debug(f'pin:{pin} state:{r.get_state(pin)}')
    time.sleep(2.0)
    r.stop()
    print(r.is_alive())
    r.join()
    print(r.is_alive())
    r.start()


