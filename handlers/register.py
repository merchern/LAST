from loader import bot, dp
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from FSM import fsm_machine as fsm

from handlers.client import cl_main as client
from handlers.admin import adm_main as admin


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(client.check_menu, state=None)
    dp.register_message_handler(client.load_name, state=fsm.PublicationRequest.NAME)
    dp.register_message_handler(client.load_own, state=fsm.PublicationRequest.OWN)
    dp.register_message_handler(client.load_filetype, state=fsm.PublicationRequest.FILE_TYPE)
    dp.register_message_handler(client.load_video, content_types=['video'], state=fsm.PublicationRequest.VIDEO)
    dp.register_message_handler(client.load_photo, content_types=['photo'], state=fsm.PublicationRequest.PHOTO)
    dp.register_message_handler(client.delreq_load_name, state=fsm.DeleteRequest.NAME)
    dp.register_message_handler(client.delreq_load_postid, state=fsm.DeleteRequest.POST_ID)
    dp.register_message_handler(client.delreq_load_reason, state=fsm.DeleteRequest.REASON)
    dp.register_message_handler(admin.accept_load_id, state=fsm.PublicationAccept.ID)
    dp.register_message_handler(admin.accept_load_vote, state=fsm.PublicationAccept.VOTE)
    dp.register_message_handler(admin.denied_load_id, state=fsm.PublicationDenied.ID)
    dp.register_message_handler(admin.denied_load_reason, state=fsm.PublicationDenied.REASON)
    dp.register_message_handler(admin.denied_load_banned, state=fsm.PublicationDenied.BANNED)
    dp.register_message_handler(admin.reqdel_accept_id, state=fsm.DeleteRequestCheckAccept.ID)
    dp.register_message_handler(admin.reqdel_accept_id, state=fsm.DeleteRequestCheckDenied.ID)