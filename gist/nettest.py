import cockle
cockle.connect('Kitchen2','c3fnh0ile')
url = "http://cefn.com/blog/files/"
_, _, host, path = url.split('/', 3)
import usocket
import gc
import sys

addr = usocket.getaddrinfo(host, 80)[0][-1]
s = usocket.socket()
s.connect(addr)
s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))

buf = bytearray(128)
while True:
    gc.collect()
    try:
        count = s.readinto(
            buf)  # TODO use readline for headers including e.g. 'content-length: 2358' then after blank line, count bytes before close
        if count > 0:
            if count < len(buf):
                sys.stdout.write(buf[:count])
            else:
                sys.stdout.write(buf)
            continue
    except OSError as ose:
        print(ose)
    break
s.close()
