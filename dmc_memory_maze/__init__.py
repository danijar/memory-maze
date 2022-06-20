
from . import tasks

try:
    # Register gym environments, if gym is available

    from typing import Callable
    from functools import partial as f

    import dm_env
    import gym
    from gym.envs.registration import register

    from .gym_wrappers import GymWrapper

    def _make_gym_env(dm_task: Callable[[], dm_env.Environment], **kwargs):
        dmenv = dm_task(**kwargs)
        return GymWrapper(dmenv)

    sizes = {
        '9x9': tasks.memory_maze_9x9,
        '11x11': tasks.memory_maze_11x11,
        '13x13': tasks.memory_maze_13x13,
        '15x15': tasks.memory_maze_15x15,
    }

    for key, dm_task in sizes.items():
        register(id=f'MemoryMaze-{key}-v0', entry_point=f(_make_gym_env, dm_task))  # Standard
        register(id=f'MemoryMaze-{key}-Vis-v0', entry_point=f(_make_gym_env, dm_task, good_visibility=True))  # Easily visible targets
        register(id=f'MemoryMaze-{key}-HD-v0', entry_point=f(_make_gym_env, dm_task, camera_resolution=256))  # High-res camera
        register(id=f'MemoryMaze-{key}-Top-v0', entry_point=f(_make_gym_env, dm_task, camera_resolution=64, top_camera=True))  # Top-down camera
        register(id=f'MemoryMaze-{key}-Img-v0', entry_point=f(_make_gym_env, dm_task, image_only_obs=True))  # Image-only observation
        
        # High control frequency
        register(id=f'MemoryMaze-{key}-HiFreq-v0', entry_point=f(_make_gym_env, dm_task, control_freq=40))
        register(id=f'MemoryMaze-{key}-HiFreq-Vis-v0', entry_point=f(_make_gym_env, dm_task, control_freq=40, good_visibility=True))
        register(id=f'MemoryMaze-{key}-HiFreq-HD-v0', entry_point=f(_make_gym_env, dm_task, control_freq=40, camera_resolution=256))
        register(id=f'MemoryMaze-{key}-HiFreq-Top-v0', entry_point=f(_make_gym_env, dm_task, control_freq=40, camera_resolution=256, top_camera=True))
        register(id=f'MemoryMaze-{key}-HiFreq-Img-v0', entry_point=f(_make_gym_env, dm_task, control_freq=40, image_only_obs=True))


except ImportError:
    print('dmc_memory_maze: gym environments not registered.')
    raise
