from loader import bot, dp
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from FSM import fsm_machine as fsm
from database.db import Database

import handlers.client.clm_main as kb
import handlers.admin.am_main as kba

db = Database('database/data.db')


@dp.message_handler(commands=['start', 'help'])
async def start(message: Message, state: FSMContext):
    if(not db.user_exists(message.from_user.id)):
        db.reg_user(message.from_user.id, message.from_user.full_name)
        await bot.send_message(message.from_user.id, "добавлен в БД нахуй.", reply_markup=kb.main)
    else:
        await bot.send_message(message.from_user.id, "хуй.", reply_markup=kb.main)

@dp.message_handler()
async def check_menu(message: Message, state: FSMContext):
    if message.text == "Личный кабинет":
        res = await db.get_user_info(message.from_user.id)
        await bot.send_message(message.from_user.id, res)
    if message.text == "Предложить запись":
        await state.set_state(fsm.PublicationRequest.NAME)
        await message.answer("Напиши как тебя зовут.")
    if message.text == "Запрос на удаление":
        await state.set_state(fsm.DeleteRequest.NAME)
        await bot.send_message(message.from_user.id, "Напиши как тебя зовут")



async def load_name(message: Message, state: FSMContext):
    if message.photo or message.video:
        await message.answer("Имя пиши, а не фотки или видео скидывай.")
    else:
        async with state.proxy() as data:
            data['name'] = message.text

        await message.answer("Теперь пиши имя владельца фотографии, желательно с сыллками на соц.сети и остальное.")
        await state.set_state(fsm.PublicationRequest.OWN)

async def load_own(message: Message, state: FSMContext):
    if message.photo or message.video:
        await message.answer("Владельца пиши, тупень. Фотки/видео - потом.")
    else:
        async with state.proxy() as data:
            data['own'] = message.text

        await message.answer("Теперь выбирай тип файла, который кидать будешь.", reply_markup=kb.file_type)
        await state.set_state(fsm.PublicationRequest.FILE_TYPE)

async def load_filetype(message: Message, state: FSMContext):
    if message == message.photo or message.video:
        await message.answer("НА КНОПОЧКУ НАЖМИ СНИЗУ БЛЯЯЯ, ВИДЕО ИЛИ ФОТО")
    else:
        if message.text == "Фото":
            async with state.proxy() as data:
                data['file_type'] = 'photo'
            await message.answer("Теперь кидай фото.")
            await state.set_state(fsm.PublicationRequest.PHOTO)
        elif message.text == "Видео":
            async with state.proxy() as data:
                data['file_type'] = 'video'
            await message.answer("Теперь кидай видео.")
            await state.set_state(fsm.PublicationRequest.VIDEO)

async def load_photo(message: Message, state: FSMContext):
    if message == message.video:
        await message.answer("ты фото вроде выбрал, нахуя ты мне видео кидаешь?? бот сломается так, ты чинить будешь бля?!1")
    else:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await message.answer("твоя заявка отправлена администраторам, показывать тебе я её не буду, так как это грузит ОЗУ сервера, жди.", reply_markup=kb.main)
        await db.request_photo(message.from_user.id, data['name'], data['own'], data['photo'], data['file_type'])
        await state.finish()

async def load_video(message: Message, state: FSMContext):
    if not message.video:
        await message.answer("ты видео вроде выбрал, нахуя ты мне фото кидаешь?? бот сломается так, ты чинить будешь бля?!1")
    else:
        async with state.proxy() as data:
            data['video'] = message.video.file_id
            await message.answer("твоя заявка отправлена администраторам, показывать тебе я её не буду, так как это грузит ОЗУ сервера, жди.", reply_markup=kb.main)
        await db.request_video(message.from_user.id, data['name'], data['own'], data['video'], data['file_type'])
        await state.finish()


async def delreq_load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Теперь скинь ссылку на пост, который нужно удалить")
    await state.set_state(fsm.DeleteRequest.POST_ID)

async def delreq_load_postid(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['postid'] = message.text
    await message.answer("Теперь введи причину удаления, подробно")
    await state.set_state(fsm.DeleteRequest.REASON)

async def delreq_load_reason(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    await message.answer("Твоя заявка успешно отправлена. Жди")
    await db.request_remove(message.from_user.id, message.from_user.full_name, data['postid'], data['reason'])
    await state.finish()