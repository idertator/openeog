# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.7.2
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x01a\
<\
svg xmlns=\x22http:\
//www.w3.org/200\
0/svg\x22 height=\x222\
4px\x22 viewBox=\x220 \
-960 960 960\x22 wi\
dth=\x2224px\x22 fill=\
\x22#5f6368\x22><path \
d=\x22M160-160q-33 \
0-56.5-23.5T80-2\
40v-480q0-33 23.\
5-56.5T160-800h2\
40l80 80h320q33 \
0 56.5 23.5T880-\
640H447l-80-80H1\
60v480l96-320h68\
4L837-217q-8 26-\
29.5 41.5T760-16\
0H160Zm84-80h516\
l72-240H316l-72 \
240Zm0 0 72-240-\
72 240Zm-84-400v\
-80 80Z\x22/></svg>\
\
"

qt_resource_name = b"\
\x00\x08\
\x06\xc1T\x07\
\x00o\
\x00p\x00e\x00n\x00.\x00s\x00v\x00g\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x90\x87\x9apu\
"


def qInitResources():
    QtCore.qRegisterResourceData(
        0x03, qt_resource_struct, qt_resource_name, qt_resource_data
    )


def qCleanupResources():
    QtCore.qUnregisterResourceData(
        0x03, qt_resource_struct, qt_resource_name, qt_resource_data
    )


qInitResources()
