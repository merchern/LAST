from loader import bot, dp
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from database.db import Database

import handlers.admin.am_main as kb
from FSM import fsm_machine as fsm

db = Database('database/data.db')

@dp.message_handler(Command('adm'))
async def main_admin(message: Message):
    if db.check_adm_access(message.from_user.id):
        await bot.send_message(message.from_user.id, "ты зашел как админ. завидую", reply_markup=kb.main)
    else:
        await bot.send_message(message.from_user.id, "ты не админ сиди на юзерке хули ты хочешь")

@dp.message_handler(lambda message: message.text == "Предложка")
async def check_amenu(message: Message):
    if(not db.check_adm_access(message.from_user.id)):
        pass
    else:
        await bot.send_message(message.from_user.id, "Чтобы одобрить/отклонить пост - нажми на соответствующую кнопку и следуй "
                                                         "указаниям бота, пон?", reply_markup=kb.requests_check)
        
@dp.message_handler(lambda message: message.text == "Запросы на удаление")
async def check_amenu(message: Message):
    if(not db.check_adm_access(message.from_user.id)):
        pass
    else:
        await bot.send_message(message.from_user.id, "Чтобы одобрить/отклонить запрос на удаление - нажми на соответствующую кнопку и следуй "
                                                         "указаниям бота, пон?", reply_markup=kb.requestsdel_check)


@dp.message_handler(lambda message: message.text == "Отклонить")
async def check_post_denied(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "<b>Сейчас введи ID поста, который хочешь отклонить</b>")
    await state.set_state(fsm.PublicationDenied.ID)

@dp.message_handler(lambda message: message.text == "Одобрить удаление")
async def check_post_accepted(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "<b>Введи ИД заявки, которую хочешь рассмотреть</b>")
    await state.set_state(fsm.DeleteRequestCheckAccept.ID)

@dp.message_handler(lambda message: message.text == "Отклонить удаление")
async def check_post_denied(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "<b>Введи ИД заявки, которую нужно удалить из БД</b>")
    await state.set_state(fsm.DeleteRequestCheckDenied.ID)

@dp.message_handler(lambda message: message.text == "Одобрить")
async def check_post_accepted(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "<b>Сейчас введи ID поста, который хочешь одобрить</b>")
    await state.set_state(fsm.PublicationAccept.ID)

@dp.message_handler(lambda message: message.text == "Назад")
async def button_back(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "ок..", reply_markup=kb.main)

#post accepted
async def accept_load_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await message.answer("С голосованием/без?", reply_markup=kb.y_n)
    await state.set_state(fsm.PublicationAccept.VOTE)

async def accept_load_vote(message: Message, state: FSMContext):
    if message.text == "Да":
        async with state.proxy() as data:
            data['vote'] = True
    elif message.text == "Нет":
        async with state.proxy() as data:
            data['vote'] = False

    await state.finish()
    await message.answer("Пост успешно опубликован!", reply_markup=kb.main)
    await db.accept_post(data['id'], data['vote'])


#post denied
async def denied_load_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await message.answer("Теперь введи причину отклонения")
    await state.set_state(fsm.PublicationDenied.REASON)

async def denied_load_reason(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    await message.answer("Теперь выбери, банить пользователя, который предложил пост, или нет", reply_markup=kb.y_n)
    await state.set_state(fsm.PublicationDenied.BANNED)

async def denied_load_banned(message: Message, state: FSMContext):
    if message.text == "Да":
        async with state.proxy() as data:
            data['banned'] = True
    elif message.text == "Нет":
        async with state.proxy() as data:
            data['banned'] = False
    await message.answer("Пост удален из БД", reply_markup=kb.main)
    await db.denied_post(data['id'], data['reason'], data['banned'])
    await state.finish()


#request remove accepted
async def reqdel_accept_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    value = True
    await message.answer("Удали пост, ссылка на который была прикреплена к заявке", reply_markup=kb.main)
    await db.request_remove_del(data['id'], value)
    await state.finish()

async def reqdel_denied_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    value = False
    await message.answer("Заявка успешно отклонена", reply_markup=kb.main)
    await db.request_remove_del(data['id'], value)
    await state.finish()