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

3. Navigate to http://127.0.0.1:8000/docs to interact with the api and view the api documentation

4. Navigate to http://127.0.0.1:8265/ to view the ray dashboard


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

3. Navigate to http://127.0.0.1:8000/docs to interact with the api and view the api documentation

4. Navigate to http://127.0.0.1:8265/ to view the ray dashboard


### Example 3

1. Deploy model
```
cd src/example_3
chmod +x ./deploy.sh
./deploy.sh
```

2. Test model api
```
cd src/example_2
python test_app.py
```

3. Navigate to http://127.0.0.1:8003/docs to interact with the api and view the api documentation

4. Navigate to http://127.0.0.1:8001/ to view the ray dashboard

5. Navigate to http://127.0.0.1:8002/ to view the ray metrics