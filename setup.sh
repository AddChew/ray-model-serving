#!/bin/bash

conda create -n model-serving python=3.10 -y
source activate model-serving
pip install -r requirements.txt