#!/bin/bash

conda create -n model-serving python=3.10 -y
conda activate model-serving
pip install -r requirements.txt