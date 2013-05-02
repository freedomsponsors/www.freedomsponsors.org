import socket

hn = socket.gethostname()
print('hostname: %s' % hn)
h = socket.gethostbyname(hn)
print('host: %s' % h)