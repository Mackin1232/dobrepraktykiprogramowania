import os, pathlib, pytest
# wystarczy uruchomić ten plik

os.chdir(pathlib.Path.cwd() / 'tests')

pytest.main()