from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config.conifg import OPENWEATHERMAP_TOKEN
from src.utils import (
    load_user_data,
    get_temperature,
    mifflin_st_jeor,
    calculate_water_intake
)


general_router = Router()


@general_router.message(Command('start'))
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду '/start' и отправляет приветственное сообщение.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/start'.

    Returns
    -------
    None
    """
    await message.reply(
        'Привет! Я помогу вам прийти в форму.\n'
        'Введите /help для получения доступных команд.\n'
        'Введите /set_profile для первоначальной настройки профиля.'
    )


@general_router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    """
    Обрабатывает команду '/help' и отправляет список доступных команд.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/help'.

    Returns
    -------
    None
    """
    await message.reply(
        'Доступные команды:\n'
        '/set_profile - Настройка профиля пользователя\n'
        '/list_profile - Просмотр профиля пользователя\n'
        '/calculate - Расчёт дневной нормы\n'
        '/log_water <кол-во, мл.> - Отслеживание воды\n'
        '/log_food <еда и кол-во еды в свободной форме> - Отслеживание еды\n'
        '/log_workout <тип тренировки> <продолжительность, мин.>- Отслеживание тренировок\n'
        '/check_progress - Прогресс\n'
        '/temperature - Получение температуры в вашем городе'
    )


@general_router.message(Command('list_profile'))
async def cmd_list_profile(message: Message) -> None:
    """
    Обрабатывает команду '/list_profile' и отправляет информацию о профиле пользователя.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/list_profile'.

    Returns
    -------
    None
    """
    user_id = message.from_user.id
    user_data = load_user_data(user_id=user_id)

    summary = (
        'Ваш профиль:\n\n'
        f'Вес: {user_data.weight} кг\n'
        f'Рост: {user_data.height} см\n'
        f'Возраст: {user_data.age} лет\n'
        f'Активность: {user_data.activity_level} минут\n'
        f'Город: {user_data.city}\n'
        f'Цель по калориям: {user_data.calorie_goal} ккал\n'
        f'Цель по воде: {user_data.water_goal} мл\n'
    )

    await message.reply(summary)


@general_router.message(Command('calculate'))
async def cmd_calculate(message: Message) -> None:
    """
    Обрабатывает команду '/calculate' и рассчитывает дневную норму калорий и воды для пользователя.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/calculate'.

    Returns
    -------
    None
    """
    user_id = message.from_user.id
    user_data = load_user_data(user_id=user_id)

    calories_needed = mifflin_st_jeor(
        sex=user_data.sex,
        weight=user_data.weight,
        height=user_data.height,
        age=user_data.age,
        activity_level=user_data.activity_level
    )
    water_intake = calculate_water_intake(
        sex=user_data.sex,
        weight=user_data.weight,
        activity_level=user_data.activity_level
    )

    await message.reply(
        f'В покое вы тратите {calories_needed} ккал в день.\n'
        f'В день вам необходимо {water_intake} мл воды.'
    )


@general_router.message(Command('temperature'))
async def cmd_temperature(message: Message) -> None:
    """
    Обрабатывает команду '/temperature' и отправляет текущую температуру в городе пользователя.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/temperature'.

    Returns
    -------
    None
    """
    user_id = message.from_user.id
    user_data = load_user_data(user_id=user_id)
    city = user_data.city

    temperature = await get_temperature(
        city=city,
        api_key=OPENWEATHERMAP_TOKEN
    )
    if temperature >= 25:
        await message.reply(
            f'Температура в городе {city}: {temperature}°C.\n'
            'Жарко, сконцентрируйтесь на потреблении воды!'
        )
    else:
        await message.reply(
            f'Температура в городе {city}: {temperature}°C.\n'
            'Дополнительного потребления воды не нужно.'
        )
