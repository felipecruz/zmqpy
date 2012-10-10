#include <stdio.h>
#include <zmq.h>
#include <stdlib.h>
#include <string.h>

void my_free (void *data, void *hint)
{
    free (data);
}

int
    main(int argc, char *argv)
{
    int i = 0;
    char msg[10] = "aaaaaaaaaa";

    void *context = zmq_init(1);
    void *sender = zmq_socket(context, ZMQ_PUSH);
    zmq_msg_t m;

    printf("%d bind\n", zmq_bind(sender, "tcp://*:3333"));
    //printf("%d bind\n", zmq_bind(sender, "ipc:///tmp/zmqpy_bench"));

    for (i = 0; i < 10000000; i++) {
        if (i % 10000 == 0)
            printf("%d\n", i);

#if (ZMQ_VERSION_MAJOR == 3)
        zmq_send(sender, msg, 10, 0);
#else
        zmq_msg_init_data(&m, msg, 10, NULL, 0);
        zmq_send(sender, &m, 0);
        zmq_msg_close(&m);
#endif
    }

    zmq_close(sender);
    zmq_term(context);
}
