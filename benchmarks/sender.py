import zmqpy as zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:3333")

    msg = "aaaaaaaaaa"

    for i in range(10000000):
        socket.send(msg, 0)

    socket.close()
    context.term()

if __name__ == "__main__":
    main()
