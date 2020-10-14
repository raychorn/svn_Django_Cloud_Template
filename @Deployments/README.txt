/usr/local/@@TEMPLATE@@

cd /usr/local/cargochief
ln -s /usr/local/@@TEMPLATE@@/_Django-1.3_Multi-Threaded _Django-1.3_Multi-Threaded
ln -s /usr/local/@@TEMPLATE@@/vyperlogix_2_7_0.zip vyperlogix_2_7_0.zip

# see also find-libs.sh for some hints on how to replace all the symlinks, in case this is required.

What ports currently have listeners ?
netstat -lnptu

OR

lsof -i

OR

psutil --> http://code.google.com/p/psutil/wiki/Documentation

OR

Run through all the ports by attempting to bind to each... choose an open port... ?!?

try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind((HOST, PORT))
except socket.error, e:
    pass
    
See also:  "J:\@Research\@Python\Port Scanner"


    