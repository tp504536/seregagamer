#import aiocron
from aiogram import Bot, Dispatcher, executor,types
import logging

import keydoards
from keydoards import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()
bot = Bot(token="5971412217:AAG1tpPOeGsWvBdtKlDtst9tTevjJ3or2gg")
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

class FSMscrin(StatesGroup):
    get_scrin = State()



@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Добро пожаловать в первого бота телеграмм, который платит настоящие деньги за игру'
                         ' в бесплтаные игры на твоем телефоне.',reply_markup=main)


@dp.message_handler(content_types='text')
async def game(message:types.Message):
    if message.text == 'Играть':
        await message.answer( 'Задание на сегодня. \n\n' \
                       '🔥Скачать игру по данной ссылке из APP STORE - GOOGLE PLAY: '
                              'https://iguverse.com/download/r/znazqe49\n\n' \
                       'Завести себе бесплатного тамагочи, и собрать 60-100 ⚡️ энергии.\n\n' \
                       'Задания в игре:\n'\
                       '1. Поделится питомцем в инстаграм-тикток +50 энергии.\n' \
                       '2. Проверить других людей на наличие выполнения первого задания +20 энергии.\n' \
                       '3. Перепрыгивать кактусы, +15 энергии.\n' \
                       '4. Пройти 1км +15 энергии.\n\n ' \
                       'Цель задания собирать от 60 энергии в день, вознаграждение за данное задание 150р 🤑',
                          reply_markup=get_active)
    elif message.text == 'Как получить деньги за игру':
        await message.answer('Мы предоставляем вам игры, за действия в которых нам платят денежные средства,'
                             ' часть из которых, мы даем вам в виде вознаграждения за действия🔥\n\n'
                             'За одну игру мы начисляем 150р ( 2.5$ )🤑 в сутки,'
                             'на данный момент проходить задание можно только один раз в сутки!\n\n'
                             'Для того что-бы играть, нажмите на кнопку «играть» расположенную в меню бота, '
                             'начисление денежных средств происходит в ручную, после проверки выполнения вами заданий.\n\n'
                             ' Вывод денежных средств доступен на QIWI, и карты рф-укр.')




@dp.callback_query_handler(text='check')
async def no_date(call: types.CallbackQuery,state: FSMContext):
    await call.message.answer('Отправьте скрин собранной энергии за сегодня')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.set_state(FSMscrin.get_scrin)

@dp.message_handler(content_types='text', state=FSMscrin.get_scrin.state)
async def scrinshot(message: types.Message, state: FSMContext):
    async with state.proxy() as spam:
        spam['text'] = message.text
        await state.finish()
        print(spam['text'])
        await message.answer("Отправить",reply_markup=scrin)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)