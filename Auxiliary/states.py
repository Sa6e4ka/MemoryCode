from aiogram.fsm.state import State, StatesGroup


class Start(StatesGroup):
    start = State()
    
    reset = State()
    
    register_name = State()
    register_mail = State()
    register_phone = State()

    login_mail = State()
    login_password = State()


class Page(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    state9 = State()
    state10 = State()
    state10 = State()
    state11 = State()
    state12 = State()
    state13 = State()
    state14 = State()
    state15 = State()
    state16 = State()

class Page18(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    state9 = State()
    state10 = State()

class Page45(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    state9 = State()
    state10 = State()

class Page60(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    state9 = State()
    state10 = State()



class PageWAR(StatesGroup):
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()
    state8 = State()
    state9 = State()
    state10 = State()

class Free(StatesGroup):
    state1 = State()
    state2 = State()


class Contact(StatesGroup):
    name = State()
    phone = State()
    mail = State()
    q_category = State()
    question = State()