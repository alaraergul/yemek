from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from controller.user_controller import user_blueprint, send_user_services
from controller.meal_controller import meal_blueprint, send_meal_services
from controller.water_consumption_controller import water_consumption_blueprint, send_water_consumption_services
from controller.custom_meal_controller import custom_meal_blueprint, send_custom_meal_services

from repository.user_repository import UserRepository
from repository.meal_repository import MealRepository
from repository.water_consumption import WaterConsumptionRepository
from repository.custom_meal_repository import CustomMealRepository

from service.database_service import DatabaseService
from service.meal_service import MealService
from service.user_service import UserService
from service.water_consumption_service import WaterConsumptionService

load_dotenv()

app = Flask(__name__)
CORS(app)

database_service = DatabaseService()

user_repository = UserRepository(database_service)
meal_repository = MealRepository(database_service)
water_consumption_repository = WaterConsumptionRepository(database_service)
custom_meal_repository = CustomMealRepository(database_service)

user_service = UserService(user_repository)
meal_service = MealService(meal_repository, custom_meal_repository)
water_consumption_service = WaterConsumptionService(water_consumption_repository)

send_user_services(user_service)
app.register_blueprint(user_blueprint, url_prefix="/users")

send_meal_services(meal_service, user_service)
app.register_blueprint(meal_blueprint, url_prefix="/meals")

send_water_consumption_services(water_consumption_service, user_service)
app.register_blueprint(water_consumption_blueprint, url_prefix="/water-consumption")

send_custom_meal_services(meal_service, user_service)
app.register_blueprint(custom_meal_blueprint, url_prefix="/custom-meals")

if __name__ == "__main__":
  app.run(port = 8087, host = "0.0.0.0")
