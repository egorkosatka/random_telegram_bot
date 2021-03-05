from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,\
    KeyboardButton, ReplyKeyboardMarkup

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import random
import vk_api
import sqlite3
import asyncio
import datetime

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

date = datetime.datetime.now()
date_now = f'{date.year}-{date.month}-{date.day}'


bot = Bot(token='my bot token')
dp = Dispatcher(bot, storage=MemoryStorage())
vk_session = vk_api.VkApi('my telephone number', 'my password')
vk_session.auth()

vk = vk_session.get_api()

admins = []
participants = []

premium_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('уведомления🔔'), KeyboardButton('подписка🎁')).add(
    KeyboardButton('игры🕹')).add(
    KeyboardButton('рынок🛒')
)

game_bar_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('орел и решка👑'),
    KeyboardButton('да или нет✨')).add(
    KeyboardButton('камень ножницы бумага✂')).add(
    KeyboardButton('◀Меню')
)

standart_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Купить прем👑'))

try:
    cursor.execute('''ALTER TABLE user ADD subscription_date STRING''')
    conn.commit()
    cursor.execute('''ALTER TABLE user ADD concurses INT''')
    conn.commit()
    cursor.execute('''ALTER TABLE user ADD walls INT''')
    conn.commit()

    cursor.execute('''ALTER TABLE user ADD push INT''')
    conn.commit()
    cursor.execute('''ALTER TABLE user ADD subscription INT''')
    conn.commit()
    cursor.execute('''ALTER TABLE user ADD main INT''')
    conn.commit()
    cursor.execute('''CREATE TABLE user(telegram_id UNIQUE, attempts INT, rated INT, main INT, subscription INT, push INT, concurses INT, walls INT, subscription_date STRING)''')
    conn.commit()
except:
    pass


class Form(StatesGroup):
    sos = State()




@dp.message_handler(commands=['start', 'command', 'help'])
async def other_message(ms: types.Message):
    cursor.execute(f'''INSERT OR IGNORE INTO user(telegram_id, attempts, rated, main, subscription, push, concurses, walls) VALUES ({ms.from_user.id}, 0, 0, 1, 0, 0, 0, 5)''')
    subscription_status = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
    conn.commit()
    if subscription_status == 0:
        await bot.send_message(ms.from_user.id, 'Hi!', reply_markup=standart_keyboard)
        await bot.send_message(ms.from_user.id, '✅Привет, ты можешь отправлять боту следующие запросы: \n\n'

                                                '🎲Рандомайзер\n'
                                                '└/random 1 2 3 4 - отправьте боту данные, разделённые пробелом, и он выберет случайное значение из списка!\n'
                                                '└random hello - ты можешь отправить слово, и он выберет случайную букву!\n\n'
                                                
                                                
                                                '📁отправляй боту файлы!\n'
                                                '└Отправь боту файл со словами, и он выберет случайное слово!\n\n'
                                                
                                                '💬Комментарии\n'
                                                '└/vk domen post_id - отправьте боту запрос, состоящий из короткого имени автора поста, и из id поста, и он выберет случайный комментарий!\n\n'
                                                
                                                
                                                '❓Задай боту вопрос!\n'
                                                '└Бот, ты правда бот?\n'
                                                '└❗️Пишите в конце вопроса "?", иначе бот распознает это как фразу!\n\n'
                                                
                                                
                                                '🏞Оценка фото\n'
                                                '└Отправь боту любое фото(не как документ) и он его оценит!\n\n\n'
                                                
                                                
                                                
                                                '🌟🌟🌟ПОДПИСКА🌟🌟🌟\n\n'
                                                
                                                '💵что даёт обычная подписка?\n'
                                                '└Доступ к минииграм🕹\n'
                                                '└доступ к управлению уведомлениями🔔\n\n'
                                                
                                                '🎁что даёт сверхпрем подписка?\n'
                                                '└Безлимит на посты в ВК🌄\n'
                                                '└Подписка действует год, а не месяц, как обычная🎟\n'
                                                '└Безлимит на обьём отправляемых файлов📁\n\n'
                                                
                                                'PS.\n'
                                                '└Ваш стартовый баланс:\n'
                                                ' └Посты вк: 55️⃣\n'
                                                ' └Обьём отправляемого файла: до 30 слов3️⃣0️⃣\n'
                                                ' └можно прислать лишь 10 фото1️⃣0️⃣\n',
                                                reply_markup=InlineKeyboardMarkup().add(
                                                    InlineKeyboardButton('Оформить премиум👑', callback_data='oform_premium')
                                                ).add(
                                                    InlineKeyboardButton('Написать в поддержку🆘', callback_data='nap_podderj')
                                                ))

    if subscription_status in [1, 2]:
        await bot.send_message(ms.from_user.id, '✅Привет, ты можешь отправлять боту следующие запросы: \n\n'

                                                '🎲Рандомайзер\n'
                                                '└/random 1 2 3 4 - отправьте боту данные, разделённые пробелом, и он выберет случайное значение из списка!\n'
                                                '└random hello - ты можешь отправить слово, и он выберет случайную букву!\n\n'
                                                
                                                
                                                '📁отправляй боту файлы!\n'
                                                '└Отправь боту файл со словами, и он выберет случайное слово!\n\n'
                                                
                                                '💬Комментарии\n'
                                                '└/vk domen post_id - отправьте боту запрос, состоящий из короткого имени автора поста, и из id поста, и он выберет случайный комментарий!\n\n'
                                                
                                                
                                                '❓Задай боту вопрос!\n'
                                                '└Бот, ты правда бот?\n'
                                                '└❗️Пишите в конце вопроса "?", иначе бот распознает это как фразу!\n\n'
                                                
                                                
                                                '🏞Оценка фото\n'
                                                '└Отправь боту любое фото(не как документ) и он его оценит!\n\n\n'
                                                
                                                
                                                
                                                '🌟🌟🌟ПОДПИСКА🌟🌟🌟\n\n'
                                                
                                                '💵что даёт обычная подписка?\n'
                                                '└Доступ к минииграм🕹\n'
                                                '└доступ к управлению уведомлениями🔔\n\n'
                                                
                                                '🎁что даёт сверхпрем подписка?\n'
                                                '└Безлимит на посты в ВК🌄\n'
                                                '└Подписка действует год, а не месяц, как обычная🎟\n'
                                                '└Безлимит на обьём отправляемых файлов📁\n\n'
                                                
                                                'PS.\n'
                                                '└Ваш стартовый баланс:\n'
                                                ' └Посты вк: 55️⃣\n'
                                                ' └Обьём отправляемого файла: до 30 слов3️⃣0️⃣\n'
                                                ' └можно прислать лишь 10 фото1️⃣0️⃣\n',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton('Написать в поддержку🆘', callback_data='nap_podderj')
                               ))


