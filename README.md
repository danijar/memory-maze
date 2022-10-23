**Status:** Stable release

[![PyPI](https://img.shields.io/pypi/v/memory-maze.svg)](https://pypi.python.org/pypi/memory-maze/#history)

# memory-maze

Memory Maze environment for evaluating long-term memory of RL agents.

| Memory 9x9 | Memory 11x11 | Memory 13x13 | Memory 15x15 |
|------------|--------------|--------------|--------------|
| <img width="100%" alt="map-9x9" src="https://user-images.githubusercontent.com/3135115/177040204-fbf3b558-d063-49d3-9973-ae113137782f.png"> | <img width="100%" alt="map-11x11" src="https://user-images.githubusercontent.com/3135115/177040184-16ccb614-b897-44db-ab2c-7ae66e14c007.png"> | <img width="100%" alt="map-13x13" src="https://user-images.githubusercontent.com/3135115/177040164-d3edb11f-de6a-4c17-bce2-38e539639f40.png"> | <img width="100%" alt="map-15x15" src="https://user-images.githubusercontent.com/3135115/177040126-b9a0f861-b15b-492c-9216-89502e8f8ae9.png"> |


For more details see the accompanying research paper: [Evaluating Long-Term Memory in 3D Mazes](https://arxiv.org/TODO)
```
@article{pasukonis2022memmaze,
  title={Evaluating Long-Term Memory in 3D Mazes},
  author={Jurgis Pasukonis, Timothy Lillicrap, Danijar Hafner},
  year={2022},
  journal={arXiv preprint arXiv:2210.xxxxx},
}
```

## Installation

The environment is available as a pip package
```
pip install memory-maze
```
It will automatically install [`dm_control`](https://github.com/deepmind/dm_control) and [`mujoco`](https://github.com/deepmind/mujoco) dependencies.

## Task

Memory Maze is a task designed to test the memory abilities of RL agents.

The task is based on a game known as Scavenger Hunt (or Treasure Hunt). The agent starts in a randomly generated maze, which contains a number of landmarks of different colors. Agent is prompted to find the target landmark of a specific color, indicated by the border color in the observation image. Once the agent successfully finds and touches the correct landmark, it gets a +1 reward and the next random landmark is chosen as a target. If the agent touches the landmark of the wrong color, there is no effect. Throughout the episode the maze layout and the locations of the landmarks do not change. The episode continues for a fixed amount of time, and so the total episode reward is equal to the number of targets the agent can find in the given time. 

<p align="center">
    <img width="256" src="https://user-images.githubusercontent.com/3135115/177040240-847f0f0d-b20b-4652-83c3-a486f6f22c22.gif">
</p>

Memory Maze tests the memory of the agent in a clean and direct way, because an agent with perfect memory will only have to explore the maze once (which is possible in a time much shorter than the length of episode) and then just follow the shortest path to the target, whereas an agent with no memory will have to randomly wonder through the maze to find each target.

There are 4 size variations of the maze. The largest maze 15x15 is designed to be challenging but solvable for humans (see benchmark results below), but out of reach for the state-of-the-art RL methods. The smaller sizes are provided as stepping stones, with 9x9 solvable with current RL methods.

| Size      | Landmarks | Episode steps | env_id                |
|-----------|-----------|---------------|-----------------------|
| **9x9**   | 3         | 1000          | `MemoryMaze-9x9-v0`   |
| **11x11** | 4         | 2000          | `MemoryMaze-11x11-v0` |
| **13x13** | 5         | 3000          | `MemoryMaze-13x13-v0` |
| **15x15** | 6         | 4000          | `MemoryMaze-15x15-v0` |

Note that the mazes are generated with [labmaze](https://github.com/deepmind/labmaze), the same algorithm as used by [DmLab-30](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/dmlab30). In particular, 9x9 corresponds to the [small](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/dmlab30#goal-locations-small) variant and 15x15 corresponds to the [large](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/dmlab30#goal-locations-large) variant.

## Gym interface

Once pip package is installed, the environment can be created using [Gym](https://github.com/openai/gym) interface

```python
!pip install gym
import gym

env = gym.make('memory_maze:MemoryMaze-9x9-v0')
env = gym.make('memory_maze:MemoryMaze-11x11-v0')
env = gym.make('memory_maze:MemoryMaze-13x13-v0')
env = gym.make('memory_maze:MemoryMaze-15x15-v0')
```

The default environment has 64x64 image observations
```python
>>> env.observation_space
Box(0, 255, (64, 64, 3), uint8)
```

There are 6 discrete actions:
```python
>>> env.action_space
Discrete(6)  # (noop, forward, left, right, forward_left, forward_right)
```

In order to create an environment with extra observations, use the environment id with `-ExtraObs-v0` suffix:
```python
>>> env = gym.make('memory_maze:MemoryMaze-9x9-ExtraObs-v0')
>>> env.observation_space
Dict(
    agent_dir: Box(-inf, inf, (2,), float64), 
    agent_pos: Box(-inf, inf, (2,), float64),
    image: Box(0, 255, (64, 64, 3), uint8),
    maze_layout: Box(0, 1, (9, 9), uint8),
    target_color: Box(-inf, inf, (3,), float64),
    target_pos: Box(-inf, inf, (2,), float64),
    target_vec: Box(-inf, inf, (2,), float64),
    targets_pos: Box(-inf, inf, (3, 2), float64),
    targets_vec: Box(-inf, inf, (3, 2), float64)
)
```

There are other helper variations of the environment, see [here](memory_maze/__init__.py).

## dm_env interface

We also provide [dm_env](https://github.com/deepmind/dm_env) API implementation:

```python
from memory_maze import tasks

env = tasks.memory_maze_9x9()
env = tasks.memory_maze_11x11()
env = tasks.memory_maze_13x13()
env = tasks.memory_maze_15x15()
```

The observation is a dictionary, which includes `image` observation key
```python
>>> env.observation_spec()
{
  'image': BoundedArray(shape=(64, 64, 3), ...)
}
```

The constructor accepts a number of arguments, which can be used to tweak the environment:
```python
env = tasks.memory_maze_9x9(
    global_observables=True,
    image_only_obs=False,
    top_camera=False,
    camera_resolution=64,
    control_freq=4,
    discrete_actions=True,
)
```

## GUI

There is also a graphical UI provided, which can be launched as:

```bash
pip install gym pygame pillow imageio

# The default view, that the agent sees
python gui/run_gui.py --fps=6 --env "memory_maze:MemoryMaze-15x15-v0"

# Higher resolution and higher control frequency, nicer for human control
python gui/run_gui.py --fps=60 --env "memory_maze:MemoryMaze-15x15-HiFreq-HD-v0"
```

## Dataset

[**Data download here** (~100GB per dataset)](https://www.dropbox.com/sh/c38sc5h7ltgyyzc/AAARVeKgnyaoBLGdYYVABh_Ja)

We provide two datasets of experience collected from the Memory Maze environment: Memory Maze 9x9 (30M) and Memory Maze 15x15 (30M). Each dataset contains 30 thousand trajectories from Memory Maze 9x9 and 15x15 environments respectively, split into 29k trajectories for training and 1k for evaluation. All trajectories are 1000 steps long, so each dataset has 30M steps total.

The data is generated by running a scripted policy, which navigates to randomly chosen points in the maze under action noise. This choice of policy was made to generate diverse trajectories that explore the maze effectively and that form loops in space, which can be important for learning long-term memory. We intentionally avoid recording data with a trained agent to ensure a diverse data distribution and to avoid dataset bias that could favor some methods over others. Because of this, the rewards are quite sparse in the data, occuring on average 1-2 times per trajectory.

Each trajectory is saved as an NPZ file, these are the data entries available:

| Key            | Shape              | Type   | Description                                   |
|----------------|--------------------|--------|-----------------------------------------------|
| `image`        | (64, 64, 3)        | uint8  | First-person view observation                 |
| `action`       | (6)                | binary | Last action, one-hot encoded                  |
| `reward`       | ()                 | float  | Last reward                                   |
| `maze_layout`  | (9, 9) or (15, 15) | binary | Maze layout (wall / no wall)                  |
| `agent_pos`    | (2)                | float  | Agent position in global coordinates          |
| `agent_dir`    | (2)                | float  | Agent orientation as a unit vector            |
| `targets_pos`  | (3, 2) or (6, 2)   | float  | Object locations in global coordinates        |
| `targets_vec`  | (3, 2) or (6, 2)   | float  | Object locations in agent-centric coordinates |
| `target_pos`   | (2)                | float  | Current target object location, global        |
| `target_vec`   | (2)                | float  | Current target object location, agent-centric |
| `target_color` | (3)                | float  | Current target object color RGB               |

All tensors in NPZ have a time dimension, e.g. `image` tensor has shape (1001, 64, 64, 3). The tensor length is 1001 because there are 1000 steps (actions) in a trajectory, `image[0]` is the observation *before* the first action, and `image[-1]` is the observation *after* the last action. 

## Baselines

### Online RL Agents

In the [research paper](https://arxiv.org/TODO), we evaluated model-free [IMPALA](https://github.com/google-research/seed_rl/tree/master/agents/vtrace) and model-based [Dreamer](https://github.com/jurgisp/pydreamer) agent baselines

<p align="center">
  <img width="657" alt="baselines" src="https://user-images.githubusercontent.com/3135115/197349778-74073613-bf6c-449b-b5c2-07adf21030ff.png">
  <img width="641" alt="image" src="https://user-images.githubusercontent.com/3135115/197349818-3dcb7551-dafe-48f6-a2fe-6f79048198d4.png">
</p>

#### Sample videos

Here are sample episodes, played by a trained agent:

##### Memory 9x9 - Dreamer (TBTT)

https://user-images.githubusercontent.com/3135115/197378287-4e413440-7097-4d11-8627-3d7fac0845f1.mp4

##### Memory 9x9 - IMPALA (400M)

https://user-images.githubusercontent.com/3135115/197378929-7fe3f374-c11c-409a-8a95-03feeb489330.mp4

##### Memory 15x15 - Dreamer (TBTT)

https://user-images.githubusercontent.com/3135115/197378324-fb99b496-dba8-4b00-ad80-2d6e19ba8acd.mp4

##### Memory 15x15 - IMPALA (400M)

https://user-images.githubusercontent.com/3135115/197378936-939e7615-9dad-4765-b0ef-a49c5a38fe28.mp4

### Offline Probing

#### Sample videos

Sample probing trajectory videos. Note these trajectories are from the offline dataset, where the agent just navigates to random points in the maze, it does *not* try to collect rewards.

Bottom-left: Object location predictions (x) versus the actual locations (o).

Bottom-right: Wall layout predictions (dark green = true positive, light green = true negative, light red = false positive, dark red = false negative).

##### Memory 9x9 Walls Objects - RSSM (TBTT)

https://user-images.githubusercontent.com/3135115/197379227-775ec5bc-0780-4dcc-b7f1-660bc7cf95f1.mp4

##### Memory 9x9 Walls Objects - Supervised oracle

https://user-images.githubusercontent.com/3135115/197379235-a5ea0388-2718-4035-8bbc-064ecc9ea444.mp4

##### Memory 15x15 Walls Objects - RSSM (TBTT)

https://user-images.githubusercontent.com/3135115/197379245-fb96bd12-6ef5-481e-adc6-f119a39e8e43.mp4

##### Memory 15x15 Walls Objects - Supervised oracle

https://user-images.githubusercontent.com/3135115/197379248-26a8093e-8b54-443c-b154-e33e0383b5e4.mp4
