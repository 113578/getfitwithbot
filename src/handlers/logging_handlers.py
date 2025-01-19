from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from config.conifg import (
    NUTRITIONIX_ID,
    NUTRITIONIX_TOKEN,
    APININJAS_TOKEN
)
from src.utils import (
    load_user_data,
    save_user_data,
    get_nutritionix,
    get_workout,
    translate_query
)


logging_router = Router()


@logging_router.message(Command('log_water'))
async def cmd_log_water(message: Message, command: CommandObject) -> None:
    """
    Обрабатывает команду '/log_water' для отслеживания количества потреблённой воды.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/log_water'.
    command : CommandObject
        Объект команды, содержащий аргументы (количество воды в мл).

    Returns
    -------
    None
    """
    try:
        water_amount = int(command.args)
        assert water_amount > 0, 'Кол-во воды не может быть отрицательным'

        user_data = load_user_data(user_id=message.from_user.id)
        user_data.logged_water += water_amount
        save_user_data(user_data=user_data)

        if user_data.water_goal > user_data.logged_water:
            await message.reply(
                f'Добавлено: {water_amount} мл воды.\n'
                f'До достижения цели осталось {user_data.water_goal - user_data.logged_water} мл.'
            )
        else:
            await message.reply(
                f'Добавлено: {water_amount} мл воды. Вы достигли дневной цели!'
            )

    except (ValueError, TypeError):
        await message.answer('Кол-во воды должно быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@logging_router.message(Command('log_food'))
async def cmd_log_food(message: Message, command: CommandObject) -> None:
    """
    Обрабатывает команду '/log_food' для отслеживания потреблённой еды и калорий.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/log_food'.
    command : CommandObject
        Объект команды, содержащий аргументы (описание еды в свободной форме).

    Returns
    -------
    None
    """
    try:
        query = command.args
        assert query is not None, 'Запрос не может быть пустым'

        translated_query = await translate_query(query=query)

        calories = await get_nutritionix(
            query=translated_query,
            application_id=NUTRITIONIX_ID,
            api_key=NUTRITIONIX_TOKEN
        )

        user_data = load_user_data(user_id=message.from_user.id)
        user_data.logged_calories += calories
        save_user_data(user_data=user_data)

        if user_data.calorie_goal > user_data.logged_calories:
            await message.reply(
                f'Добавлено: {calories} ккал.\n'
                f'До достижения цели осталось {user_data.calorie_goal - user_data.logged_calories} ккал.'
            )
        else:
            await message.reply(
                f'Добавлено: {calories} ккал. Вы достигли дневной цели!'
            )

    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@logging_router.message(Command('log_workout'))
async def cmd_log_workout(message: Message, command: CommandObject) -> None:
    """
    Обрабатывает команду '/log_workout' для отслеживания тренировок и сжигания калорий.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/log_workout'.
    command : CommandObject
        Объект команды, содержащий аргументы (тренировка и длительность).

    Returns
    -------
    None
    """
    try:
        activity, duration = command.args.split()
        duration = int(duration)

        assert activity is not None, 'Запрос не должен быть пустым'
        assert duration > 0, 'Длительность должна быть положительным числом'

        translate_activity = await translate_query(query=activity)

        user_data = load_user_data(user_id=message.from_user.id)

        burned_calories = await get_workout(
            activity=translate_activity,
            weight=user_data.weight,
            duration=duration,
            api_key=APININJAS_TOKEN
        )

        user_data.burned_calories += burned_calories
        user_data.logged_calories -= burned_calories

        save_user_data(user_data=user_data)

        if user_data.calorie_goal > user_data.logged_calories:
            await message.reply(
                f'Сожжено: {burned_calories} ккал.\n'
                f'До достижения цели осталось {user_data.calorie_goal - user_data.logged_calories} ккал.'
            )
        else:
            await message.reply(
                f'Сожжено: {burned_calories} ккал. Вы достигли дневной цели!'
            )

    except (ValueError, TypeError):
        await message.answer('Значения должны быть в виде <тренировка> <продолжительность, мин.>')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@logging_router.message(Command('check_progress'))
async def cmd_check_progress(message: Message) -> None:
    """
    Обрабатывает команду '/check_progress' для отображения прогресса пользователя по воде и калориям.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/check_progress'.

    Returns
    -------
    None
    """
    user_data = load_user_data(user_id=message.from_user.id)

    await message.reply(
        '📊 Прогресс:\n\n'
        'Вода:\n'
        f'- Выпито: {user_data.logged_water} мл. из {user_data.water_goal} мл.\n'
        f'- Осталось: {user_data.water_goal - user_data.logged_water} мл.\n'
        'Калории:\n'
        f'- Потреблено: {user_data.logged_calories} ккал. из {user_data.calorie_goal} ккал.\n'
        f'- Сожжено: {user_data.burned_calories} ккал.\n'
        f'- Осталось: {user_data.calorie_goal - user_data.logged_calories} ккал.\n'
    )
