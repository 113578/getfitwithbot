import json
import aiohttp
from config.conifg import PYTHONPATH
from src.states import UserState


def save_user_info(user_info: UserState) -> None:
    """
    Сохраняет информацию о пользователе в JSON-файл.

    Parameters
    ------------
    user_info : UserState
        Объект, содержащий информацию о пользователе.

    Returns
    --------
    None
    """
    with open(f'{PYTHONPATH}/users/{user_info.user_id}.json', 'w', encoding='UTF-8') as file:
        json.dump(user_info.__dict__, file)


def load_user_info(user_id: int) -> UserState:
    """
    Загружает информацию о пользователе из JSON-файла.

    Parameters
    ------------
    user_id : int
        Уникальный идентификатор пользователя.

    Returns
    --------
    UserState
        Объект, содержащий информацию о пользователе.
    """
    with open(f'{PYTHONPATH}/users/{user_id}.json', 'r', encoding='UTF-8') as file:
        user_info_json = json.load(file)
        user_info = UserState(**user_info_json)
        return user_info


async def get_temperatures(city: str, api_key: str) -> float:
    """
    Получает текущую температуру для указанного города с использованием API OpenWeatherMap.

    Parameters
    ------------
    city : str
        Название города.
    api_key : str
        Ключ API для доступа к OpenWeatherMap.

    Returns
    --------
    float
        Температура в указанном городе в градусах Цельсия.
    """
    base_url = 'https://api.openweathermap.org/data/2.5/weather?'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, params=params) as response:
            response_data = await response.text()
            temperature = json.loads(response_data)['main']['temp']

    return temperature


async def get_nutritionix(query: str, application_id: str, api_key: str) -> float:
    """
    Получает информацию о калориях на основании запроса, используя API Nutritionix.

    Parameters
    ------------
    query : str
        Запрос, описывающий еду в свободной форме (например, '2 яблока').
    application_id : str
        ID приложения для API Nutritionix.
    api_key : str
        Ключ API для доступа к Nutritionix.

    Returns
    --------
    float
        Количество калорий для указанного запроса.
    """
    base_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    body = {
        'query': f'{query}'
    }
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': application_id,
        'x-app-key': api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url=base_url, headers=headers, json=body) as response:
            nutritionix = await response.json()
            calories = int(nutritionix['foods'][0]['nf_calories'])

    return calories
