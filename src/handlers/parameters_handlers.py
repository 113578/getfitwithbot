from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from config.conifg import OPENWEATHERMAP_TOKEN
from src.states import ParametersState, UserState
from src.utils import (
    save_user_data,
    mifflin_st_jeor,
    calculate_water_intake,
    get_temperature
)

parameters_router = Router()

sex_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Мужской', callback_data='male')],
        [InlineKeyboardButton(text='Женский', callback_data='female')],
    ]
)


@parameters_router.message(Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext) -> None:
    """
    Начинает процесс настройки профиля пользователя.

    Parameters
    ----------
    message : Message
        Объект сообщения, содержащий команду '/set_profile'.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    await message.reply('Выберите свой пол', reply_markup=sex_keyboard)
    await state.set_state(ParametersState.sex)


@parameters_router.callback_query()
async def process_callback_query(callback_query, state: FSMContext) -> None:
    """
    Обрабатывает выбор пола пользователя через кнопки.

    Parameters
    ----------
    callback_query : CallbackQuery
        Запрос от нажатия кнопки.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    if callback_query.data == 'male':
        await callback_query.message.reply('Вы выбрали мужской пол')
        sex = 'male'
    elif callback_query.data == 'female':
        sex = 'female'
        await callback_query.message.reply('Вы выбрали женский пол')

    await state.update_data(sex=sex)
    await callback_query.message.reply('Введите свой вес (в кг)')
    await state.set_state(ParametersState.weight)


@parameters_router.message(ParametersState.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод веса пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с введённым весом.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        weight = int(message.text.strip())
        assert weight > 0, 'Вес не может быть отрицательным'
        assert weight >= 10, 'Слишком низкий вес'
        assert weight <= 200, 'Слишком тяжёлый вес'

        await state.update_data(weight=weight)
        await message.answer('Введите ваш рост (в см)')
        await state.set_state(ParametersState.height)

    except ValueError:
        await message.answer('Вес должен быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.height)
async def process_height(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод роста пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с введённым ростом.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        height = int(message.text.strip())
        assert height > 0, 'Рост не может быть отрицательным'
        assert height >= 100, 'Слишком низкий рост'
        assert height <= 250, 'Слишком высокий рост'

        await state.update_data(height=height)
        await message.answer('Введите ваш возраст')
        await state.set_state(ParametersState.age)

    except ValueError:
        await message.answer('Рост должен быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.age)
async def process_age(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод возраста пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с введённым возрастом.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        age = int(message.text.strip())
        assert age > 0, 'Возраст не может быть отрицательным'
        assert age >= 10, 'Слишком низкий возраст'
        assert age <= 100, 'Слишком высокий возраст'

        await state.update_data(age=age)
        await message.answer(
            'Насколько вы активны? Введите кол-во активных дней в неделю.\n\n'
            '- 0 - Нет активности;\n'
            '- 1-2 - Небольшая активность;\n'
            '- 3-5 - Средняя активность;\n'
            '- 6-7 - Высокая активность.'
        )
        await state.set_state(ParametersState.activity_level)

    except ValueError:
        await message.answer('Возраст должен быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.activity_level)
async def process_activity_level(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод уровня активности пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с уровнем активности.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        activity_level = int(message.text.strip())
        assert activity_level >= 0, 'Уровень активности не может быть отрицательным'
        assert activity_level <= 7, 'Уровень активности не может превышать неделю'

        await state.update_data(activity_level=activity_level)
        await message.answer(
            'В каком городе вы находитесь?\n'
            'Эта информация понадобится для расчёта потребления воды.'
        )
        await state.set_state(ParametersState.city)

    except ValueError:
        await message.answer('Уровень активности должен быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.city)
async def process_city(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод города пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с названием города.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        city = message.text.strip()
        assert city, 'Город должен быть заполнен'

        await state.update_data(city=city)

        user_data = await state.get_data()
        calories_needed = mifflin_st_jeor(
            sex=user_data.get('sex'),
            weight=user_data.get('weight'),
            height=user_data.get('height'),
            age=user_data.get('age'),
            activity_level=user_data.get('activity_level')
        )

        await message.answer(
            f'В покое вы тратите {calories_needed} ккал.\n\n'
            'Введите свою цель по калориям.\n\n'
            'Подсказка:\n'
            f'- {calories_needed + 250} ккал. для набора веса;\n'
            f'- {calories_needed - 250} ккал. для сброса веса.'
        )

        await state.set_state(ParametersState.calorie_goal)

    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.calorie_goal)
async def process_calorie_goal(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод цели по калориям пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с целью по калориям.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        calorie_goal = int(message.text.strip())
        assert calorie_goal > 0, 'Цель по калориям не может быть отрицательной'

        await state.update_data(calorie_goal=calorie_goal)

        user_data = await state.get_data()
        water_intake = calculate_water_intake(
            sex=user_data.get('sex'),
            weight=user_data.get('weight'),
            activity_level=user_data.get('activity_level')
        )
        temperature = await get_temperature(
            city=user_data.get('city'),
            api_key=OPENWEATHERMAP_TOKEN
        )

        if temperature >= 25:
            await message.answer(
                'Введите свою цель по воде.\n'
                f'Внимание! Сегодня жарко: в день вам необходимо {water_intake + 500} мл. воды.\n'
            )
        else:
            await message.answer(
                'Введите свою цель по воде.\n'
                f'Подсказка: в день вам необходимо {water_intake} мл. воды.'
            )

        await state.set_state(ParametersState.water_goal)

    except ValueError:
        await message.answer('Цель по калориям должна быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.water_goal)
async def process_calories_goal(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод цели по воде пользователя.

    Parameters
    ----------
    message : Message
        Сообщение пользователя с целью по воде.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    -------
    None
    """
    try:
        water_goal = int(message.text.strip())
        assert water_goal > 0, 'Цель по воде не может быть отрицательной'

        await state.update_data(water_goal=water_goal)

        user_data = await state.get_data()

        user_data = UserState(
            user_id=message.from_user.id,
            sex=user_data.get('sex'),
            weight=user_data.get('weight'),
            height=user_data.get('height'),
            age=user_data.get('age'),
            activity_level=user_data.get('activity_level'),
            city=user_data.get('city'),
            calorie_goal=user_data.get('calorie_goal'),
            water_goal=user_data.get('water_goal'),
            logged_water=0,
            logged_calories=0,
            burned_calories=0
        )

        save_user_data(user_data=user_data)

        summary = (
            'Ваш профиль:\n\n'
            f'Вес: {user_data.weight} кг\n'
            f'Рост: {user_data.height} см\n'
            f'Возраст: {user_data.age} лет\n'
            f'Активность: {user_data.activity_level} минут\n'
            f'Город: {user_data.city}\n'
            f'Цель по калориям: {user_data.calorie_goal} ккал\n'
            f'Цель по воде: {user_data.water_goal} мл'
        )

        await message.answer(summary)
        await state.clear()

    except ValueError:
        await message.answer('Цель по воде должна быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')
