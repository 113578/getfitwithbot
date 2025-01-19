import json
import aiohttp
from googletrans import Translator
from config.conifg import PYTHONPATH
from src.states import UserState


def save_user_data(user_data: UserState) -> None:
    """
    Сохраняет информацию о пользователе в JSON-файл.

    Parameters
    ----------
    user_data : UserState
        Объект, содержащий информацию о пользователе.

    Returns
    -------
    None
    """
    with open(f'{PYTHONPATH}/users/{user_data.user_id}.json', 'w', encoding='UTF-8') as file:
        json.dump(user_data.__dict__, file)


def load_user_data(user_id: int) -> UserState:
    """
    Загружает информацию о пользователе из JSON-файла.

    Parameters
    ----------
    user_id : int
        Уникальный идентификатор пользователя.

    Returns
    -------
    UserState
        Объект, содержащий информацию о пользователе.
    """
    with open(f'{PYTHONPATH}/users/{user_id}.json', 'r', encoding='UTF-8') as file:
        user_data_json = json.load(file)
        user_data = UserState(**user_data_json)
        return user_data


def mifflin_st_jeor(
        sex: str,
        weight: int,
        height: int,
        age: int,
        activity_level: int
) -> int:
    """
    Рассчитывает дневную норму калорий пользователя по формуле Mifflin-St Jeor.

    Parameters
    ----------
    sex : str
        Пол пользователя ('male' или 'female').
    weight : int
        Вес пользователя в килограммах.
    height : int
        Рост пользователя в сантиметрах.
    age : int
        Возраст пользователя в годах.
    activity_level : int
        Уровень активности (количество активных дней в неделю).

    Returns
    -------
    int
        Рассчитанная дневная норма калорий.
    """
    activity_coef = (activity_level + 1) * 0.1

    if sex == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    bmr += bmr * activity_coef
    bmr = int(bmr)

    return bmr


async def get_temperature(city: str, api_key: str) -> float:
    """
    Получает текущую температуру для указанного города с использованием API OpenWeatherMap.

    Parameters
    ----------
    city : str
        Название города.
    api_key : str
        Ключ API для доступа к OpenWeatherMap.

    Returns
    -------
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


def calculate_water_intake(sex: str, weight: int, activity_level: int) -> int:
    """
    Рассчитывает дневную норму потребления воды для пользователя.

    Parameters
    ----------
    sex : str
        Пол пользователя ('male' или 'female').
    weight : int
        Вес пользователя в килограммах.
    activity_level : int
        Уровень активности (количество активных дней в неделю).

    Returns
    -------
    int
        Рассчитанное количество воды в миллилитрах.
    """
    activity_coef = (activity_level + 1) * 0.1

    if sex == 'male':
        water_intake = weight * 35
    else:
        water_intake = weight * 31

    water_intake += water_intake * activity_coef
    water_intake = int(water_intake)

    return water_intake


async def get_nutritionix(query: str, application_id: str, api_key: str) -> int:
    """
    Получает информацию о калориях на основании запроса, используя API Nutritionix.

    Parameters
    ----------
    query : str
        Запрос, описывающий еду в свободной форме (например, '2 яблока').
    application_id : str
        ID приложения для API Nutritionix.
    api_key : str
        Ключ API для доступа к Nutritionix.

    Returns
    -------
    int
        Количество калорий для указанного запроса.
    """
    base_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    body = {
        'query': query
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


async def get_workout(activity: str, weight: int, duration: int, api_key: str) -> int:
    """
    Получает информацию о количестве сожжённых калорий на основе активности, веса и длительности.

    Parameters
    ----------
    activity : str
        Название активности (например, 'бег').
    weight : int
        Вес пользователя в килограммах.
    duration : int
        Длительность активности в минутах.
    api_key : str
        Ключ API для доступа к API Ninjas.

    Returns
    -------
    int
        Количество сожжённых калорий.
    """
    base_url = 'https://api.api-ninjas.com/v1/caloriesburned?'
    params = {
        'activity': activity,
        'weight': weight * 2.20462262,  # Конвертация веса в фунты
        'duration': duration
    }
    headers = {
        'X-Api-Key': api_key
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=base_url, headers=headers, params=params) as response:
            workout = await response.json()
            burned_calories = int(workout[0]['total_calories'])

    return burned_calories


async def translate_query(query: str) -> str:
    """
    Переводит запрос с русского языка на английский.

    Parameters
    ----------
    query : str
        Запрос на русском языке.

    Returns
    -------
    str
        Переведённый запрос на английский язык.
    """
    async with Translator() as translator:
        translated_query = await translator.translate(query, src='ru', dest='en')

    translated_query = translated_query.text

    return translated_query
