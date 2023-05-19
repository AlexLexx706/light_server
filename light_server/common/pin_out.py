"""GPIO wrapper
"""
import time
import logging

LOG = logging.getLogger(__name__)


class PinOut:
    """gpio pin
    """
    VALUE_MAP = {0: 'off', 1: 'on'}

    def __init__(self, pin_num, name):
        self._num = pin_num
        self._val = 0
        self._name = name
        try:
            with open('/sys/class/gpio/export', 'w', encoding="utf8") as f:
                f.write(f'{self._num}')
            with open(f'/sys/class/gpio/gpio{self._num}/direction', 'w', encoding="utf8") as file:
                file.write('out')
            self._file = open(
                f'/sys/class/gpio/gpio{self._num}/value', 'w', encoding="utf8")
        except Exception as exc:
            LOG.warning("Can't open gpio:%s", exc)
            self._file = None
        self.set(1)

    @property
    def value(self):
        return self.VALUE_MAP[self._val]

    @property
    def name(self):
        return self._name

    def set(self, val):
        """set pin value

        Args:
            val (int): 0/1
        """
        LOG.info('set:%s', val)

        if self._file:
            self._file.write(f'{val}')
            self._file.flush()
        else:
            LOG.warning("No gpio:%s", self._num)
        self._val = val


if __name__ == '__main__':
    pin = PinOut(14)
    DELAY = 1
    while 1:
        pin.set(0)
        time.sleep(DELAY)
        pin.set(1)
        time.sleep(DELAY)
