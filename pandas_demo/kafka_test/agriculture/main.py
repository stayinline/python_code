import threading

import dirt_data
import env_data
import persion_data

if __name__ == '__main__':
    thread1 = threading.Thread(target=env_data.generate_env_data)
    thread2 = threading.Thread(target=dirt_data.generate_dirt_data)
    thread3 = threading.Thread(target=persion_data.generate_persion_data)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    print("所有线程执行完毕，主线程结束")
