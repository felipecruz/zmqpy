#include <stdio.h>
#include <zmq.h>

int
    main(int argc, char *argv)
{
    int i = 0;
    char buf[10];

    void *context = zmq_init(1);
    void *receiver = zmq_socket(context, ZMQ_PULL);

    printf("%d connect\n", zmq_connect(receiver, "tcp://localhost:3333"));
    //printf("%d connect\n", zmq_connect(receiver, "ipc:///tmp/zmqpy_bench"));

    zmq_msg_t m;

    for (i = 0; i < 10000000; i++) {

#if (ZMQ_VERSION_MAJOR == 3)
        zmq_recv(receiver, buf, 10, 0);
#else
        zmq_msg_init(&m);
        if (i % 10000 == 0)
            printf("%d\n", i);
        zmq_recv(receiver, &m, 0);
        zmq_msg_close(&m);
#endif
    }

    zmq_close(receiver);
    zmq_term(context);
}
