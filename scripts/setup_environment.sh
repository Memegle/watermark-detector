#!/bin/bash

count=0

python3 -m pip install --upgrade pip || ((count++))
python3 -m pip install tensorflow==1.13.2 || ((count++))
python3 -m pip install keras==2.1.5 || ((count++))

if ((count != 0)); then
  printf "\n\nFailed installing at least one of the dependencies, please try again or try installing manually\n"
else
  printf "\n\nPaddleOCR has been installed successfully\n"
fi

