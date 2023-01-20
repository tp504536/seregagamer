from aiogram.types import InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)
mooney = KeyboardButton('Как получить деньги за игру')
game = KeyboardButton('Играть')
pay = KeyboardButton('Кошелек')
main.add(mooney).add(game).add(pay)

get_active = InlineKeyboardMarkup(row_width=2)
stories_in = InlineKeyboardButton('Проверить выполнения задания',callback_data='check')
get_active.add(stories_in)

scrin = InlineKeyboardMarkup(row_width=2)
send = InlineKeyboardButton('Отправить',callback_data='send')
out = InlineKeyboardButton('Отменить',callback_data='out')
scrin.add(send).add(out)

admin_update = InlineKeyboardMarkup(row_width=2)
ok = InlineKeyboardButton('Подтвердить',callback_data='ok')
no = InlineKeyboardButton('Отбой', callback_data='no')
admin_update.add(ok).add(no)