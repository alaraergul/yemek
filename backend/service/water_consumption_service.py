from typing import List

from repository.water_consumption import WaterConsumptionRepository

from model.water_consumption import WaterConsumption, WaterValue

class WaterConsumptionService:
  def __init__(self, water_consumption_repository: WaterConsumptionRepository):
    self.water_consumption_repository = water_consumption_repository

  def get_water_consumption(self, user_id: str) -> List[WaterConsumption]:
    water_consumption = self.water_consumption_repository.get_water_consumption(user_id)

    for data in water_consumption:
      data.timestamp *= 1000

    return water_consumption

  def push_water_consumption(self, user_id: str, value: WaterValue, timestamp: int) -> bool:
    return self.water_consumption_repository.push_water_consumption(user_id, value, timestamp / 1000)
  
  def delete_user_all_consumption(self, user_id: str) -> bool:
    return self.water_consumption_repository.delete_user_water_consumption(user_id)