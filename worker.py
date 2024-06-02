import queue
import threading
import time


class Task:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


def greet(id: str, name: str, age: int):
    print(f'[{id}]: My name is {name}, and I\'m {age} years old.')


def producer_1(q: queue.Queue):
    for i in range(10):
        task = Task(greet, id='Producer 1', name='Bob', age=i)
        q.put(task)
        time.sleep(.1)


def producer_2(q: queue.Queue):
    for i in range(10):
        task = Task(print, f'[Producer 2]: Magic number is {i}')
        q.put(task)
        time.sleep(.1)


def consumer(q: queue.Queue):
    while True:
        task = q.get()
        if task is None:  # Exit signal
            break
        task()
        q.task_done()


task_queue = queue.Queue()

producer_1_thread = threading.Thread(target=producer_1, args=(task_queue,))
producer_2_thread = threading.Thread(target=producer_2, args=(task_queue,))
consumer_thread = threading.Thread(target=consumer, args=(task_queue,))

producer_1_thread.start()
producer_2_thread.start()
consumer_thread.start()

producer_1_thread.join()
producer_2_thread.join()
task_queue.put(None)  # Send signal to consumer to exit
consumer_thread.join()
