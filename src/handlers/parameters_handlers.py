from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.states import ParametersState, UserState
from src.utils import save_user_info


parameters_router = Router()


@parameters_router.message(Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext) -> None:
    """
    Начинает процесс настройки профиля пользователя.

    Parameters
    ------------
    message : Message
        Объект сообщения, содержащий команду '/set_profile'.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    await message.reply('Введите ваш вес (в кг)')
    await state.set_state(ParametersState.weight)


@parameters_router.message(ParametersState.weight)
async def process_weight(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод веса пользователя.

    Parameters
    ------------
    message : Message
        Сообщение пользователя с введённым весом.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
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
    ------------
    message : Message
        Сообщение пользователя с введённым ростом.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
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
    ------------
    message : Message
        Сообщение пользователя с введённым возрастом.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    try:
        age = int(message.text.strip())
        assert age > 0, 'Возраст не может быть отрицательным'
        assert age >= 10, 'Слишком низкий возраст'
        assert age <= 100, 'Слишком высокий возраст'

        await state.update_data(age=age)
        await message.answer('Сколько минут активности у вас в день?')
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
    ------------
    message : Message
        Сообщение пользователя с уровнем активности.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    try:
        activity_level = int(message.text.strip())
        assert activity_level > 0, 'Уровень активности не может быть отрицательным'
        assert activity_level <= 1440, 'Уровень активности не может превышать один день'

        await state.update_data(activity_level=activity_level)
        await message.answer('В каком городе вы находитесь?')
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
    ------------
    message : Message
        Сообщение пользователя с названием города.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    try:
        city = message.text.strip()
        assert city, 'Город должен быть заполнен'

        await state.update_data(city=city)
        await message.answer('Введите свою цель по калориям')
        await state.set_state(ParametersState.calorie_goal)

    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.calorie_goal)
async def process_calorie_goal(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает ввод цели по калориям пользователя.

    Parameters
    ------------
    message : Message
        Сообщение пользователя с целью по калориям.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    try:
        calorie_goal = int(message.text.strip())
        assert calorie_goal > 0, 'Цель по калориям не может быть отрицательной'

        await state.update_data(calorie_goal=calorie_goal)
        await message.answer('Введите свою цель по воде')
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
    ------------
    message : Message
        Сообщение пользователя с целью по воде.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    try:
        water_goal = int(message.text.strip())
        assert water_goal > 0, 'Цель по воде не может быть отрицательной'

        await state.update_data(water_goal=water_goal)
        await state.set_state(ParametersState.saving_parameters)

    except ValueError:
        await message.answer('Цель по воде должна быть числовым значением! Попробуйте ещё раз.')
    except AssertionError as e:
        await message.answer(f'{e}! Попробуйте ещё раз.')


@parameters_router.message(ParametersState.saving_parameters)
async def process_saving_parameters(message: Message, state: FSMContext) -> None:
    """
    Сохраняет параметры профиля пользователя.

    Parameters
    ------------
    message : Message
        Сообщение пользователя.
    state : FSMContext
        Контекст состояния конечного автомата.

    Returns
    --------
    None
    """
    user_data = await state.get_data()

    user_info = UserState(
        user_id=message.from_user.id,
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

    save_user_info(user_info=user_info)

    summary = (
        'Ваш профиль:\n\n'
        f'Вес: {user_info.weight} кг\n'
        f'Рост: {user_info.height} см\n'
        f'Возраст: {user_info.age} лет\n'
        f'Активность: {user_info.activity_level} минут\n'
        f'Город: {user_info.city}\n'
        f'Цель по калориям: {user_info.calorie_goal} ккал\n'
        f'Цель по воде: {user_info.water_goal} мл'
    )

    await message.answer(summary)
    await state.clear()
