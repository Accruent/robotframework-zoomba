import os
import sys
from robot import libdoc
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import version

print("Generating new documentation...")
libraries = ['APILibrary.py', 'GUILibrary.py', 'SOAPLibrary.py', 'DesktopLibrary.py', 'MobileLibrary.py']
curr_dir = os.path.dirname(os.path.realpath(__file__)).replace('docs', '')
for file in libraries:
    libdoc.libdoc(curr_dir+'src/Zoomba/'+file, curr_dir+'docs/'+file.replace('.py', 'Documentation.html'),
                  name=file.replace(".py", "").replace("Lib", "_Lib"), version=version.VERSION)
