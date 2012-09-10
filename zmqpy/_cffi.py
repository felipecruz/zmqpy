# coding: utf-8

from cffi import FFI

from error import *

ffi = FFI()

ffi.cdef('''

typedef struct {
    void *content;
    unsigned char flags;
    unsigned char vsm_size;
    unsigned char vsm_data [30];
} zmq_msg_t;

void* zmq_init(int);
int zmq_term(void *context);

void* zmq_socket(void *context, int type);
int zmq_close(void *socket);

int zmq_bind(void *socket, const char *endpoint);
int zmq_connect(void *socket, const char *endpoint);

int zmq_send(void *socket, zmq_msg_t *msg, int flags);
int zmq_recv(void *socket, zmq_msg_t *msg, int flags);

int zmq_errno(void);

int zmq_getsockopt(void *socket,
                   int option_name,
                   void *option_value,
                   size_t *option_len);

int zmq_setsockopt(void *socket,
                   int option_name,
                   const void *option_value,
                   size_t option_len);

typedef ... zmq_free_fn;

int zmq_msg_init(zmq_msg_t *msg);
int zmq_msg_init_size(zmq_msg_t *msg, size_t size);
int zmq_msg_init_data(zmq_msg_t *msg,
                      void *data,
                      size_t size,
                      zmq_free_fn *ffn,
                      void *hint);

size_t zmq_msg_size(zmq_msg_t *msg);
void *zmq_msg_data(zmq_msg_t *msg);
int zmq_msg_close(zmq_msg_t *msg);


typedef struct
{
    void *socket;
    int fd;
    short events;
    short revents;
} zmq_pollitem_t;

int zmq_poll(zmq_pollitem_t *items, int nitems, long timeout);

char* strncpy(char* dest, char* orig, size_t len);

''')

C = ffi.verify('''
    #include <string.h>
    #include <zmq.h>
''', libraries=['c', 'zmq'])

nsp = new_sizet_pointer = lambda length: ffi.new('size_t*', length)

new_uint64_pointer = lambda: (ffi.new('uint64_t*'),
                              nsp(ffi.sizeof('uint64_t')))
new_int64_pointer = lambda: (ffi.new('int64_t*'),
                             nsp(ffi.sizeof('int64_t')))
new_int_pointer = lambda: (ffi.new('int*'),
                           nsp(ffi.sizeof('int')))
new_binary_data = lambda length: (ffi.new('char[%d]' % (length)),
                                  nsp(ffi.sizeof('char') * length))

value_uint64_pointer = lambda val : (ffi.new('uint64_t*', val),
                                     ffi.sizeof('uint64_t'))
value_int64_pointer = lambda val: (ffi.new('int64_t*', val),
                                   ffi.sizeof('int64_t'))
value_int_pointer = lambda val: (ffi.new('int*', val),
                                 ffi.sizeof('int'))
value_binary_data = lambda val, length: (ffi.new('char[%d]' % (length), val),
                                         ffi.sizeof('char') * length)
