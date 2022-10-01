from aiogram.dispatcher.filters.state import State, StatesGroup

class FSM_Nik(StatesGroup):
  NickName = State()

class FSM_Send_message(StatesGroup):
  Message = State()

class FSM_loading_workDB(StatesGroup):
  subject = State()
  course = State()
  description = State()  
  deadline = State()
  average_price = State()

class FSM_Works_editing_subject(StatesGroup):
  modified_version = State()

class FSM_Works_editing_description(StatesGroup):
  modified_version = State()

class FSM_Works_editing_course(StatesGroup):
  modified_version = State()

class FSM_Works_editing_file(StatesGroup):
  modified_version = State()

class FSM_Works_editing_deadline(StatesGroup):
  modified_version = State()

class FSM_Works_editing_average_price(StatesGroup):
  modified_version = State()