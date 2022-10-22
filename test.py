from threading import Thread

x = 1

def a(s):
    print(x)
    def b(s):
        print(x)
        print(s)

    worker = Thread(target=b, kwargs={"s": s})
    worker.start()


if __name__ == '__main__':
    a(1)
