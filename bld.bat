conda config --add channels DLR-SC
conda config --add channels floatingpointstack
"%PYTHON%" setup.py install
if errorlevel 1 exit 1