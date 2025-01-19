from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config.conifg import OPENWEATHERMAP_TOKEN
from src.utils import load_user_info, get_temperatures


general_router = Router()


@general_router.message(Command('start'))
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду '/start' и отправляет приветственное сообщение.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/start'.

    Returns
    --------
    None
    """
    await message.reply(
        'Привет! Я помогу вам прийти в форму.\n'
        'Введите /help для получения доступных команд.'
    )


@general_router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    """
    Обрабатывает команду '/help' и отправляет список доступных команд.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/help'.

    Returns
    --------
    None
    """
    await message.reply(
        'Доступные команды:\n'
        '/set_profile - Настройка профиля пользователя\n'
        '/list_profile - Просмотр профиля пользователя\n'
        '/calculate - Расчёт дневной нормы\n'
        '/log_water <кол-во, мл.> - Отслеживание воды\n'
        '/log_food <еда и кол-во еды в свободной форме> - Отслеживание еды\n'
        '/log_workout - Отслеживание тренировок\n'
        '/check_progress - Прогресс\n'
        '/temperature - Получение температуры в вашем городе'
    )


@general_router.message(Command('list_profile'))
async def cmd_list_profile(message: Message) -> None:
    """
    Обрабатывает команду '/list_profile' и отправляет информацию о профиле пользователя.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/list_profile'.

    Returns
    --------
    None
    """
    user_id = message.from_user.id
    user_info = load_user_info(user_id=user_id)

    summary = (
        'Ваш профиль:\n\n'
        f'Вес: {user_info.weight} кг\n'
        f'Рост: {user_info.height} см\n'
        f'Возраст: {user_info.age} лет\n'
        f'Активность: {user_info.activity_level} минут\n'
        f'Город: {user_info.city}\n'
        f'Цель по калориям: {user_info.calorie_goal} ккал\n'
        f'Цель по воде: {user_info.water_goal} мл\n'
    )

    await message.reply(summary)


@general_router.message(Command('temperature'))
async def cmd_temperature(message: Message) -> None:
    """
    Обрабатывает команду '/temperature' и отправляет текущую температуру в городе пользователя.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/temperature'.

    Returns
    --------
    None
    """
    user_id = message.from_user.id
    user_info = load_user_info(user_id=user_id)
    city = user_info.city

    temperature = await get_temperatures(
        city=city,
        api_key=OPENWEATHERMAP_TOKEN
    )

    await message.reply(f'Температура в городе {city}: {temperature}°C')
