from aiogram.types import InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True)
mooney = KeyboardButton('Как получить деньги за игру')
game = KeyboardButton('Играть')
pay = KeyboardButton('Кошелек')
main.add(mooney).add(game).add(pay)

admin = ReplyKeyboardMarkup(resize_keyboard=True)
stat = KeyboardButton('Статистика🗒️')
spam = KeyboardButton('Рассылка📤')
users_menu =KeyboardButton('Users-menu')
admin.add(stat).add(spam).add(users_menu)


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

out_money = ReplyKeyboardMarkup(resize_keyboard=True)
send_out = KeyboardButton('Вывод')
back = KeyboardButton('Главное меню')
out_money.add(send_out).add(back)

admin_spam = InlineKeyboardMarkup(row_width=2)
spam_all = InlineKeyboardButton('Spam', callback_data='spam_all')
cancel = InlineKeyboardButton('Cancel', callback_data='cancel')
admin_spam.add(spam_all).add(cancel)