from model.user import Language
from enum import IntEnum

class WaterValue(IntEnum):
  GLASS = 0
  BOTTLE = 1

class WaterConsumption:
  def __init__(self, value: WaterValue, timestamp: int):
    self.value = int(value)
    self.timestamp = timestamp

  def to_dict(self):
    return {
      "value": self.value,
      "timestamp": self.timestamp
    }
