#import aiocron
from aiogram import Bot, Dispatcher, executor,types
import logging
from sql import Database
import keydoards
from keydoards import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()
bot = Bot(token="5824546211:AAHT0YJk7mqKjCTWC6lzC4rFclKTOJJ63Gg")
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

db = Database('base')

class FSMscrin(StatesGroup):
    get_scrin = State()

class Money(StatesGroup):
    sum = State()
    card = State()

class Send(StatesGroup):
    get_send = State()
    get_out = State()

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if not db.users(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer('Добро пожаловать в первого бота телеграмм, который платит настоящие деньги за игру'
                         ' в бесплтаные игры на твоем телефоне.',reply_markup=main)


@dp.message_handler(content_types='text')
async def game(message:types.Message, state: FSMContext):
    if message.text == 'Играть':
        await message.answer( 'Задание на сегодня. \n\n' \
                       '🔥Скачать игру по данной ссылке из APP STORE - GOOGLE PLAY: '
                              '<a href="https://iguverse.com/download/r/znazqe49">ссылка</a>\n\n' \
                       'Завести себе бесплатного тамагочи, и собрать 60-100 ⚡️ энергии.\n\n' \
                       'Задания в игре:\n'\
                       '1. Поделится питомцем в инстаграм-тикток +50 энергии.\n' \
                       '2. Проверить других людей на наличие выполнения первого задания +20 энергии.\n' \
                       '3. Перепрыгивать кактусы, +15 энергии.\n' \
                       '4. Пройти 1км +15 энергии.\n\n ' \
                       'Цель задания собирать от 60 энергии в день, вознаграждение за данное задание 150р 🤑\n'
                              'После выполнения задания, нажмите кнопку проверить задание',
                          reply_markup=get_active,parse_mode='html')
    elif message.text == 'Как получить деньги за игру':
        await message.answer('Мы предоставляем вам игры, за действия в которых нам платят денежные средства,'
                             ' часть из которых, мы даем вам в виде вознаграждения за действия🔥\n\n'
                             'За одну игру мы начисляем 150р ( 2.5$ )🤑 в сутки,'
                             'на данный момент проходить задание можно только один раз в сутки!\n\n'
                             'Для того что-бы играть, нажмите на кнопку «играть» расположенную в меню бота, '
                             'начисление денежных средств происходит в ручную, после проверки выполнения вами заданий.\n\n'
                             ' Вывод денежных средств доступен на QIWI, и карты рф-укр.')

    elif message.text == 'Кошелек':
        money = db.balance(message.chat.id)
        await message.answer('Ваш баланс ' + str(money).replace('[','').replace(']','').replace('(','').replace(')','')
                             .replace('\'','').replace(',','') + "\n\n Вывод производится на карту банка или Qiwi",reply_markup=out_money)

    elif message.text == 'Вывод':
        await message.answer("Введите сумму")
        await state.set_state(Money.sum)

    elif message.text == "Главное меню":
        await message.answer('Вы вернулись в гавное меню',reply_markup=main)

@dp.callback_query_handler(text='check')
async def no_date(call: types.CallbackQuery,state: FSMContext):
    await call.message.answer('Отправьте скрин собранной энергии за сегодня')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.set_state(FSMscrin.get_scrin)

@dp.message_handler(content_types='photo', state=FSMscrin.get_scrin.state)
async def scrinshot(message: types.Message, state: FSMContext):
    global photo
    #global uid
    async with state.proxy() as photo:
        photo['photo'] = message.photo[0].file_id
        await state.finish()
        uid = message.from_user.id
        await message.answer("Отправить скрин",reply_markup=scrin)



@dp.message_handler(content_types='text', state=Money.sum.state)
async def sum(message: types.Message, state: FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        await message.answer('Введите номер карты или номер Qiwi\n\n Пример:\nCard 1111 1111 1111 1111 \nQiwi 79045530327')
        await state.set_state(Money.card)


@dp.message_handler(content_types='text',state=Money.card.state)
async def card(message: types.Message, state : FSMContext):
    async with state.proxy() as text:
        text['text'] =message.text
        await state.finish()
        check = db.balance(message.from_user.id)
        print(check)
        check=str(check).replace('[','').replace(']','').replace('(','').replace(')','').replace('\'','').replace(',','')
        if int(check) < 500:
            await message.answer("У вас не достаточно средств")
        else:
            await message.answer('Ваш вывод в обработке')


@dp.callback_query_handler(text='send')
async def get_send(call: types.CallbackQuery):
    global uid
    uid = call.from_user.id
    await call.bot.send_photo(chat_id='1226644704',photo=photo['photo'],caption=str(uid),reply_markup=admin_update)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)



@dp.callback_query_handler(text='out')
async def get_out(call: types.CallbackQuery):
    await call.message.answer('Вы отменили отправку ')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='ok')
async def ok(call: types.CallbackQuery,state: FSMContext):
    await state.set_state(Send.get_send)
    await call.message.answer("Введи id")

@dp.message_handler(content_types='text',state=Send.get_send.state)
async def get_senc(message: types.Message, state : FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        await message.answer('Вы начислили баланс')
        db.balance_update(text['text'])
        await bot.send_message(text['text'] , 'На ваш кошелек поуступили денежные средства')


@dp.callback_query_handler(text='no')
async def no(call: types.CallbackQuery,state: FSMContext):
    await state.set_state(Send.get_out)
    await call.message.answer("Введи id")

@dp.message_handler(content_types='text', state=Send.get_out.state)
async def get_senc(message: types.Message, state: FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        await message.answer('Вы отменили')
        await bot.send_message(text['text'], 'Вы не выполнили задание')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)