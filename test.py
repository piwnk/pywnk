from utils import interrupt_after, print_execution_time, profiler
import time


@interrupt_after(6)
@print_execution_time
@profiler()
def test():
    print('Starting')
    time.sleep(5)
    print('Ending')


if __name__ == '__main__':
    try:
        test()
    except TimeoutError:
        print('Interrupted')
