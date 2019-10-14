import threading
import ctypes
import time
import logging


# A "BETTER" thread which support start(timeout=xxx) and terminate()
class BThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        # 'timeout' is not for original thread
        self.timeout = None
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
            kwargs.remove('timeout')

        super(BThread, self).__init__(*args, **kwargs)

        self.setName(self.name + '_GThread_' + time.strftime("%Y%m%d-%H%M%S"))
        self._log = logging.getLogger(self.getName())

    def start(self, timeout=None):
        current_timeout = timeout if timeout else self.timeout
        if current_timeout:
            # create another thread to terminate self if timeout
            threading.Thread(target=self._terminate_thread,
                             args=(self, current_timeout)).start()

        super(BThread, self).start()

    @staticmethod
    def _terminate_thread(thread, timeout):
        time.sleep(timeout)
        if thread.is_alive():
            thread.terminate()

    # ret:
    #   True: success
    #   False: fail
    def terminate(self):
        if self.is_alive():
            self._log.info('terminate thread <%s> tid=%s', self.name, self.ident)

            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident,
                                                             ctypes.py_object(
                                                                 SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, 0)
                self._log.error('FAIL, res=%s', res)
                return False

        return True


########
# test #
########
LOG_FMT = "%(asctime)s [%(levelname)s] " \
          "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)


def infinite_loop():
    while True:
        print('infinite_loop...')
        time.sleep(1)


def test1():
    t1 = BThread(target=infinite_loop)

    t1.start()

    time.sleep(2)

    print('TERMINATE')
    t1.terminate()

    print('JOIN')
    t1.join()


def test2():
    t2 = BThread(target=infinite_loop)
    t2.start(timeout=3)
    t2.join()


if __name__ == '__main__':
    test2()
