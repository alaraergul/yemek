class MealEntry:
  def __init__(self, id: int, timestamp: int, count: int):
    self.id = id
    self.timestamp = timestamp
    self.count = count

  def to_dict(self):
    return {
      "id": self.id,
      "count": self.count,
      "timestamp": self.timestamp
    }
