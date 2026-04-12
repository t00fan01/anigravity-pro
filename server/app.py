import sys
import os

# This line is CRITICAL so the server folder can see your root files!
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from openenv.core.env_server.http_server import create_app
except ImportError:
    pass

from models import AnigravityAction, AnigravityObservation
from anigravity_env import AnigravityEnvironment

app = create_app(
    AnigravityEnvironment,
    AnigravityAction,
    AnigravityObservation,
    env_name="anigravity_pro",
    max_concurrent_envs=1, 
)

def main(host: str = "0.0.0.0", port: int = 7860):
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == '__main__':
    main()