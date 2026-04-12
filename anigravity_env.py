from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State
from models import AnigravityAction, AnigravityObservation

class AnigravityEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.task_name = "easy_hover"
        self._setup_task()

    def _setup_task(self):
        self.dt = 0.1
        self.max_steps = 30
        self.step_count = 0
        self.altitude = 0.0
        self.velocity = 0.0
        self.fuel = 100.0
        self.target_altitude = 10.0

    def reset(self, task_name: str = None) -> State:
        if task_name:
            self.task_name = task_name
        self._setup_task()
        
        # Adjust starting conditions based on difficulty
        if self.task_name == "medium_landing":
            self.altitude = 50.0
            self.target_altitude = 0.0
        elif self.task_name == "hard_takeoff":
            self.target_altitude = 100.0

        return self._get_state()

    def step(self, action: AnigravityAction) -> State:
        self.step_count += 1
        
        gravity = 9.8
        thrust = action.thrust_level * 20.0
        
        # Burn fuel
        if self.fuel > 0:
            self.fuel -= action.thrust_level * 0.5
        else:
            thrust = 0.0 # Out of fuel!

        # Physics math: Acceleration = Thrust - Gravity
        acceleration = thrust - gravity
        self.velocity += acceleration * self.dt
        self.altitude += self.velocity * self.dt

        # Don't fall through the floor
        if self.altitude < 0:
            self.altitude = 0.0
            self.velocity = 0.0

        done = self.step_count >= self.max_steps
        
        # Reward the AI for getting close to the target
        distance = abs(self.target_altitude - self.altitude)
        reward = 1.0 / (1.0 + distance)

        return self._get_state(reward, done)

    # ---> THIS IS THE NEW MISSING FUNCTION <---
    def state(self) -> State:
        return self._get_state()

    def _get_state(self, reward=0.0, done=False) -> State:
        obs = AnigravityObservation(
            altitude=self.altitude,
            velocity=self.velocity,
            target_altitude=self.target_altitude,
            fuel_remaining=self.fuel
        )
        return State(observation=obs.model_dump(), reward=reward, done=done)
