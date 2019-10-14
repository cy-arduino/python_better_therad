import threading
import ctypes
import time
import logging


# A "BETTER" thread which support start(timeout=xxx) and terminate()
class BThread(threading.Thread):
    LOG_FMT = "%(asctime)s [%(levelname)s] " \
              "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"

    def _process_timeout(self, timeout=None):
        ret = 0

        if timeout:
            try:
                timeout = float(timeout)
                if timeout >= 0:
                    ret = timeout
                else:
                    raise ValueError('less than 0')
            except ValueError as e:
                self._log.error(e)
                raise ValueError('not a float')

        return ret

    # timeout(float, >=0):
    #    0: no timeout
    # exception:
    #    ValueError: invalid timeout
    def __init__(self, *args, **kwargs):
        # 'timeout' is not for original thread
        self.default_timeout = None
        if 'timeout' in kwargs:
            self.default_timeout = self._process_timeout(kwargs['timeout'])
            del kwargs['timeout']

        super(BThread, self).__init__(*args, **kwargs)

        self.setName(self.name + '_GThread_' + time.strftime("%Y%m%d-%H%M%S"))

        logging.basicConfig(level=logging.WARNING, format=self.LOG_FMT)
        self._log = logging.getLogger(self.getName())

        # terminate this thread when sys.exit()
        # self.setDaemon(True)

    # level: python logging's level
    def dbg(self, level=logging.DEBUG):
        self._log.setLevel(level)

    # timeout(float, >=0):
    #    0: no timeout
    # exception:
    #    ValueError: invalid timeout
    def set_timeout(self, timeout):
        self.default_timeout = self._process_timeout(timeout)

    # timeout(float, >=0):
    #    0: no timeout
    # exception:
    #    ValueError: invalid timeout
    def start(self, timeout=None):

        if timeout or self.default_timeout:
            if not timeout:
                timeout = self.default_timeout

            self._log.info("timeout=%s", timeout)

            # create another thread to terminate self if timeout
            t = threading.Thread(target=self._terminator,
                                 args=(self, timeout))
            t.start()

        super(BThread, self).start()

    def _terminator(self, thread, timeout):
        self._log.debug("%s's terminator", thread.name)

        time.sleep(timeout)
        if thread and thread.is_alive():
            self._log.info("terminate %s", thread.name)
            thread.terminate()

    # ret:
    #   True: success
    #   False: fail
    def terminate(self):
        if self.is_alive():
            self._log.info('terminate thread <%s> tid=%s',
                           self.name, self.ident)

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
def infinite_loop(name):
    interval = 0.1
    i = 1
    while True:
        print('{}: infinite_loop...{}'.format(name, i))
        i += interval
        time.sleep(interval)


def test_terminate_thread_asyn():
    print("Terminate thread asynchronously")
    t = BThread(target=infinite_loop, args=('test_terminate_thread_asyn',))
    t.dbg(logging.ERROR)

    t.start()

    time.sleep(2)
    print("TERMINATE")
    t.terminate()

    t.join()


def test_start_with_timeout():
    print("Start thread with timeout 3s")
    t = BThread(target=infinite_loop, args=('test_start_timeout',))
    t.dbg(logging.DEBUG)

    t.start(timeout=3)

    t.join()


def test_set_timeout1():
    print("Set timeout #1 3s")
    t = BThread(target=infinite_loop, args=('test_set_timeout1',), timeout=3)
    t.dbg(logging.DEBUG)

    t.start()

    t.join()


def test_set_timeout2():
    print("Set timeout #2 3s")
    t = BThread(target=infinite_loop, args=('test_set_timeout2',))
    t.dbg(logging.DEBUG)
    t.set_timeout(3)

    t.start()

    t.join()


if __name__ == '__main__':
    test_terminate_thread_asyn()
    # test_start_with_timeout()
    # test_set_timeout1()
    # test_set_timeout2()
