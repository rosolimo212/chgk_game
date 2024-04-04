import random
import numpy as np
import pandas as pd
import datetime
import yaml, json

import os
current_dir = os.path.abspath(os.getcwd())
parent_dir = os.path.dirname(current_dir)

# добавить папку с собственными библиотеками
import sys
# ддя linux
# sys.path.append('//home//roman//python//litres//data_load//')
sys.path.append(parent_dir+'/data_load/')
sys.path.append(parent_dir+'/draw/')

import mechanics as mh


from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor

# костыль, чтобы на юпитере работала
# import nest_asyncio
# nest_asyncio.apply()

def read_yaml_config(yaml_file: str, section: str) -> dict:
    """
    Читаем yaml-файл настроек для дальнейшей работы
    """
    with open(yaml_file, 'r') as yaml_stream:
        descriptor = yaml.full_load(yaml_stream)
        if section in descriptor:
            configuration = descriptor[section]
            return configuration
        else:
            print(f"Section {section} not find in the file '{yaml_file}'")

def make_answer_buttons(buttons_lst):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons_lst:
        item = types.KeyboardButton(text=button)
        markup.add(item)
    
    return markup 

async def launch_404(bot, message):
    markup = make_answer_buttons([
         'Главное меню',
                                ])
    await bot.send_message(
        message.chat.id, 
        """
К сожалению, что-то пошло не так: такой команды нет.
Возможно, произошла ошибка в самой игре. 
Возможно, вы использовали неожиданную текстовую команду.
Возвращайтесь в главное меню и попробуйте снова.
Если проблема повторяется, нажмите /start
        """,
        reply_markup=markup
                )
    
async def start_game(bot, message):
    markup = make_answer_buttons([
         'Следующий вопрос', 'Главное меню'
                                ])
    await bot.send_message(message.from_user.id, """Начнём""", reply_markup=markup)
    gamers_lst = mh.create_team()
    await bot.send_message(message.from_user.id, """Команда создана: """, reply_markup=markup)
    for i in range(len(gamers_lst)):
        await bot.send_message(
                                message.from_user.id, 
                                "Игрок " + str(i+1) + " skil:" + str(gamers_lst[i].skill) + " ego: " + str(gamers_lst[i].ego), 
                                reply_markup=markup
                            )
    difficult = round(random.randint(20, 90),2)
    await bot.send_message(
                                message.from_user.id, 
                                "сложность вопроса :" + str(difficult), 
                                reply_markup=markup
                            )
    res, jump_lst, help_lst, jump_value, help_value, team_value = mh.minute(gamers_lst, difficult)
    await bot.send_message(
                                message.from_user.id, 
                                "взяли ли вопрос: " + str(res), 
                                reply_markup=markup
                            )
    await bot.send_message(
                            message.from_user.id, 
                            "массив накидываний: " + str(jump_lst), 
                            reply_markup=markup
                        )
    await bot.send_message(
                        message.from_user.id, 
                        "массив докрутов: " + str(help_lst), 
                        reply_markup=markup
                    )
    await bot.send_message(
                        message.from_user.id, 
                        "лучшая версия: " + str(jump_value), 
                        reply_markup=markup
                    )
    await bot.send_message(
                        message.from_user.id, 
                        "лучший докрут: " + str(help_value), 
                        reply_markup=markup
                    )
    

bot = Bot(read_yaml_config('config.yaml', section='chgk_emulator')['token'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'старт'])
async def launch_main_menu(message: types.Message):
    markup = make_answer_buttons([
         'Начать игру'
                                ])
    await bot.send_message(message.from_user.id, """Давайте сыграем в игру!""", reply_markup=markup)


@dp.message_handler(content_types=["text"])
async def process_text_command(message: types.Message):
    if message.text.strip() in 'Начать игру':
        # try:
            await start_game(bot, message)    
        # except:
            # await launch_404(bot, message)
    elif message.text.strip() in 'Следующий вопрос':
        try:
            await start_game(bot, message)    
        except:
            await launch_404(bot, message)
    elif message.text.strip() in 'Главное меню':
        try:
            await launch_main_menu(message)
        except:
            await launch_404(bot, message)
    else:
        try:
            await launch_404(bot, message)
        except:
            bot.send_message(chat_id=249792088, text="Опять какая-то хрень")

print('Ready for launch')
executor.start_polling(dp)
