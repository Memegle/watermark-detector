#!/bin/bash

python3 -m pip install --upgrade pip || ((count++))
python3 -m pip install tensorflow || ((count++))
python3 -m pip install keras || ((count++))