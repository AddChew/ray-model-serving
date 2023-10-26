import ray
import pytest

from ray import serve


@pytest.fixture(scope = "session")
def ray_serve():
    ray.init(num_cpus = 1, ignore_reinit_error = True)
    yield serve.start(detached = True, http_options = {"host": "0.0.0.0"})
    ray.shutdown()