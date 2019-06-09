Environment setup steps:
λ python --version                                                                                           
Python 3.7.3                                                                                                 
λ pip --version                                                                                              
pip 19.1.1 from c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages\pip (python 3.7)     
λ robot --version                                                                                            
Robot Framework 3.1.2 (Python 3.7.3 on win32)    

pip install -U wxPython
pip install robotframework-ride
Collecting robotframework-ride
  Downloading https://files.pythonhosted.org/packages/4e/a6/1835a17fa566b19c166735a9a75d55101e53b68566771ddb0b690dd4be83/robotframework_ride-1.7.3.1-py2.py3-none-any.whl (926kB)
     |████████████████████████████████| 931kB 2.2MB/s
Requirement already satisfied: robotframework in c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages (from robotframework-ride) (3.1.2)
Collecting Pywin32 (from robotframework-ride)
  Downloading https://files.pythonhosted.org/packages/8a/37/917c4020e93e0e854d4cbff1cbdf14ec45a6d1cedf52f8cafdea5b22451a/pywin32-224-cp37-cp37m-win32.whl (8.3MB)
     |████████████████████████████████| 8.3MB 3.3MB/s
Requirement already satisfied: wxPython in c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages (from robotframework-ride) (4.0.6)
Collecting robotframeworklexer (from robotframework-ride)
  Downloading https://files.pythonhosted.org/packages/24/18/ad01d42227d824b890f1b4d32237e5003bf7afe8764cb13545fb63d7fcb5/robotframeworklexer-1.1-py3-none-any.whl
Collecting Pypubsub (from robotframework-ride)
  Downloading https://files.pythonhosted.org/packages/1a/41/a0aceb552d8ec63bb1e8223d130f9dd0f736470036d75d708183b104a2cb/Pypubsub-4.0.3-py3-none-any.whl (61kB)
     |████████████████████████████████| 61kB 2.0MB/s
Collecting Pygments (from robotframework-ride)
  Downloading https://files.pythonhosted.org/packages/5c/73/1dfa428150e3ccb0fa3e68db406e5be48698f2a979ccbcec795f28f44048/Pygments-2.4.2-py2.py3-none-any.whl (883kB)
     |████████████████████████████████| 890kB 6.4MB/s
Requirement already satisfied: pillow in c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages (from wxPython->robotframework-ride) (6.0.0)
Requirement already satisfied: six in c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages (from wxPython->robotframework-ride) (1.12.0)
Requirement already satisfied: numpy in c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages (from wxPython->robotframework-ride) (1.16.4)
ERROR: robotframework-ride 1.7.3.1 has requirement Pypubsub==3.3.0, but you'll have pypubsub 4.0.3 which is incompatible.
Installing collected packages: Pywin32, robotframeworklexer, Pypubsub, Pygments, robotframework-ride
Successfully installed Pygments-2.4.2 Pypubsub-4.0.3 Pywin32-224 robotframework-ride-1.7.3.1 robotframeworklexer-1.1

ride.py

λ pip install --upgrade robotframework-seleniumlibrary
Collecting robotframework-seleniumlibrary
  Downloading https://files.pythonhosted.org/packages/ff/15/6961c801eeec7f062973509958b33f158bbc505d45ee6c20b2966275ef51/robotframework_seleniumlibrary-3.3.1-py2.py3-none-any.whl (81kB)
     |████████████████████████████████| 81kB 1.1MB/s
Requirement already satisfied, skipping upgrade: robotframework>=2.8.7 in c:\users\pc\appdata\local\programs\python\python37-32\lib\site-packages (from robotframework-seleniumlibrary) (3.1.2)
Collecting selenium>=3.4.0 (from robotframework-seleniumlibrary)
  Downloading https://files.pythonhosted.org/packages/80/d6/4294f0b4bce4de0abf13e17190289f9d0613b0a44e5dd6a7f5ca98459853/selenium-3.141.0-py2.py3-none-any.whl (904kB)
     |████████████████████████████████| 911kB 6.8MB/s
Collecting urllib3 (from selenium>=3.4.0->robotframework-seleniumlibrary)
  Downloading https://files.pythonhosted.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl (150kB)
     |████████████████████████████████| 153kB 6.4MB/s
Installing collected packages: urllib3, selenium, robotframework-seleniumlibrary
Successfully installed robotframework-seleniumlibrary-3.3.1 selenium-3.141.0 urllib3-1.25.3
