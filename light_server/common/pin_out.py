"""GPIO wrapper
"""
import time
import logging

LOG = logging.getLogger(__name__)

class PinOut:
    """gpio pin
    """
    def __init__(self, pin_num):
        self._num = pin_num
        try:
            with open('/sys/class/gpio/export', 'w', encoding="utf8") as f:
                f.write(f'{self._num}')
            with open(f'/sys/class/gpio/gpio{self._num}/direction', 'w', encoding="utf8") as file:
                file.write('out')
            self._file = open(f'/sys/class/gpio/gpio{self._num}/value', 'w', encoding="utf8")
        except Exception as exc:
            LOG.warning("Can't open gpio:%s", exc)
            self._file = None
        self.set(1)

    def set(self, val):
        """set pin value

        Args:
            val (int): 0/1
        """
        if self._file:
            self._file.write(f'{val}')
            self._file.flush()
        else:
            LOG.warning("No gpio:%s", self._num)

if __name__ == '__main__':
    pin = PinOut(14)
    DELAY = 1
    while 1:
        pin.set(0)
        time.sleep(DELAY)
        pin.set(1)
        time.sleep(DELAY)
