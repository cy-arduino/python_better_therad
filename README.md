# python_better_therad

## introduction
A "BETTER" thread(BThread) which extend thread.Thread and support 
terminate()/max execution time.

By default, a parent thread will be block until all children thread finished.
If some children thread not stop for some reason, you must use os._exit() in 
parent thread or kill it by `kill` in cmd line manually to force stop it.
If you want a children thread exit immediately when it's parent thread exit, 
you should set it as a daemon thread.

Terminate a thread may cause some problem because the thread is not correctly 
exit by itself.
This is the original design of threading.Thread.

With Bthread, you can set max execution time for a thread or terminate a running
thread asynchronously.


## install
`pip install bthread`

## Usage
Basically same as "threading.Thread". difference as following:

### hooked method:
* start(timeout=)
  * timeout(float, >=0): max execution time for this thread
  * modify thread name:
    * `[ori name]_GThread_[time]`

### new method:
* terminate()
  * terminate this thread
* set_timeout(timeout)
  * should be called before start()
  * set a max execution time for this thread
* dbg(level)
  * set debug level. Same as level in python's logging
    * see https://docs.python.org/3/library/logging.html#levels

## TODO
* pack this project
* upload to pypi
* add unit test
* 
