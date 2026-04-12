from pydantic import BaseModel, Field

# What the AI sees
class AnigravityObservation(BaseModel):
    altitude: float = Field(0.0, description="Current height in meters")
    velocity: float = Field(0.0, description="Current vertical speed")
    target_altitude: float = Field(10.0, description="Target height to maintain")
    fuel_remaining: float = Field(100.0, description="Remaining fuel percentage")

# What the AI can do
class AnigravityAction(BaseModel):
    thrust_level: float = Field(0.0, ge=0.0, le=1.0, description="Thrust power (0 to 1)")