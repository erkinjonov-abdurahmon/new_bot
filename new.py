from aiogram import types, executor, Bot, Dispatcher
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import re 
from aiogram.contrib.fsm_storage.memory import MemoryStorage




TOKEN = '6437566680:AAFWvs2sX266yqe4Jq-iV4-4iuxy_dGvIxI'
bot = Bot(token=TOKEN)
API_KEY = "60fd1e65ebc143ee3e6547821b5d53d1"
dp = Dispatcher(bot=bot)

storage = MemoryStorage()

PHONE_PATTERN = re.compile ("^\+998[0-9]{9}")

class Info(StatesGroup):
    name = State()
    phone_number = State()
    age = State()
    email = State()


buttons = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton(text="kanal 1", callback_data="kanal")
btn2 = InlineKeyboardButton(text="Obuna bo'ldim", callback_data="tekshirish")
buttons.add(btn1)
buttons.add(btn2)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # await message.answer("Iltimos shu kanalga obuna bo'ling", reply_markup=buttons)
    await message.answer(text="Ismingizni kiriting")
    await Info.name.set()

# @dp.callback_query_handler()
# async def is_subscribe_to_channel(callback_data: types.CallbackQuery):
#     channel_username = "Abdurahmon"
#     bot_user = await bot.get_me("https://t.me/lsjkflsjfknvk")
#     try:
#         member = await bot.get_chat_member(channel_username, bot_user.id)
#         if member.status in [types.ChatMemberStatus.ADMINISTRATOR, types.ChatMemberStatus.CREATOR, types.ChatMemberStatus.MEMBER]:
#             print("Bot is a member of the channel.")
#         else:
#             print("Bot is not a member of the channel.")
#     except Exception as e:
#         print(f"Error: {e}")

@dp.message_handler(state=Info.name)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text="Telefon raqamingizni kiriting")
    await Info.next()




@dp.message_handler(state=Info.phone_number)
async def set_phone(message:types.Message, state:FSMContext):
    await state.update_data(phone_number = message.text)
    await message.answer(text='yoshigizni kiriting')
    await Info.next()


@dp.message_handler(state=Info.age)
async def set_age(message:types.Message, state:FSMContext):
    await state.update_data(age = message.text)
    await message.answer(text='pochtangizni kiriting:')
    await Info.next()

btn = ReplyKeyboardMarkup()
btn.add("Ha", "Yo'q")

@dp.message_handler(state=Info.email)
async def set_email(message:types.Message, state:FSMContext):
    await state.update_data(email = message.text)
    data = await state.get_data()
    await message.answer(text=f"Ism: {data['name']}, Telefon raqam: {data['phone_number']}, Yosh: {data['age']}, email: {data['email']}", reply_markup=btn)
    await message.answer(text="Ha ni bossangiz malumotlaringiz adminga ketadi")
    await state.finish()






if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)