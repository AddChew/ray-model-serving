import ray
from datetime import datetime


class DummyModelPipeline:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return "I am a dummy model pipeline"
    

@ray.remote # TODO: integrate with tenacity retry
class DummyShapPipeline: # TODO: Figure out why ray creates 2 actors

    def __init__(self, name, *args, **kwargs):
        self.name = name
        print(self.name)
        pass

    def write_to_file(self):
        print(self.name)
        time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filepath = f'./{time}.txt'
        with open(filepath, "w") as f:
            f.write(time + " " + self.name)
        return "Write to file successfully"
    
actor = DummyShapPipeline.remote("hello")