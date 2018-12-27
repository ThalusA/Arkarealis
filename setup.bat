@echo off
color 07
pip install -r ./requirements.txt
rd /q /s build
python setup.py build
echo "BUILD SUCCEFULLY"
pause