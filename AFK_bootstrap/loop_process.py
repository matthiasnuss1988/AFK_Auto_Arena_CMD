import time
from multiprocessing import Process, Event

def long_duration_loop(stop, conn):
    try:
        for i in range(10):
            for j in range(1000):
                if stop.is_set():
                    break
                time.sleep(1)
                conn.send(j)
        else:
            conn.send("Finished")
    except Exception as e:
        conn.send(str(e))
    finally:
        conn.close()


