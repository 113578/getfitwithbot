from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from config.conifg import (
    NUTRITIONIX_ID,
    NUTRITIONIX_TOKEN
)
from src.utils import (
    load_user_info,
    save_user_info,
    get_nutritionix
)


logging_router = Router()


@logging_router.message(Command('log_water'))
async def cmd_log_water(message: Message, command: CommandObject) -> None:
    """
    Обрабатывает команду '/log_water' для отслеживания количества потреблённой воды.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/log_water'.
    command : CommandObject
        Объект команды, содержащий аргументы (количество воды в мл).

    Returns
    --------
    None
    """
    try:
        water_amount = int(command.args)
        assert water_amount > 0, 'Кол-во воды не может быть отрицательным'

        user_info = load_user_info(user_id=message.from_user.id)
        user_info.logged_water += water_amount
        save_user_info(user_info=user_info)

        if user_info.water_goal > user_info.logged_water:
            await message.reply(
                f'Добавлено: {water_amount} мл воды.\n'
                f'До достижения цели осталось {user_info.water_goal - user_info.logged_water} мл.'
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
    ------------
    message : Message
        Объект сообщения, содержащий команду '/log_food'.
    command : CommandObject
        Объект команды, содержащий аргументы (описание еды в свободной форме).

    Returns
    --------
    None
    """
    try:
        query = command.args
        assert query is not None, 'Запрос не может быть пустым'

        calories = await get_nutritionix(
            query=query,
            application_id=NUTRITIONIX_ID,
            api_key=NUTRITIONIX_TOKEN
        )

        user_info = load_user_info(user_id=message.from_user.id)
        user_info.logged_calories += calories
        save_user_info(user_info=user_info)

        if user_info.calorie_goal > user_info.logged_calories:
            await message.reply(
                f'Добавлено: {calories} ккал.\n'
                f'До достижения цели осталось {user_info.calorie_goal - user_info.logged_calories} ккал.'
            )
        else:
            await message.reply(
                f'Добавлено: {calories} ккал. Вы достигли дневной цели!'
            )

    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@logging_router.message(Command('check_progress'))
async def cmd_check_progress(message: Message) -> None:
    """
    Обрабатывает команду '/check_progress' для отображения прогресса пользователя по воде и калориям.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/check_progress'.

    Returns
    --------
    None
    """
    user_info = load_user_info(user_id=message.from_user.id)

    await message.reply(
        '📊 Прогресс:\n\n'
        'Вода:\n'
        f'- Выпито: {user_info.logged_water} мл. из {user_info.water_goal} мл.\n'
        f'- Осталось: {user_info.water_goal - user_info.logged_water} мл.\n'
        'Калории:\n'
        f'- Потреблено: {user_info.logged_calories} ккал. из {user_info.calorie_goal} ккал.\n'
        f'- Сожжено: 228 ккал.\n'
        f'- Осталось: {user_info.calorie_goal - user_info.logged_calories} ккал.\n'
    )
