# import aiocron
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
import logging
from sql import Database
import keydoards
from keydoards import *
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()
bot = Bot(token="5971412217:AAG1tpPOeGsWvBdtKlDtst9tTevjJ3or2gg")
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


class Spam(StatesGroup):
    get_spam = State()



@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if not db.users(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer('Добро пожаловать в первого бота телеграмм, который платит настоящие деньги за игру'
                         ' в бесплтаные игры на твоем телефоне.', reply_markup=main)


@dp.message_handler(commands='admin')
async def cmd_admin(message: types.Message):
    if message.from_user.id != 1912165183:
        await message.answer('Сударь а не пошли бы вы на хуй!')
    else:
        await message.answer('Доброго времени суток!', reply_markup=admin)


@dp.message_handler(content_types='text')
async def game(message: types.Message, state: FSMContext):
    if message.text == 'Играть':
        await message.answer('Задание на сегодня. \n\n' \
                             '🔥Скачать игру по данной ссылке из APP STORE - GOOGLE PLAY: '
                             '<a href="https://iguverse.com/download/r/znazqe49">ссылка</a>\n\n' \
                             'Завести себе бесплатного тамагочи, и собрать 60-100 ⚡️ энергии.\n\n' \
                             'Задания в игре:\n' \
                             '1. Поделится питомцем в инстаграм-тикток +50 энергии.\n' \
                             '2. Проверить других людей на наличие выполнения первого задания +20 энергии.\n' \
                             '3. Перепрыгивать кактусы, +15 энергии.\n' \
                             '4. Пройти 1км +15 энергии.\n\n ' \
                             'Цель задания собирать от 60 энергии в день, вознаграждение за данное задание 150р 🤑\n'
                             'После выполнения задания, нажмите кнопку проверить задание',
                             reply_markup=get_active, parse_mode='html')
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
        await message.answer(
            'Ваш баланс ' + str(money).replace('[', '').replace(']', '').replace('(', '').replace(')', '')
            .replace('\'', '').replace(',', '') + "\n\n Вывод производится на карту банка или Qiwi",
            reply_markup=out_money)

    elif message.text == 'Вывод':
        await message.answer("Введите сумму")
        await state.set_state(Money.sum)

    elif message.text == "Главное меню":
        await message.answer('Вы вернулись в гавное меню', reply_markup=main)

    elif message.text == 'Users-menu':
        await message.answer('Вы вернулись в пользовательское меню', reply_markup=main)
    elif message.text == 'Статистика🗒️':
        len_users = db.lenuser()
        await message.answer('В бота заходило ' + str(len_users))
    elif message.text == 'Рассылка📤':
        await message.answer('Введите текск')
        await state.set_state(Spam.get_spam)


@dp.callback_query_handler(text='check')
async def no_date(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Отправьте скрин собранной энергии за сегодня')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await state.set_state(FSMscrin.get_scrin)


@dp.message_handler(content_types='photo', state=FSMscrin.get_scrin.state)
async def scrinshot(message: types.Message, state: FSMContext):
    global photo
    async with state.proxy() as photo:
        photo['photo'] = message.photo[0].file_id
        await state.finish()
        await message.answer("Отправить скрин", reply_markup=scrin)


@dp.message_handler(content_types='text', state=Money.sum.state)
async def sum(message: types.Message, state: FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        if text['text'].isdigit():
            await message.answer(
                'Введите номер карты или номер Qiwi\n\n Пример:\nCard 1111 1111 1111 1111 \nQiwi 79045530327')
            await state.set_state(Money.card)
        else:
            await message.answer('Походу вы ошиблись! Попробуйте снова.',reply_markup=main)

@dp.message_handler(content_types='text', state=Money.card.state)
async def card(message: types.Message, state: FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        if text['text'].isdigit():
            check = db.balance(message.from_user.id)
            print(check)
            check = str(check).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('\'',
                                        '').replace(',', '')
            if int(check) < 500:
                await message.answer("У вас не достаточно средств")
            else:
                await message.answer('Ваш вывод в обработке')
        else:
            await message.answer('Походу вы ошиблись! Попробуйте снова.',reply_markup=main)


@dp.callback_query_handler(text='send')
async def get_send(call: types.CallbackQuery):
    global uid
    uid = call.from_user.id
    await call.bot.send_photo(chat_id='1912165183', photo=photo['photo'], caption=str(uid), reply_markup=admin_update)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='out')
async def get_out(call: types.CallbackQuery):
    await call.message.answer('Вы отменили отправку ')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='ok')
async def ok(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Send.get_send)
    await call.message.answer("Введи id")


@dp.message_handler(content_types='text', state=Send.get_send.state)
async def get_senc(message: types.Message, state: FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        await message.answer('Вы начислили баланс')
        db.balance_update(text['text'])
        await bot.send_message(text['text'], 'На ваш кошелек поуступили денежные средства')


@dp.callback_query_handler(text='no')
async def no(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Send.get_out)
    await call.message.answer("Введи id")


@dp.message_handler(content_types='text', state=Send.get_out.state)
async def get_senc(message: types.Message, state: FSMContext):
    async with state.proxy() as text:
        text['text'] = message.text
        await state.finish()
        await message.answer('Вы отменили')
        await bot.send_message(text['text'], 'Вы не выполнили задание')

@dp.message_handler(content_types='text', state=Spam.get_spam.state)
async def spam(message: types.Message, state: FSMContext):
    global spam
    async with state.proxy() as spam:
        spam['text'] = message.text
        await state.finish()
        await message.answer(
            'Ваш текст для расскылки: ' + spam['text'],reply_markup=admin_spam)


@dp.callback_query_handler(text='spam_all')
async def no_date(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer('Отлично,начинаю рассылку')
    all_users = db.all_user()
    for i in all_users:
        try:
            await bot.send_message(i[0], spam['text'])
            await sleep(0.33)
        except Exception:
            pass
    await call.message.answer('Рассылка выполнена.')


@dp.callback_query_handler(text='cancel')
async def no(call: types.CallbackQuery):
    await call.message.answer("Вы отменил расслыку")
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
