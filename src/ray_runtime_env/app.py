from ray import serve
from fastapi import FastAPI


app = FastAPI()


@serve.deployment(
    ray_actor_options = {
        "runtime_env":{"pip": ["lightgbm==4.0.0", "scikit-learn==1.3.1"]},
        "num_cpus": 0.5
    }
)
class V1:

    def __call__(self):
        import lightgbm
        import sklearn
        return f"lightgbm version {lightgbm.__version__}, sklearn version {sklearn.__version__}"
    

@serve.deployment(
    ray_actor_options = {
        "runtime_env": {"pip": ["lightgbm==4.2.0", "scikit-learn==1.3.2"]},
        "num_cpus": 0.5
    }
)
class V2:

    def __call__(self):
        import lightgbm
        import sklearn
        return f"lightgbm version {lightgbm.__version__}, sklearn version {sklearn.__version__}"


@serve.deployment(ray_actor_options = {"num_cpus": 0.5})
@serve.ingress(app)
class Ingress:

    def __init__(self, v1_handle, v2_handle):
        self.v1_handle = v1_handle
        self.v2_handle = v2_handle

    @app.get("/{version}")
    async def get_deps(self, version):
        if version == "v1":
            ref = await self.v1_handle.remote()
            return await ref
        
        ref = await self.v2_handle.remote()
        return await ref


v1_handle = V1.bind()
v2_handle = V2.bind()
ingress = Ingress.bind(v1_handle, v2_handle)