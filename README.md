# Ray Model Serving
Toy Repository to experiment with Ray Serve for model serving.

## Installation Instructions

Run setup.sh to install the necessary libraries.
```
chmod +x ./setup.sh
./setup.sh
conda activate model-serving
```

## How to run examples

### Example 1

1. Deploy model
```
cd src/example_1
serve run app:deployment
```

2. Test model api
```
cd src/example_1
python test_app.py
```

### Example 2

1. Deploy model
```
cd src/example_2
serve run app:deployment
```

2. Test model api
```
cd src/example_2
python test_app.py
```