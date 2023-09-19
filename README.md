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

### Example 1 (Toy example)

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


### Example 2 (FastAPI Integration)

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


### Example 3 (Batching)

1. Deploy model
```
cd src/example_3
chmod +x ./deploy.sh
./deploy.sh
```

2. Test model api
```
cd src/example_3
python test_app.py
```

3. Navigate to http://127.0.0.1:8003/docs to interact with the api and view the api documentation

4. Navigate to http://127.0.0.1:8001/ to view the ray dashboard

5. Navigate to http://127.0.0.1:8002/ to view the ray metrics


### Example 4 (Multiple models)

1. Deploy model
```
cd src/example_4
chmod +x ./deploy.sh
./deploy.sh
```

2. Test model api
```
cd src/example_4
python test_app.py
```

3. Navigate to http://127.0.0.1:8003/docs to interact with the api and view the api documentation

4. Navigate to http://127.0.0.1:8001/ to view the ray dashboard

5. Navigate to http://127.0.0.1:8002/ to view the ray metrics

## Useful Commands

* Generate serve config files (Recommended approach for production)
```shell
# i.e. serve build app:deployment -o config.yaml --single-app
# i.e. serve build app:deployment -o config.yaml --multi-app
serve build <module>:<deployment> -o <output config yaml file>
```

* Check health status
```shell
serve status
```

* Check current deployed serve config
```shell
serve config
```

* Deploy/Redeploy deployment graph

- A rolling update is performed if there are multiple replicas. Might end up getting responses from older replicas when the update is in progress.
- If there is no code or config change for the deployment/application, then no deploy operation will be performed on it.  

```shell
# i.e. serve deploy config.yaml
# --dashboard-agent-listen-port in ray start defaults to 52365
# serve deploy config.yaml --address http://localhost:52365 (Can also be specified using RAY_AGENT_ADDRESS environment variable)
serve deploy <config yaml file>
```