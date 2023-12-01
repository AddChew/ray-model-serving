#!/bin/bash

source activate model-serving
ray start --head --dashboard-port 8001 --metrics-export-port 8002
serve run app:model -p 8003