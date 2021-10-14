# This workload tests running many instances of PPO (many actors)
# This covers https://github.com/ray-project/ray/pull/12148

import ray
from ray.tune import run_experiments
from ray.tune.utils.release_test_util import ProgressCallback

num_redis_shards = 5
redis_max_memory = 10**8
object_store_memory = 10**9
num_nodes = 3

message = ("Make sure there is enough memory on this machine to run this "
           "workload. We divide the system memory by 2 to provide a buffer.")
assert (num_nodes * object_store_memory + num_redis_shards * redis_max_memory <
        ray._private.utils.get_system_memory() / 2), message

# Simulate a cluster on one machine.

ray.init(address="auto")

# Run the workload.

run_experiments(
    {
        "ppo": {
            "run": "PPO",
            "env": "CartPole-v0",
            "num_samples": 10,
            "config": {
                "framework": "torch",
                "num_workers": 7,
                "num_gpus": 0,
                "num_sgd_iter": 1,
            },
            "stop": {
                "timesteps_total": 1,
            },
        }
    },
    callbacks=[ProgressCallback()])
