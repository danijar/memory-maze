import functools

import numpy as np
from dm_control import composer
from dm_control.locomotion.arenas import labmaze_textures, mazes
from dm_control.locomotion.props import target_sphere
from dm_control.locomotion.tasks import random_goal_maze
from dm_control.locomotion.walkers import jumping_ball

from dmc_memory_maze.wrappers import (DiscreteActionSetWrapper,
                                      RemapObservationWrapper)
from dmc_memory_maze.maze import MemoryMaze

def test_maze(discrete_actions=True, random_state=None, top_camera=False):

    walker = jumping_ball.RollingBallWithHead(
        camera_height=0,
        add_ears=top_camera
    )

    # Build a maze with rooms and targets.
    wall_textures = labmaze_textures.WallTextures(style='style_01')
    arena = mazes.RandomMazeWithTargets(
        x_cells=11,
        y_cells=11,
        xy_scale=2.0,
        z_height=1.2,
        max_rooms=4,
        room_min_size=4,
        room_max_size=5,
        spawns_per_room=1,
        targets_per_room=1,
        wall_textures=wall_textures,
        skybox_texture=None,  # TODO: remove clouds
        aesthetic='outdoor_natural')

    # Build a task that rewards the agent for obtaining targets.
    task = MemoryMaze(
        walker=walker,
        maze_arena=arena,
        target_reward_scale=1.,
        contact_termination=False,
        enable_global_task_observables=True,
        )

    if top_camera:
        task.observables['top_camera'].enabled = True

    env = composer.Environment(
        time_limit=30,
        task=task,
        random_state=random_state,
        strip_singleton_obs_buffer_dim=True)

    camera_key = 'walker/egocentric_camera' if not top_camera else 'top_camera'
    env = RemapObservationWrapper(env, {'image': camera_key})

    if discrete_actions:
        env = DiscreteActionSetWrapper(env, [
            np.array([0., 0.]),  # noop
            np.array([-1., 0.]),  # move forward
            np.array([0., -1.]),  # turn left
            np.array([0., +1.]),  # turn right
            np.array([+1., 0.]),  # move backward
        ])

    return env
