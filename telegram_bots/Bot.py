from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from random import random, randrange, randint


from config import TOKEN

# ---------End------------Of--------------Imports-------------


def readCrocodileLibrary():
    global CrocodileLibrary
    with open("Crocodile_Library.txt", encoding='utf-8') as file:
        for line in file.readlines():
            CrocodileLibrary = CrocodileLibrary + line.split()


def loadCrocodileStatusToDictionary():
    global CrocodileStatusDictionary
    with open("Crocodile_Chats.txt", encoding='utf-8') as file:
        for line in file.readlines():
            ToMakeDictArray = line.split()
            CrocodileStatusDictionary[ToMakeDictArray[0]] = ToMakeDictArray[1]


def saveCrocodileStatusToDictionary():
    global CrocodileStatusDictionary
    CrocodileFile = open('Crocodile_Chats.txt', 'w', encoding='utf-8')
    CrocodileFile.truncate()
    for key in CrocodileStatusDictionary:
        CrocodileFile.write(
            str(key) + " " + str(CrocodileStatusDictionary[key]))
        CrocodileFile.write('\n')
    CrocodileFile.close()


def CrocodileChooseNewWord(PreviousWord):
    global CrocodileLibrary
    cnt = len(CrocodileLibrary)
    NewWord = CrocodileLibrary[randint(0, cnt - 1)]
    while NewWord == PreviousWord:
        NewWord = CrocodileLibrary[randint(0, cnt - 1)]
    return NewWord

# --------PROGRAMM----------STARTS----------HERE------------


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CrocodileLibrary = []
readCrocodileLibrary()

CrocodileStatusDictionary = dict()
loadCrocodileStatusToDictionary()

Crocodilekeyboard = InlineKeyboardMarkup()
Crocodile_menu_1 = InlineKeyboardButton(
    text='Новое Слово', callback_data="crocodile_menu_1")
Crocodile_menu_2 = InlineKeyboardButton(
    text='Посмотреть слово', callback_data="crocodile_menu_2")
Crocodilekeyboard.add(Crocodile_menu_1, Crocodile_menu_2)


CrocodileWinKeyboard = InlineKeyboardMarkup()
Crocodile_win_menu_1 = InlineKeyboardButton(
    text='Хочу быть ведущим!', callback_data="crocodile_win_menu_1")
CrocodileWinKeyboard.add(Crocodile_win_menu_1)


# ----------For_Tg-------Functions-------Right-------Below--------------

@dp.message_handler(commands="startCrocodile")
async def startCrocodileGame(message: types.Message):
    global CrocodileStatusDictionary
    chat_id = str(message.chat.id)
    newWord = CrocodileChooseNewWord("none")
    CrocodileStatusDictionary[chat_id] = str(
        message.from_user.id) + "_" + newWord
    await message.answer(f'<a href="tg://user?id={str(message.from_user.id)}">{str(message.from_user.first_name)}</a> объясняет слово🔥', reply_markup=Crocodilekeyboard, parse_mode="HTML")


@dp.callback_query_handler(text_contains='crocodile_menu_')
async def menu(call: types.CallbackQuery):
    global CrocodileStatusDictionary
    chat_id = str(call.message.chat.id)
    Array = CrocodileStatusDictionary[chat_id].split('_')
    crocodile_master_id, crocodile_word = str(Array[0]), str(Array[1])
    # print(crocodile_master_id + " " + crocodile_word)
    if call.data and call.data.startswith("crocodile_menu_"):
        code = call.data[-1:]
        if code.isdigit():
            code = int(code)
        if code == 1:
            if (str(call.from_user.id) == crocodile_master_id):

                crocodile_new_word = CrocodileChooseNewWord(crocodile_word)
                CrocodileStatusDictionary[chat_id] = str(
                    crocodile_master_id) + "_" + crocodile_new_word

                await bot.answer_callback_query(call.id,
                                                text="Ваше новое слово - " + crocodile_new_word, show_alert=True)
            else:
                await bot.answer_callback_query(call.id,
                                                text="Это слово предназначено не для тебя", show_alert=True)
        elif code == 2:
            if (str(call.from_user.id) == crocodile_master_id):
                await bot.answer_callback_query(call.id,
                                                text="Ваше слово - " + crocodile_word, show_alert=True)
            else:
                await bot.answer_callback_query(call.id,
                                                text="Это слово предназначено не для тебя", show_alert=True)
        else:
            await bot.answer_callback_query(call.id)


@dp.callback_query_handler(text_contains='crocodile_win_menu_')
async def menu(call: types.CallbackQuery):
    global CrocodileStatusDictionary
    chat_id = str(call.message.chat.id)
    newWord = CrocodileChooseNewWord("none")
    if call.data and call.data.startswith("crocodile_win_menu_"):
        code = call.data[-1:]
        if code.isdigit():
            code = int(code)
        if code == 1:
            if (CrocodileStatusDictionary[chat_id] == "none"):
                CrocodileStatusDictionary[chat_id] = str(
                    call.from_user.id) + "_" + newWord
                await bot.answer_callback_query(call.id,
                                                text="Твое слово - " + newWord, show_alert=True)
                await call.message.answer(f'<a href="tg://user?id={str(call.from_user.id)}">{str(call.from_user.first_name)}</a> объясняет слово🔥', reply_markup=Crocodilekeyboard, parse_mode="HTML")
            else:
                await bot.answer_callback_query(call.id,
                                                text="Слово уже загадывают", show_alert=True)


@dp.message_handler(content_types=['text'])
async def echo_message(message: types.Message):
    global CrocodileStatusDictionary
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if (CrocodileStatusDictionary[chat_id] != "none"):
        Array = CrocodileStatusDictionary[chat_id].split('_')
        crocodile_master_id, crocodile_word = str(Array[0]), str(Array[1])
        if (crocodile_word == message.text.lower() and not user_id == crocodile_master_id):
            CrocodileStatusDictionary[chat_id] = "none"
            await message.answer(f'<a href="tg://user?id={str(message.from_user.id)}">{str(message.from_user.first_name)}</a> отгдал(а) слово 🐊',
                                 reply_markup=CrocodileWinKeyboard, parse_mode="HTML")


@dp.message_handler(commands="help")
async def process_help_command(message: types.Message):
    await message.reply("Помощи не будет")

if __name__ == '__main__':
    executor.start_polling(dp)