@dp.message_handler()
async def othm(ms: types.Message):
    try:
        subscription_date_status = \
            cursor.execute(f'''SELECT subscription_date FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0].split('-')
        year = int(subscription_date_status[0])
        month = int(subscription_date_status[1])
        day = int(subscription_date_status[2])
        if date.day >= day:
            if date.month >= month or date.year > year:
                cursor.execute(f'''UPDATE user SET subscription_date="0" WHERE telegram_id={ms.from_user.id}''')
                cursor.execute(f'''UPDATE user SET subscription=0 WHERE telegram_id={ms.from_user.id}''')
                await bot.send_message(ms.from_user.id, 'Ваша подписка закончена⏰\n'
                                                        'Не расстраивайтесь, ведь вы можете продлить её ещё '
                                                        'на месяц, или купить новую, более лучшую!', reply_markup=
                                       InlineKeyboardMarkup().add(
                                           InlineKeyboardButton('Купить👑', callback_data='oform_premium')
                                       ))
                conn.commit()

    except:
        pass
    if 'Меню' in ms.text:
        prem_status = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if prem_status == 0:
            await bot.send_message(ms.from_user.id, 'Меню;', reply_markup=standart_keyboard)
        if prem_status in [1, 2]:
            await bot.send_message(ms.from_user.id, 'Меню;', reply_markup=premium_keyboard)
    if '/super' in ms.text:
        await ms.answer('Выбери клетку: ', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton('🟣', callback_data='neitral'),
            InlineKeyboardButton('🟣', callback_data='neitral'),
            InlineKeyboardButton('🟣', callback_data='neitral')).add(
            InlineKeyboardButton('🟣', callback_data='neitral'),
            InlineKeyboardButton('🟣', callback_data='neitral'),
            InlineKeyboardButton('🟣', callback_data='neitral')).add(
            InlineKeyboardButton('🟣', callback_data='neitral'),
            InlineKeyboardButton('🟣', callback_data='neitral'),
            InlineKeyboardButton('🟣', callback_data='neitral')))
    elif 'игры' in ms.text:
        subscription_status = \
            cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if subscription_status in [1, 2]:
            await bot.send_message(ms.from_user.id, 'Вот список доступных игры: ', reply_markup=game_bar_keyboard)
        else:
            await bot.send_message(ms.from_user.id, 'У вас нет активированного премиум статуса😢',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')
                                   ))


    elif '/compet' in ms.text:
        ids = cursor.execute(f'''SELECT telegram_id FROM user''').fetchall()
        await ms.answer('Вы обьявили конкурс🎁', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton('результат👑', callback_data='results')
        ))
        for i in range(len(ids)):
            subscription_status = \
            cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
            push_status = cursor.execute(f'''SELECT push FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
            if subscription_status not in [1, 2] and push_status != 0:
                await bot.send_message(ids[i][0], 'КОНКУРС НА ПОДПИСКИ🌟!\n\n' + ms.text[8:],
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton('Я участвую!✅', callback_data='partic')).add(
                                           InlineKeyboardButton('Не уведомлять о конкурсах🛑', callback_data='push_off')
                                       ))

    elif ms.text == 'орел и решка👑' or ms.text == 'орёл и решка👑':
        subscription_status = \
        cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if subscription_status in [1, 2]:
            rlist = ['орёл🦅', 'решка👑']
            result = random.choice(rlist)
            if 'орёл' in result:
                await bot.send_message(ms.from_user.id, 'Вам выпал ' + result)
            else:
                await bot.send_message(ms.from_user.id, 'Вам выпала ' + result)
        else:
            await bot.send_message(ms.from_user.id, 'У вас нет активированного премиум статуса😢',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')
                                   ))
    elif 'да или нет' in ms.text:
        subscription_status = \
        cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if subscription_status in [1, 2]:
            rlist = ['да✅', 'нет❌']
            result = random.choice(rlist)
            await bot.send_message(ms.from_user.id, 'Вам выпало ' + result)
        else:
            await bot.send_message(ms.from_user.id, 'У вас нет активированного премиум статуса😢',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')
                                   ))
    elif 'камень ножницы бумага' in ms.text:
        status_id = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if status_id > 0:
            await bot.send_message(ms.from_user.id, '🎌Первым ходишь ты: ', reply_markup=
            InlineKeyboardMarkup().add(
                InlineKeyboardButton('Камень🥌', callback_data='camen')
            ).add(
                InlineKeyboardButton('Ножницы✂', callback_data='nojnic')
            ).add(
                InlineKeyboardButton('Бумага📜', callback_data='bumag')
            ))
        else:
            await bot.send_message(ms.from_user.id, 'У вас нет активированного премиум статуса😢',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')
                                   ))

    if 'уведомления🔔' in ms.text:
        status = cursor.execute(f'''SELECT push, main FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()
        on_concurse_push = InlineKeyboardMarkup().add(InlineKeyboardButton('уведомлять о конкурсах✅', callback_data='push_on'))
        on_push = InlineKeyboardMarkup().add(
            InlineKeyboardButton('уведомлять о событиях в боте✅', callback_data='push_on'))


        if status[0] == 0 and status[1] in [0, 3]:

            await bot.send_message(ms.from_user.id, 'Уведомления о боте: 🚫\nУведомление о конкурсах: 🚫', reply_markup=
            InlineKeyboardMarkup().add(
                InlineKeyboardButton('Уведомлять о событиях в боте✅', callback_data='podpis')).add(
                InlineKeyboardButton('Уведомлять о конкурсах✅', callback_data='push_on')))
        if status[0] == 1 and status[1] in [0, 3]:
            await bot.send_message(ms.from_user.id, 'Уведомления о боте: 🚫\nУведомление о конкурсах: ✅', reply_markup=
            InlineKeyboardMarkup().add(
                InlineKeyboardButton('Уведомлять о событиях в боте✅', callback_data='podpis')).add(
                InlineKeyboardButton('Не уведомлять о конкурсах🚫', callback_data='push_off'))
                                   )
        if status[0] == 1 and status[1] == 1:
            await bot.send_message(ms.from_user.id, 'Уведомления о боте: ✅\nУведомление о конкурсах: ✅', reply_markup=
            InlineKeyboardMarkup().add(
                InlineKeyboardButton('Не уведомлять о событиях в боте🚫', callback_data='otpis')).add(
                InlineKeyboardButton('Не уведомлять о конкурсах🚫', callback_data='push_off'))
                                   )
        if status[0] == 0 and status[1] == 1:
            await bot.send_message(ms.from_user.id, 'Уведомления о боте: ✅\nУведомление о конкурсах: 🚫', reply_markup=
            InlineKeyboardMarkup().add(
                InlineKeyboardButton('Не уведомлять о событиях в боте🚫', callback_data='otpis')).add(
                InlineKeyboardButton('Уведомлять о конкурсах✅', callback_data='push_on'))
                                   )


    elif 'подписка🎁' in ms.text:
        subscription_date_status = \
            cursor.execute(f'''SELECT subscription_date FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        posts = cursor.execute(f'''SELECT walls FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        status = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if status == 0:
            await bot.send_message(ms.from_user.id, f'Статус вашей подписки: отсутствует🚫\n\nПостов ВК: {posts}🌆', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')
                                   ))
        if status == 1:
            await bot.send_message(ms.from_user.id, f'Статус вашей подписки: Премиум✅\n\nОкончание действия: {subscription_date_status}📆\n\nПостов ВК: {posts}🌆', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Купить сверхпрем👑', callback_data='oform_premium')
                                   ))
        if status == 2:
            await bot.send_message(ms.from_user.id, f'Статус вашей подписки: Сверхпремиум👑!\n\nОкончание действия: {subscription_date_status}📆\n\n'
                                                    f'Постов ВК: {posts}🌆')
    elif 'Купить прем' in ms.text:
        premium_status = \
        cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if premium_status == 0 or premium_status == 3:
            await bot.send_message(ms.from_user.id, '✅Выбери тариф: ', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Премиум⭐', callback_data='prem')).add(
                InlineKeyboardButton('Сверх премиум🌟', callback_data='sverh_prem'))
                                   )
        if premium_status == 1:
            await bot.send_message(ms.from_user.id, '✅Выбери тариф: ', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Сверх премиум🌟', callback_data='sverh_prem')))

        if premium_status == 2:
            await bot.send_message(ms.from_user.id, 'У вас уже есть активный сверхпремиум тариф👑')
    elif 'ofpr' in ms.text:
        await bot.send_message(ms.from_user.id,
                               'у вас нет активированного премиум статуса😢',
                               reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')
                               ))
    elif '/vk' in ms.text:
        if len(ms.text.split()) > 1:
            try:
                select_subscription = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
                walls = cursor.execute(f'''SELECT walls FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
                if select_subscription != 2 and walls <= 0:
                    await bot.send_message(ms.from_user.id, 'Эта функция доступна лишь по единоразовой оплате, или при покупке сверхпрема!',
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton('Купить посты ВК💵', callback_data='buy_walls')
                                           ).add(
                                               InlineKeyboardButton('Оформить премиум👑', callback_data='oform_premium')
                                           ))
                elif select_subscription == 2 or walls > 0:
                    if select_subscription != 2:
                        walls = \
                        cursor.execute(f'''SELECT walls FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
                        cursor.execute(f'''UPDATE user SET walls={walls - 1} WHERE telegram_id={ms.from_user.id}''')

                    result = ms.text.split()
                    domen = result[1]
                    post_id = result[2]

                    vk_user_id = vk.utils.resolveScreenName(screen_name=domen)
                    res = vk.wall.getComments(owner_id=vk_user_id["object_id"], post_id=post_id, count=99)
                    r_list = []

                    for i in range(len(res['items'])):
                        r_list.append(res['items'][i])
                    r_comment = random.choice(r_list)

                    screen_name = vk.users.get(user_ids=r_comment['from_id'], fields='domain', name_case='nom')
                    await bot.send_message(ms.from_user.id, f'Случайный комментарий: {r_comment["text"]}\n\nАвтор: {screen_name[0]["first_name"]} {screen_name[0]["last_name"]}\n\nУ вас осталось {walls} постов!\n\nhttps://vk.com/{screen_name[0]["domain"]}')
                    conn.commit()
            except vk_api.exceptions.ApiError:
                await bot.send_message(ms.from_user.id, 'Такой записи не существует на стене пользователя🤵')
            except TypeError:
                await bot.send_message(ms.from_user.id, 'Такого пользователя не существует!🚫')
        else:
            await bot.send_photo(chat_id=ms.from_user.id, photo='https://sun9-45.userapi.com/impg/75p6gZ6mDX_aIE0Zjnak8_8XIQAFcVMB1q3ZgA/6UH0r7l9d64.jpg?size=643x278&quality=96&proxy=1&sign=0602b861479bb8acd9e4a8e42b9060fa&type=album', caption='Ищем ID поста🔍')
            await bot.send_photo(chat_id=ms.from_user.id, photo='https://sun9-29.userapi.com/impg/LKb1ZaqmTOMX2yW2fgVEL5pR3HKZiTM7Kl15WA/LU3WeRtSM-o.jpg?size=491x210&quality=96&proxy=1&sign=79b9a4e3547a126dc950cb69512c1cc5&type=album', caption='Ищем ID поста🔍\n\n'
                                                                                                                                                                                                                                                    'Копируем эти цифры;')
            await bot.send_photo(chat_id=ms.from_user.id, photo='https://sun9-39.userapi.com/impg/EEybOsLVT1Mcsh-myCVS94isbSrlewZMDbF79g/_FF_WKWyezA.jpg?size=351x190&quality=96&proxy=1&sign=32078bc06a99708df74c28ca0172b8b8&type=album', caption='Составляем запрос✏')

    elif ms.text == '/not_premium':
        cursor.execute(f'''UPDATE user SET subscription=0 WHERE telegram_id={ms.from_user.id}''')
        conn.commit()

    elif '/free_keyboard' in ms.text:
        await bot.send_message(ms.from_user.id, '.', reply_markup=standart_keyboard)


    elif ms.text == '/update_keyboard':
        ids = cursor.execute(f'''SELECT telegram_id FROM user''').fetchall()
        for i in range(len(ids)):
            subscription_status = \
                cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
            if subscription_status in [1, 2]:
                await bot.send_message(ids[i][0], 'Вам пришли новые функции бота🎁', reply_markup=premium_keyboard)
            if subscription_status == 0:
                await bot.send_message(ids[i][0], 'Вам пришли новые функции бота🎁', reply_markup=standart_keyboard)
    elif '/mail' in ms.text:
        ids = cursor.execute(f'''SELECT telegram_id FROM user''').fetchall()
        for i in range(len(ids)):
            mail_status = cursor.execute(f'''SELECT main FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
            if mail_status == 1:
                await bot.send_message(ids[i][0], 'Привет, это новые новости о боте!\n\n' + ms.text[6:], reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton('Отписаться от рассылки❌', callback_data='otpis')
                ))
            if mail_status == 0:
                await bot.send_message(ids[i][0], 'А вы, хотите получать новости?\n\n',
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton('Подписаться на рассылку✅', callback_data='podpis')).add(
                                           InlineKeyboardButton('Не предлагать больше🚫', callback_data='nopodpis')
                                       ))
    elif ms.text == '/rait':
        result = cursor.execute('''SELECT rated FROM user''').fetchall()
        rest = 0
        for i in range(len(result)):
            rest += result[i][0]

        rest = rest / len(result)
        await ms.reply(rest)

    elif '?' in ms.text or '❓' in ms.text:
        val_list = ['возможно', 'скорее всего', 'наверное', 'точно', 'абсолютно точно!', 'нет', 'скорее всего нет!',
                    'Очень жаль, но точно нет!', 'точно нет!', 'абсолютно точно нет!']
        smile = ['o(*￣▽￣*)ブ', '(☞ﾟヮﾟ)☞', '(^人^)', '(❤ ω ❤)', 'ヽ(￣ω￣〃)ゝ', '(⓿_⓿)', 'ヾ(≧▽≦*)o', 'ψ(｀∇´)ψ', '(´▽`ʃ♡ƪ)']
        await bot.send_message(ms.from_user.id, random.choice(val_list) + random.choice(smile))

    elif '/random' in ms.text or '/рандом' in ms.text:
        random_list = ms.text[8:].split()
        subscription_status = \
            cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if (subscription_status == 0 and len(random_list)) < 30 or (subscription_status == 1 and len(random_list) < 100) or subscription_status == 2:
            if len(random_list) == 0:
                await bot.send_message(ms.from_user.id, 'Эй, напиши строку или несколько чисел!🎲\n\nПример: /random 1 2 3 4')

            elif len(random_list) != 1:
                await bot.send_message(ms.from_user.id, random.choice(random_list))
                attempts = cursor.execute(f'''SELECT attempts FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[
                    0]
                cursor.execute(f'''UPDATE user SET attempts={attempts + 1} WHERE telegram_id={ms.from_user.id}''')
                conn.commit()
                attempts = cursor.execute(f'''SELECT attempts FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[
                    0]


                if attempts % 5 == 0:
                    rated = \
                    cursor.execute(f'''SELECT rated FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
                    if rated == 0:
                        await bot.send_message(ms.from_user.id,
                                               f'Привет, ты пользовался ботом уже {attempts} раз, не мог бы ты поставить оценку боту?',
                                               reply_markup=InlineKeyboardMarkup().add(
                                                   InlineKeyboardButton('⭐', callback_data='oc_1')).add(
                                                   InlineKeyboardButton('⭐⭐', callback_data='oc_2')).add(
                                                   InlineKeyboardButton('⭐⭐⭐', callback_data='oc_3')).add(
                                                   InlineKeyboardButton('⭐⭐⭐⭐', callback_data='oc_4')).add(
                                                   InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data='oc_5')))
                    else:
                        await bot.send_message(ms.from_user.id, 'Спасибо, что уже долгое время пользуешься ботом и поставил ему оценку!',
                                               reply_markup=InlineKeyboardMarkup().add(
                                                   InlineKeyboardButton('Убрать оценку⭐', callback_data='del_oc')
                                               ))
            else:
                random_list = list(random_list[0])
                await bot.send_message(ms.from_user.id, random.choice(random_list))

                attempts = cursor.execute(f'''SELECT attempts FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[
                    0]
                cursor.execute(f'''UPDATE user SET attempts={attempts + 1} WHERE telegram_id={ms.from_user.id}''')
                conn.commit()
                attempts = cursor.execute(f'''SELECT attempts FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[
                    0]

                if attempts % 5 == 0:
                    rated = \
                        cursor.execute(f'''SELECT rated FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
                    if rated == 0:
                        await bot.send_message(ms.from_user.id,
                                               f'Привет, ты пользовался ботом уже {attempts} раз, не мог бы ты поставить оценку боту?',
                                               reply_markup=InlineKeyboardMarkup().add(
                                                   InlineKeyboardButton('⭐', callback_data='oc_1')).add(
                                                   InlineKeyboardButton('⭐⭐', callback_data='oc_2')).add(
                                                   InlineKeyboardButton('⭐⭐⭐', callback_data='oc_3')).add(
                                                   InlineKeyboardButton('⭐⭐⭐⭐', callback_data='oc_4')).add(
                                                   InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data='oc_5')))
                    else:
                        await bot.send_message(ms.from_user.id,
                                               'Спасибо, что уже долгое время пользуешься ботом и поставил ему оценку!',
                                               reply_markup=InlineKeyboardMarkup().add(
                                                   InlineKeyboardButton('Убрать оценку⭐', callback_data='del_oc')
                                               ))

        else:
            await bot.send_message(ms.from_user.id, 'Ограничения вашей подписки🚫', reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Оформить премиум👑', callback_data='oform_premium')))

    if 'рынок' in ms.text:
        subscription_status = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]
        if subscription_status != 2:
            await ms.answer('🆕РЫНОК🆕\n\nЗдесь ты можешь покупать и обменивать подписки🎁', reply_markup=
                            InlineKeyboardMarkup().add(
                                InlineKeyboardButton('Купить прем👑', callback_data='oform_premium')).add(
                                InlineKeyboardButton('Купить посты ВК🗺', callback_data='buy_walls')).add(
                                InlineKeyboardButton('🆕Обмен постов на прем👑', callback_data='walls_prem')
                            ))
        if subscription_status == 2:
            await ms.answer('У вас уже есть все товары рынка(у вас сверхпремиум тариф)❗')
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def send_document(ms: types.Message):

    subscription_status = \
    cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]

    file_id = ms.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.send_message(ms.from_user.id, 'Подожди немного, обрабатываю файл📁')

    try:
        await bot.download_file(file_path, "doc.txt")
        doc = open('doc.txt', 'rb')
        result = doc.read().decode('utf-8').split()
        if subscription_status == 0 and len(result) < 30:
            doc = open('doc.txt', 'rb')
            await bot.send_message(ms.from_user.id, 'Текст файла: \n' + doc.read().decode('utf-8'))
            await bot.send_message(ms.from_user.id, random.choice(result))

        elif len(result) > 30 and len(result) < 100 and subscription_status == 1:
            await bot.send_message(ms.from_user.id, random.choice(result))

        elif len(result) > 100 and subscription_status in [0, 1]:
            await bot.send_message(ms.from_user.id,
                                   'Отправлять большие файлы могут только сверхпрем👑 пользователи!🚫\n', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Оформить премиум👑', callback_data='oform_premium')))
        elif len(result) > 30 and len(result) < 100 and subscription_status == 0:
            await bot.send_message(ms.from_user.id, 'Ограничение на количество слов без подписки🚫\n'
                                                    'Вы можете отправить файл с не более 30 словами!', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Оформить премиум👑', callback_data='oform_premium')))

        elif subscription_status == 2:
            await bot.send_message(ms.from_user.id, random.choice(result))


    except:
        doc = open('doc.txt', 'rb')
        result = doc.read().decode('utf-8').split()
        if subscription_status == 2:
            await bot.send_message(ms.from_user.id, '❗Файл слишком большой, поэтому телеграм не позволяет '
                                                    'отправить текст;')
            await bot.send_message(ms.from_user.id, random.choice(result))
        else:
            await bot.send_message(ms.from_user.id, 'Отправлять большие файлы могут только сверхпрем👑 пользователи!🚫\n', reply_markup=
            InlineKeyboardMarkup().add(InlineKeyboardButton('Оформить премиум👑', callback_data='oform_premium')))

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def send_document(ms: types.Message):

    subscription_status = \
    cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={ms.from_user.id}''').fetchone()[0]

    if subscription_status in [1, 2]:
        eval_list = ['10/10, бомба💣🔞', '9/10, почти бомба🔉', '8/10, чел ты....', '7/10, ближе к 6️⃣', '6️⃣/🔟, стрёмный тип, но с лимонадом норм🥤',
                     '5/10, фигня🙉', '4/10 нуууу...Тут даже с лимонадом не стрёмно🥤🚫', '3/10 ,то же самое что и 2/10', '1/10, '
                                                                                                                   'Настолько плохо, что даже хорошо✅']
        eval_value = random.choice(eval_list)
        file = await bot.get_file(ms.photo[0].file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "photo.jpg")
        doc = open('photo.jpg', 'rb')
        await bot.send_photo(chat_id=ms.from_user.id, photo=doc, caption=eval_value)


@dp.callback_query_handler(lambda c: True)
async def callback(c):

    if c.data in ['bumag', 'nojnic', 'camen']:
        user_value = c.data
        if user_value == 'bumag':
            user_value = 'бумага📜'
        elif user_value == 'nojnic':
            user_value = 'ножницы✂'
        elif user_value == 'camen':
            user_value = 'камень🥌'
        r_value = random.choice(['камень🥌', 'ножницы✂', 'бумага📜'])
        if r_value == user_value:
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nНИЧЬЯ!👁‍', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')
                                   ))
        if user_value == 'камень🥌' and r_value == 'бумага📜':
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nБОТ ПОБЕДИЛ!🤖🏆',
                                        reply_markup=
                                        InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')))
        if user_value == 'камень🥌' and r_value == 'ножницы✂':
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nВЫ ПОБЕДИЛИ!🥇🏆',
                                        reply_markup=
                                        InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')))
        if user_value == 'бумага📜' and r_value == 'камень🥌':
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nВЫ ПОБЕДИЛИ!🥇🏆',
                                        reply_markup=
                                        InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')))
        if user_value == 'бумага📜' and r_value == 'ножницы✂':
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nБОТ ПОБЕДИЛ!🤖🏆',
                                        reply_markup=
                                        InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')))
        if user_value == 'ножницы✂' and r_value == 'бумага📜':
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nВЫ ПОБЕДИЛИ!🥇🏆',
                                        reply_markup=
                                        InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')))
        if user_value == 'ножницы✂' and r_value == 'камень🥌':
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text=f'Ты выбрал {user_value}\n\nБот выбрал {r_value}\n\nБОТ ПОБЕДИЛ!🤖🏆',
                                        reply_markup=
                                        InlineKeyboardMarkup().add(
                                            InlineKeyboardButton('🔄Переиграть', callback_data='replay_in_knb')))

    if c.data == 'replay_in_knb':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='🎌Первым ходишь ты: ', reply_markup=
        InlineKeyboardMarkup().add(
            InlineKeyboardButton('Камень🥌', callback_data='camen')
        ).add(
            InlineKeyboardButton('Ножницы✂', callback_data='nojnic')
        ).add(
            InlineKeyboardButton('Бумага📜', callback_data='bumag')
        ))
    if c.data == 'oform_premium':
        premium_status = cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={c.from_user.id}''').fetchone()[0]
        if premium_status == 0 or premium_status == 3:
            await bot.send_message(c.from_user.id, '✅Выбери тариф: ', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Премиум⭐', callback_data='prem')).add(
                InlineKeyboardButton('Сверх премиум🌟', callback_data='sverh_prem'))
                                   )
        if premium_status == 1:
            await bot.send_message(c.from_user.id, '✅Выбери тариф: ', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Сверх премиум🌟', callback_data='sverh_prem')))

        if premium_status == 2:
            await bot.send_message(c.from_user.id, 'У вас уже есть активный сверхпремиум тариф👑')

    if c.data == 'oformу_premium':
        premium_status = \
        cursor.execute(f'''SELECT subscription FROM user WHERE telegram_id={c.from_user.id}''').fetchone()[0]
        if premium_status == 0 or premium_status == 3:
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='✅Выбери тариф: ', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Премиум⭐', callback_data='prem')).add(
                InlineKeyboardButton('Сверх премиум🌟', callback_data='sverh_prem'))
                                   )
        if premium_status == 1:
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='✅Выбери тариф: ', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Сверх премиум🌟', callback_data='sverh_prem')
            ))

        else:
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='У вас уже есть активный сверхпремиум тариф👑')
    if c.data == 'prem':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Тариф: премиум⭐\n\n'
                                                                                             'Доп. функции: ✅\n'
                                                                                             'Комментарии вк: 🚫\n\n'
                                                                                                  '𝙋𝙍𝙄𝘾𝙀: 30p', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton('Выбрать другой тариф🔄', callback_data='oformу_premium')
        ).add(
                                        InlineKeyboardButton('Купить🛒', callback_data='buy_premium')
                                    ))
    if c.data == 'sverh_prem':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Тариф: сверх-премиум🌟\n\n'
                                                                                                  'Доп. функции: ✅\n'
                                                                                                  'Комментарии вк: ✅\n\n'
                                                                                                  '𝙋𝙍𝙄𝘾𝙀: 100p',
                                    reply_markup=InlineKeyboardMarkup().add(
                                        InlineKeyboardButton('Выбрать другой тариф🔄', callback_data='oformу_premium')
                                    ).add(
                                        InlineKeyboardButton('Купить🛒', callback_data='buy_sverh_premium')
                                    ))

    if c.data == 'buy_sverh_premium':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Выполняем запрос🕥')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Покупаем личный самолёт🛩')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Пьём самый дорогой ликёр🥃')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Активируем сверхпремиум премиум👑')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Готово✅\nТеперь вам'
                                                                                                  ' доступны абсолютно все функции бота!')
        await bot.send_message(c.from_user.id, 'Вам отправлены сверх прем функции👑', reply_markup=premium_keyboard)
        cursor.execute(f'''UPDATE user SET subscription=2 WHERE telegram_id={c.from_user.id}''')
        if date.month == 12:
            date_next_month = f'{date.year}-1-{date.day}'
        else:
            date_next_month = f'{date.year}-{date.month + 1}-{date.day}'
        cursor.execute(f'''UPDATE user SET subscription_date='{date_next_month}' WHERE telegram_id={c.from_user.id}''')
        conn.commit()
    if c.data == 'buy_premium':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Выполняем запрос🕥')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Воруем деньги с обедов🥘💵')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Воруем деньги с карт💳')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Активируем премиум👑')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Готово✅\nТеперь вам'
                                                                                                  ' доступны почти все функции бота!')
        await bot.send_message(c.from_user.id, 'Вам отправлены VIP функции👑', reply_markup=premium_keyboard)
        cursor.execute(f'''UPDATE user SET subscription=1 WHERE telegram_id={c.from_user.id}''')
        if date.month == 12:
            date_next_month = f'{date.year}-1-{date.day}'
        else:
            date_next_month = f'{date.year}-{date.month + 1}-{date.day}'
        cursor.execute(f'''UPDATE user SET subscription_date='{date_next_month}' WHERE telegram_id={c.from_user.id}''')
        conn.commit()
    if c.data == 'free_premium':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Активируем премиум👑')
        await asyncio.sleep(1)
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Готово✅\nТеперь вам'
                                                                                                  ' доступны все функции бота!')
        await bot.send_message(c.from_user.id, 'Вам отправлены VIP функции👑', reply_markup=premium_keyboard)
        cursor.execute(f'''UPDATE user SET subscription=1 WHERE telegram_id={c.from_user.id}''')
        conn.commit()

    if c.data == 'partic':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Вы учавствуете в конкурсе✅\n\n', reply_markup=
                                    InlineKeyboardMarkup().add(
                                        InlineKeyboardButton('Не уведомлять о конкурсах🛑', callback_data='push_off')
                                    ))
        cursor.execute(f'''UPDATE user SET concurses=1 WHERE telegram_id={c.from_user.id}''')
        conn.commit()

    if c.data == 'push_off':
        cursor.execute(f'''UPDATE user SET push=0 WHERE telegram_id={c.from_user.id}''')
        conn.commit()
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Вам больше не будут приходить уведомления о'
                                         ' текущих конкурсах;\n\n☑', reply_markup=
                                    InlineKeyboardMarkup().add(
                                        InlineKeyboardButton('уведомлять о конкурсах✅', callback_data='push_on')
                                    ))
    if c.data == 'push_on':
        cursor.execute(f'''UPDATE user SET push=1 WHERE telegram_id={c.from_user.id}''')
        conn.commit()
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Теперь вы будете знать о'
                                         ' текущих конкурсах✅;\n\n')
    if c.data == 'nopodpis':
        cursor.execute(f'''UPDATE user SET main=3 WHERE telegram_id={c.from_user.id}''')
        conn.commit()
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Мы больше не будем предлагать вам рассылку☑', reply_markup=
                                    InlineKeyboardMarkup().add(
                                        InlineKeyboardButton('СТОП! ОТМЕНА!😩', callback_data='podpis')
                                    ))
    if c.data == 'otpis':
        cursor.execute(f'''UPDATE user SET main=0 WHERE telegram_id={c.from_user.id}''')
        conn.commit()
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Вы отписались от рассылки!❌', reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton('Подписаться на рассылку✅', callback_data='podpis')).add(
                                           InlineKeyboardButton('Не предлагать больше🚫', callback_data='nopodpis')
                                       ))
    if c.data == 'podpis':
        cursor.execute(f'''UPDATE user SET main=1 WHERE telegram_id={c.from_user.id}''')
        conn.commit()
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Вы подписаны на рассылку✅', reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton('Отписаться от рассылки❌', callback_data='otpis')))

    if c.data == 'del_oc':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Вы удалили свою оценку✔🌠')
        cursor.execute(f'''UPDATE user SET rated=0 WHERE telegram_id={c.from_user.id}''')
        conn.commit()
    if c.data in ['oc_1', 'oc_2', 'oc_3', 'oc_4', 'oc_5']:
        rated = cursor.execute(f'''SELECT rated FROM user WHERE telegram_id={c.from_user.id}''').fetchone()[0]
        if rated == 0:
            if c.data == 'oc_1':
                await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Ваш голос принят: ⭐')
                cursor.execute(f'''UPDATE user SET rated=1 WHERE telegram_id={c.from_user.id}''')
                conn.commit()
            if c.data == 'oc_2':
                await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Ваш голос принят: ⭐⭐')
                cursor.execute(f'''UPDATE user SET rated=2 WHERE telegram_id={c.from_user.id}''')
                conn.commit()
            if c.data == 'oc_3':
                await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Ваш голос принят: ⭐⭐⭐')
                cursor.execute(f'''UPDATE user SET rated=3 WHERE telegram_id={c.from_user.id}''')
                conn.commit()
            if c.data == 'oc_4':
                await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Ваш голос принят: ⭐⭐⭐⭐')
                cursor.execute(f'''UPDATE user SET rated=4 WHERE telegram_id={c.from_user.id}''')
                conn.commit()
            if c.data == 'oc_5':
                await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Ваш голос принят: ⭐⭐⭐⭐⭐')
                cursor.execute(f'''UPDATE user SET rated=5 WHERE telegram_id={c.from_user.id}''')
                conn.commit()

        else:
            await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                        text='Вы уже поставили свою оценку!')
    if c.data == 'buy_walls':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Покупка 5 постов🗺\n\nцена: 75р💰', reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Купить🛒', callback_data='buy_wall')
            ))
    if c.data == 'buy_wall':
        walls = cursor.execute(f'''SELECT walls FROM user WHERE telegram_id={c.from_user.id}''').fetchone()[0]
        cursor.execute(f'''UPDATE user SET walls={walls + 5}''')
        conn.commit()
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Успешно!\n\nТеперь вы можете отправить боту ссылку на пост ВК;')
    if c.data == 'nap_podderj':
        await bot.send_message(c.from_user.id, '\n\nВыберите тип сообщения: ', reply_markup=
                                    InlineKeyboardMarkup().add(
                                        InlineKeyboardButton('Жалоба😡', callback_data='complaint')).add(
                                        InlineKeyboardButton('Предложение🤔', callback_data='sentence')).add(
                                        InlineKeyboardButton('Пожелание🍏', callback_data='pojelanie')
                                    ))

    if c.data == 'complaint':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Чат с поддержкой открыт🆘\n\nНапишите жалобу в одном сообщении: ')
        await Form.sos.set()
    if c.data == 'sentence':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Чат с поддержкой открыт🆘\n\nНапишите предложение в одном сообщении: ')
        await Form.sos.set()
    if c.data == 'pojelanie':
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                    text='Чат с поддержкой открыт🆘\n\nНапишите пожелание в одном сообщении: ')
        await Form.sos.set()
    if c.data == 'walls_prem':
        walls = cursor.execute(f'''SELECT walls FROM user WHERE telegram_id={c.from_user.id}''').fetchone()[0]
        if walls >= 5:
            await bot.send_message(c.from_user.id, 'Обмен 5 постов на оычный прем🎁', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Обменять▶', callback_data='obmen_walls_post')
                                   ))
        else:
            await bot.send_message(c.from_user.id, 'У вас недостаточно постов❗\nМинимум 5❗')
    if c.data == 'obmen_walls_post':
        walls = cursor.execute(f'''SELECT walls FROM user WHERE telegram_id={c.from_user.id}''').fetchone()[0]
        await bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id, text='Вы успешно обменяли 5 постов на обычный прем!')
        cursor.execute(f'''UPDATE user SET walls={walls - 5}, subscription=1 WHERE telegram_id={c.from_user.id}''')
        await asyncio.sleep(1)
        await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
        conn.commit()
    if c.data == 'results':

        ids = cursor.execute(f'''SELECT telegram_id FROM user''').fetchall()
        result = []
        try:
            for i in range(len(ids)):
                    concurs_status = \
                        cursor.execute(f'''SELECT concurses FROM user WHERE telegram_id={ids[i][0]}''').fetchone()[
                            0]
                    if concurs_status == 1:
                        result.append(ids[i][0])
            cursor.execute(f'''UPDATE user SET concurses=0''')
            conn.commit()
            result = random.choice(result)
            await bot.send_message(result, 'Вы выиграли подписку🎁', reply_markup=
                                   InlineKeyboardMarkup().add(
                                       InlineKeyboardButton('Активировать👑', callback_data='free_premium')
                                   ))


        except:
            pass
    await bot.answer_callback_query(callback_query_id=c.id, text='')


@dp.message_handler(state=Form.sos)
async def sos(ms: types.Message, state: FSMContext):
    await ms.answer('Ваше предложение отправлено модераторам✅⏭')
    await bot.send_message(admins[0], '❗Сообщение в поддержку: ' + ms.text, reply_markup=InlineKeyboardMarkup().add(
        InlineKeyboardButton('принять✅', callback_data='enter_predloj')
    ).add(
        InlineKeyboardButton('отклонить❌', callback_data='noenter_predloj')
    ))
    await state.finish()

@dp.edited_message_handler()
@dp.message_handler()
async def edit(ms: types.Message):
    await bot.delete_message(chat_id=ms.from_user.id, message_id=ms.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)