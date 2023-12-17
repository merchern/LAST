from aiogram.dispatcher.filters.state import State, StatesGroup


class PublicationRequest(StatesGroup):
    NAME = State()
    OWN = State()
    FILE_TYPE = State()
    PHOTO = State()
    VIDEO = State()


class PublicationAccept(StatesGroup):
    ID = State()
    VOTE = State()

class PublicationDenied(StatesGroup):
    ID = State()
    REASON = State()
    BANNED = State()


class DeleteRequest(StatesGroup):
    NAME = State()
    POST_ID = State()
    REASON = State()

class DeleteRequestCheckAccept(StatesGroup):
    ID = State()

class DeleteRequestCheckDenied(StatesGroup):
    ID = State()