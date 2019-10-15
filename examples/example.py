import time
import logging
from bthread import BThread


def infinite_loop(name):
    interval = 1
    i = 0
    while True:

        if i > 10:
            print("ERROR")
            break

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
    LOG_FMT = "%(asctime)s [%(levelname)s] " \
              "%(filename)s:%(lineno)s %(name)s %(funcName)s() : %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)

    # test_terminate_thread_asyn()
    # test_start_with_timeout()
    # test_set_timeout1()
    test_set_timeout2()
