# PyScriptEngine
A python project for executing python embedded in HTML code.

To execute, simply run:
```python
from engine import *
__engine = Engine("path to html file")
__engine.execute_all_scripts()
```

You can also test this by running:
python main.py test/test.html

This library does prevent against the usage of modules like os, and sys, and functions like open and exec.
More will be covered, and you can keep adding more by editing the files in global_data.

Contributors:

1dime: owner

indie-dev: is also 1dime
