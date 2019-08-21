import os
from robot import libdoc
from version import VERSION

libraries = ['APILibrary.py', 'GUILibrary.py', 'SOAPLibrary.py', 'DesktopLibrary.py']
curr_dir = os.path.dirname(os.path.realpath(__file__)).replace('docs', '')
for file in libraries:
    libdoc.libdoc(curr_dir+'src/Zoomba/'+file, curr_dir+'docs/'+file.replace('.py', 'Documentation.html'),
                  name=file.replace(".py", "").replace("Lib", "_Lib"), version=VERSION)
