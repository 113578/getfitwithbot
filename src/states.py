from pydantic import BaseModel
from aiogram.fsm.state import State, StatesGroup


class UserState(BaseModel):
    user_id: int
    weight: int
    height: int
    age: int
    activity_level: int
    city: str
    calorie_goal: int
    water_goal: int
    logged_water: int
    logged_calories: int
    burned_calories: int


class ParametersState(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity_level = State()
    city = State()
    calorie_goal = State()
    water_goal = State()
    saving_parameters = State()
