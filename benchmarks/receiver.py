import zmqpy as zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://localhost:3333")

    for i in range(10000000):
        var = socket.recv()

    socket.close()
    context.term()

if __name__ == "__main__":
    main()
