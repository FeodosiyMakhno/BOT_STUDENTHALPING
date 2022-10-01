from aiogram import Dispatcher, types
from aiogram.types import ContentType, MediaGroup
from enum import Enum, auto
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
import keyboards
from create_bot import bot
import config
from .db import sql_request
from .fsm_class import *


class WORKS_DB_NUM(Enum):
    ID: int = 0
    Id_userID: int = auto()
    course: int = auto()
    subject: int = auto()
    description: int = auto()
    FILEType: int = auto()
    FILE: int = auto()
    deadline: int = auto()
    average_price: int = auto()
    buy_or_sell: int = auto()


class MESSAGE_DB_NUM(Enum):
    ID: int = 0
    Id_sender: int = auto()
    Id_recipient: int = auto()
    message: int = auto()
    Id_works = auto()


class __Bot__(
):  # сделанно ради метода со счетчиком, что б позже можно было узнать данные через обьект
    def __init__(self):
        self.counter = 0
        self.mode = None
        self.user_id = None
        self.works_arr = None

    def set_mode(self, mode):
        self.mode = mode

    def get_works(self):
        if self.mode == 'all':
            self.works_arr = self.works_arr = sql_request(f"SELECT * FROM works WHERE NOT Id_userID={self.user_id}")
        else:
            self.works_arr = sql_request(f"SELECT * FROM works WHERE  Id_userID={self.user_id}")
        return self.works_arr

    def next_post(self):
        if (len(self.works_arr) > self.counter + 1):
            self.counter += 1
            return self.counter
        else:
            self.counter = 0
            return self.counter

    def get_message(self):
        return sql_request(f"select * from message where Id_recipient={self.user_id}")

def check_sub_channel(chat_member):  # проверка на подписку
    return chat_member['status'] != 'left'

def checkingNewSubscriber(id_user):  # проверка является ли он новым подписчиком
    return len(sql_request(f"SELECT Id_user FROM users WHERE Id_user = {id_user}")) == 0

def add_nick(id_user, new_nick):  # добавляем ник в базу
    sql_request(f"UPDATE users SET nick_name ='{new_nick}' WHERE Id_user = {id_user}")
def check_none_nick(id_user):  #  проверка есть ли у пользователся ник
    return str(sql_request(f"SELECT nick_name FROM users WHERE Id_user = {id_user}")[0][0]) == 'None'
def date_now():  # возращает сегодняшнюю дату
    return datetime.now().strftime("%d-%m-%y")
def update_last_date(id_user):  # обновляет в базе дату последнего посещения
    sql_request(f"UPDATE users SET Date_Last ='{date_now()}' WHERE Id_user = {id_user}")
def sending_post(num):  # вывод одной работы
    try:
        nik = str(
            sql_request(f'SELECT nick_name FROM users WHERE Id_user={__bot__.get_works()[num][WORKS_DB_NUM.Id_userID.value]}')[0][0])
        return f"<b>Предмет: </b><i>{__bot__.get_works()[num][WORKS_DB_NUM.subject.value]}</i>\n<b>Курс: </b><i>{__bot__.get_works()[num][WORKS_DB_NUM.course.value]} </i>\n<b>Краткое условие: </b><i>{__bot__.get_works()[num][WORKS_DB_NUM.description.value]}</i>\n<b>Дедлайн: </b><i>{__bot__.get_works()[num][WORKS_DB_NUM.deadline.value]}</i>\n<b>Средняя цена за роботу: </b><i>{__bot__.get_works()[num][WORKS_DB_NUM.average_price.value]}</i>\n<b>Ник: </b><i>{nik}</i>"
    except Exception as e:
        print(e)
        return 0
def sending_answer(num):
    try:

        return f"Ответ на пост:\nОписание:{sql_request('SELECT description FROM works WHERE ID= ' + __bot__.get_message[num][MESSAGE_])} {__bot__.get_message[num][MESSAGE_DB_NUM.Id_sender.value]}\n{__bot__.get_message[num][MESSAGE_DB_NUM.message.value]}"
    except Exception as e:
        print("Error answer:", e)
        return 0
__bot__ = __Bot__()

async def process_start_command(message: types.Message):  # старт бота
    update_last_date(message.from_user.id)  # обновляем время посещения
    if checkingNewSubscriber(message.from_user.id):
        sql_request(f"INSERT INTO users VALUES({message.from_user.id} , '{message.from_user.first_name}' ,'{message.from_user.last_name}','None','{date_now()}','{date_now()}')")

    if check_sub_channel(awaitbot.get_chat_member(chat_id=config.ID_CANAL,user_id=message.from_user.id)):
        await bot.send_message(message.chat.id,"<b>Добро пожаловать</b>, {}!\nЯ <b>бот, созданный, чтобы помочь тебе в учебе.</b>".format(message.from_user.first_name))
        await bot.send_message(message.chat.id,"<b>❗️Внимание❗️\n Бот запущен в тестовом режиме работы!</b>")
        if check_none_nick(message.from_user.id):
            await FSM_Nik.NickName.set()
            await bot.send_message(message.from_user.id,"<b>Для того что б продолжить, придумай себе  псевдоним(nick):</b>",reply_markup=types.ReplyKeyboardRemove())
        else:
            await bot.send_message(message.from_user.id,"<b>✅Вы вошли в свой кабинет...</b>",reply_markup=keyboards.kb_menu)
    else:
        await bot.send_message(message.from_user.id,"<b>Для доступа к функционалу бота,</b>подпишитесь на канал: <a href='https://t.me/+2WGaikjHOPxhYTAy'>MamItsCrimin</a> ")
    update_last_date(message.from_user.id)  # обновляем время посещения
async def cancel_handler(message: types.Message, state: FSMContext):  # хендлер для того что останавливать машину состояний
    if await state.get_state() is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id,"<b>Процесс отменен❗</b>",reply_markup=keyboards.kb_menu)
async def AddNickNameDB(message: types.Message,state: FSMContext):  # добавление введного ника в базу
    update_last_date(message.from_user.id)  # обновляем время посещения
    add_nick(message.from_user.id, message.text)
    await bot.send_message(message.from_user.id, "<b>Ник добавлен...</b>")
    await bot.send_message(message.from_user.id,"<b>✅Вы вошли в свой кабинет...</b>",reply_markup=keyboards.kb_menu)
    await state.finish()
async def FSM_loading_workDB_start(message: types.Message,state=None):  # загрузка роботы в базу
    update_last_date(message.from_user.id)  # обновляем время посещения
    await FSM_loading_workDB.subject.set()
    await bot.send_message(message.from_user.id,"<b>Введи по какому предмету у вас задание:</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_loading_workDB_subject(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await FSM_loading_workDB.next()
    await bot.send_message(message.from_user.id,"<b>На какой курсе обучаешься: </b>")
async def FSM_loading_workDB_course(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['course'] = message.text
    await FSM_loading_workDB.next()
    await bot.send_message(message.from_user.id,"<b>Скинь файл, фото,видео,архив с заданием, или введи описание задания: </b>")
async def FSM_loading_workDB_description(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == 'text':
            data['description'] = message.text
            try:
                check = data['FILEType']
            except:
                data['FILEType'] = 'None'
                data['FILE'] = 'None'
                await FSM_loading_workDB.next()
                await bot.send_message(message.from_user.id,"<b>Введите дедлайн для своей роботы:</b>")
        elif message.content_type == 'document':
            data['FILE'] = message.document.file_id
            data['FILEType'] = 'DOCUMENT'
            await bot.send_message(message.from_user.id,"<b>✅Файл загружен..</b>")
            await FSM_loading_workDB.description.set()
            await bot.send_message(message.from_user.id,"<b>Введите краткое условие,\nтип задания(примеры, задача, лаб.),количество заданий:</b>")
        elif message.content_type == 'photo':
            data['FILE'] = message.photo[-1].file_id
            data['FILEType'] = 'PHOTO'
            await bot.send_message(message.from_user.id,"<b>✅Фото загружено..</b>")
            await bot.send_message(message.from_user.id,"<b>Введите краткое условие,\nтип задания(примеры, задача, лаб.),количество заданий:</b>")
            await FSM_loading_workDB.description.set()
        elif message.content_type == 'video':
            data['FILE'] = message.video.file_id
            data['FILEType'] = 'VIDEO'
            await bot.send_message(message.from_user.id,"<b>✅Видео загружено..</b>")
            await FSM_loading_workDB.description.set()
            await bot.send_message(message.from_user.id,"<b>Введите краткое условие,\nтип задания(примеры, задача, лаб.),количество заданий:</b>")
        else:
            await bot.send_message(message.from_user.id, "<b>Ошибка❗</b>")
            await FSM_loading_workDB.description.set()
            await bot.send_message(message.from_user.id,"<b>Введите еще раз:</b>")
async def FSM_loading_workDB_deadline(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['deadline'] = message.text
    await FSM_loading_workDB.next()
    await bot.send_message(message.from_user.id,"<b>На какую сумму вы рассчитываете:</b>")
async def FSM_loading_workDB_average_price(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['average_price'] = message.text
    await state.finish()
    sql_request(f"INSERT INTO works(Id_userID,course,subject,description,FILEType,FILE,deadline,average_price,buy_or_sell) VALUES({message.from_user.id}, '{data['course']}','{data['subject']}','{data['description']}','{data['FILEType']}','{data['FILE']}','{data['deadline']}', '{data['average_price']}', 'BUY' )")
    await bot.send_message(message.from_user.id,"✅Зазрузка прошла успешно",reply_markup=keyboards.kb_menu)
    __bot__ = __Bot__()
async def Output_Works(message: types.Message):
    update_last_date(message.from_user.id)  # обновляем время посещения
    __bot__.user_id = message.from_user.id
    __bot__.set_mode("all")
    if len(__bot__.get_works()) != 0:
        await bot.send_message(message.from_user.id,"🗒️ <b>Список заданий:</b>",reply_markup=keyboards.kb_return_menu)
        await bot.send_message(message.from_user.id,sending_post(0),reply_markup=keyboards.inline_client)
    else:
        await bot.send_message(message.from_user.id,"<b>Работ пока что нет, зайдите позже❗️</b>",reply_markup=keyboards.kb_menu)
async def Output_My_Works(message: types.Message):
    update_last_date(message.from_user.id)  # обновляем время посещения
    __bot__.user_id = message.from_user.id
    __bot__.set_mode("one")
    if len(__bot__.get_works()) != 0:
        await bot.send_message(message.from_user.id,"<b>🗒️ Список заданий:</b>",reply_markup=keyboards.kb_return_menu)
        await bot.send_message(message.from_user.id,sending_post(0),reply_markup=keyboards.inline_my_post)
    else:
        await bot.send_message(message.from_user.id,"<b>Вы еще не выкладывали работы❗️</b>",reply_markup=keyboards.kb_client_my_works)
async def InlineB_save_post(callback: types.CallbackQuery):
    await callback.answer("<b>Пост сохранен✅(а если честно, то пока что нет)</b>")
    await callback.answer()
async def InlineB_next_post(callback: types.CallbackQuery):
    if len(__bot__.get_works()) != 1:
        await callback.message.delete()
        if __bot__.mode == "all":
            await callback.message.answer(sending_post(__bot__.next_post()),reply_markup=keyboards.inline_client)
        else:
            await callback.message.answer(sending_post(__bot__.next_post()),reply_markup=keyboards.inline_my_post)
        await callback.answer()
    else:
        await callback.answer("❗️Больше постов нету❗️")
async def InlineB_write_client(callback: types.CallbackQuery):
    await FSM_Send_message.Message.set()
    await callback.message.answer("<b>Введите сообщение:</b>",reply_markup=keyboards.kb_client_cancel)
    await callback.answer()
async def FSM_write_client(message: types.Message, state: FSMContext):
    update_last_date(message.from_user.id)  # обновляем время посещения
    sql_request(f"INSERT INTO message(Id_sender,Id_recipient,message,Id_works) VALUES({message.from_user.id},{__bot__.works_arr[__bot__.counter][WORKS_DB_NUM.Id_userID.value]},'{message.text}',{__bot__.works_arr[__bot__.counter][WORKS_DB_NUM.id.value]})")
    await bot.send_message(message.from_user.id,"<b>✅Cобщение отправлено</b>",reply_markup=keyboards.kb_menu)
    await state.finish()
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Menu_main_menu(message: types.Message):  # хендлер для кнопки в главное меню
    await bot.send_message(message.from_user.id,"<b>📋 Главное меню:</b>",reply_markup=keyboards.kb_menu)
async def Menu_my_works(message: types.Message):
    await bot.send_message(message.from_user.id,"<b>📝 Мои задания:</b>",reply_markup=keyboards.kb_client_my_works)
async def Inline_send_file(callback: types.CallbackQuery):
    if __bot__.get_works()[__bot__.counter][WORKS_DB_NUM.FILEType.value] == "DOCUMENT":
        await callback.message.delete()
        await callback.message.answer_document(
            __bot__.get_works()[__bot__.counter][WORKS_DB_NUM.FILE.value],
            caption="<b>Файл с заданием </b>",
            reply_markup=keyboards.inline_close_post_file)
    elif __bot__.get_works()[__bot__.counter][
            WORKS_DB_NUM.FILEType.value] == "PHOTO":
        await callback.message.delete()
        await callback.message.answer_photo(__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.FILE.value],"<b>Фото с заданием </b>",reply_markup=keyboards.inline_close_post_file)
    else:
        await callback.answer("❗️Файл не прикрепляли❗️")
    await callback.answer()
async def Inline_delete_postDB(callback: types.CallbackQuery):
    await callback.message.delete()
    sql_request(f"delete from works WHERE ID='{__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}'")
    if len(__bot__.get_works()) != 0:
        await callback.message.answer(sending_post(0),reply_markup=keyboards.inline_my_post)
        await callback.answer("✅Пост удален")
    else:
        await callback.message.answer("<b>✅Пост удален</b>", reply_markup=keyboards.kb_client_my_works)
async def Inline_Close_Post_File(callback: types.CallbackQuery):
    __bot__.user_id = callback.from_user.id
    await callback.message.delete()
    if __bot__.mode == "all":
        await callback.message.answer(sending_post(__bot__.counter),reply_markup=keyboards.inline_client)
    else:
        await callback.message.answer(sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    await callback.answer()
async def Inline_Edit_Post(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("<b>Выберите какие данные вы хотите изменить:</b>",reply_markup=keyboards.Inline_select_edit_buttons)
async def Inline_Edit_subject(callback: types.CallbackQuery, state=None):
    await callback.message.delete()
    await FSM_Works_editing_subject.modified_version.set()
    await callback.message.answer("<b>Введите измененный вариант</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_Edit_subject(message: types.Message, state: FSMContext):
    sql_request(f"update works set subject = '{message.text}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
    await state.finish()
    await bot.send_message(message.from_user.id, "<b>✅Данные изменены</b>")
    await bot.send_message(message.from_user.id,sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Inline_Edit_description(callback: types.CallbackQuery):
    await callback.message.delete()
    await FSM_Works_editing_description.modified_version.set()
    await callback.message.answer("<b>Введите измененный вариант</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_Edit_description(message: types.Message, state: FSMContext):
    sql_request(f"update works set description = '{message.text}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
    await state.finish()
    await bot.send_message(message.from_user.id, "<b>✅Данные изменены</b>")
    await bot.send_message(message.from_user.id,sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Inline_Edit_file(callback: types.CallbackQuery):
    await callback.message.delete()
    await FSM_Works_editing_file.modified_version.set()
    await callback.message.answer("<b>Cкинь измененый файл</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_Edit_file(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        sql_request(f"update works set FILE = '{message.document.file_id}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.FILE.value]}")
        sql_request(f"update works set FILEType = 'DOCUMENT' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.FILEType.value]}")
        await state.finish()
    elif message.content_type == 'photo':
        sql_request(f"update works set FILE = '{message.photo[-1].file_id}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
        sql_request(f"update works set FILEType = 'PHOTO' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
        await state.finish()
    elif message.content_type == 'video':
        sql_request(f"update works set FILE = '{message.video.file_id}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.FILE.value]}")
        sql_request(f"update works set FILEType = 'VIDEO' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "<b>Ошибка❗</b>")
        await FSM_Works_editing_file.modified_version.set()
        await bot.send_message(message.from_user.id, "<b>Скинь еще раз:</b>")
        return
    await bot.send_message(message.from_user.id, "<b>✅Данные изменены</b>")
    await bot.send_message(message.from_user.id,sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Inline_Edit_deadline(callback: types.CallbackQuery):
    await callback.message.delete()
    await FSM_Works_editing_deadline.modified_version.set()
    await callback.message.answer("<b>Введите измененный вариант</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_Edit_deadline(message: types.Message, state: FSMContext):
    sql_request(f"update works set deadline = '{message.text}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
    await state.finish()
    await bot.send_message(message.from_user.id, "<b>✅Данные изменены</b>")
    await bot.send_message(message.from_user.id,sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Inline_Edit_average_price(callback: types.CallbackQuery):
    await callback.message.delete()
    await FSM_Works_editing_average_price.modified_version.set()
    await callback.message.answer("<b>Введите измененный вариант</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_Edit_average_price(message: types.Message, state: FSMContext):
    sql_request(f"update works set average_price = '{message.text}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
    await state.finish()
    await bot.send_message(message.from_user.id, "<b>✅Данные изменены</b>")
    await bot.send_message(message.from_user.id,sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Inline_Edit_course(callback: types.CallbackQuery):
    await callback.message.delete()
    await FSM_Works_editing_course.modified_version.set()
    await callback.message.answer("<b>Введите измененный вариант</b>",reply_markup=keyboards.kb_client_cancel)
async def FSM_Edit_Edit_course(message: types.Message, state: FSMContext):
    sql_request(f"update works set course = '{message.text}' where ID={__bot__.get_works()[__bot__.counter][WORKS_DB_NUM.id.value]}")
    await state.finish()
    await bot.send_message(message.from_user.id, "<b>✅Данные изменены</b>")
    await bot.send_message(message.from_user.id,sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
    update_last_date(message.from_user.id)  # обновляем время посещения
async def Inline_Edit_back(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(sending_post(__bot__.counter),reply_markup=keyboards.inline_my_post)
async def Answers_tasks(message: types.Message):  # ответы на ваши выставленые работы
    update_last_date(message.from_user.id)  # обновляем время посещения
    __bot__.id_user = message.from_user.id
    messages_answer = __bot__.get_message()
    print(messages_answer)
    if (len(messages_answer)):
        await bot.send_message(message.from_user.id,"<b>Ответы на ваши посты 🙋:</b>",reply_markup=keyboards.kb_return_menu)
        for message_answer in messages_answer:
            id_user = sql_request(f"select Id_sender from message WHERE message = '{message_answer[0]}' ")[0][0]
            await bot.send_message(sending_answer(0),reply_markup=keyboards.inline_message_check)
    else:
        await bot.send_message(message.from_user.id,"<b>Вам никто не отвечал❗️</b>",reply_markup=keyboards.kb_menu)

# async def Output_My_Answers_tasks

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands="Отмена")
    dp.register_message_handler(cancel_handler,Text(equals="❌Отмена", ignore_case=True),state="*")
    dp.register_message_handler(Menu_main_menu, Text(equals='⬅️ Главное меню'))
    dp.register_message_handler(Answers_tasks, Text(equals='✉️ Ответы'))
    dp.register_message_handler(Output_Works, Text(equals='🔍 Найти задание'))
    dp.register_message_handler(Menu_my_works, Text(equals='📝 Мои задания'))
    dp.register_message_handler(Output_My_Works,Text(equals='🗄️ Просмотр моих заданий'))
    dp.register_message_handler(process_start_command,commands=['start'],state=None)
    dp.register_message_handler(AddNickNameDB, state=FSM_Nik.NickName)
    dp.register_message_handler(FSM_loading_workDB_start,Text(equals='⬇️ Загрузить работу'),state=None)
    dp.register_message_handler(FSM_loading_workDB_subject,state=FSM_loading_workDB.subject)
    dp.register_message_handler(FSM_loading_workDB_course,state=FSM_loading_workDB.course)
    dp.register_message_handler(FSM_loading_workDB_description,state=FSM_loading_workDB.description)
    dp.register_message_handler(FSM_loading_workDB_description,content_types=ContentType.DOCUMENT,state=FSM_loading_workDB.description)
    dp.register_message_handler(FSM_loading_workDB_description,content_types=ContentType.PHOTO,state=FSM_loading_workDB.description)
    dp.register_message_handler(FSM_loading_workDB_description,content_types=ContentType.VIDEO,state=FSM_loading_workDB.description)
    dp.register_message_handler(FSM_loading_workDB_deadline,state=FSM_loading_workDB.deadline)
    dp.register_message_handler(FSM_loading_workDB_average_price,state=FSM_loading_workDB.average_price)
    dp.register_message_handler(FSM_write_client,state=FSM_Send_message.Message)
    dp.register_message_handler(FSM_Edit_subject, state=FSM_Works_editing_subject.modified_version)
    dp.register_message_handler(FSM_Edit_description,state=FSM_Works_editing_description.modified_version)
    dp.register_message_handler(FSM_Edit_subject, state=FSM_Works_editing_subject.modified_version)
    dp.register_message_handler(FSM_Edit_file,content_types=ContentType.DOCUMENT,state=FSM_Works_editing_file.modified_version)
    dp.register_message_handler(FSM_Edit_file,content_types=ContentType.PHOTO,state=FSM_Works_editing_file.modified_version)
    dp.register_message_handler(FSM_Edit_file,content_types=ContentType.VIDEO,state=FSM_Works_editing_file.modified_version)
    dp.register_message_handler(FSM_Edit_file,state=FSM_Works_editing_file.modified_version)
    dp.register_message_handler(FSM_Edit_deadline,state=FSM_Works_editing_deadline.modified_version)
    dp.register_message_handler(FSM_Edit_average_price,state=FSM_Works_editing_average_price.modified_version)
    dp.register_message_handler(FSM_Edit_Edit_course, state=FSM_Works_editing_course.modified_version)
    dp.register_callback_query_handler(InlineB_save_post, text="save_post")
    dp.register_callback_query_handler(InlineB_next_post, text="next_post")
    dp.register_callback_query_handler(InlineB_write_client,text="write_client")
    dp.register_callback_query_handler(Inline_send_file, text="show_file")
    dp.register_callback_query_handler(Inline_delete_postDB,text="delete_post")
    dp.register_callback_query_handler(Inline_Close_Post_File,text="close_post_file")
    dp.register_callback_query_handler(Inline_Edit_Post,text="edit_post")
    dp.register_callback_query_handler(Inline_Edit_subject,text="edit_subject",state=None)
    dp.register_callback_query_handler(Inline_Edit_description,text="edit_description",state=None)
    dp.register_callback_query_handler(Inline_Edit_file,text="edit_file",state=None)
    dp.register_callback_query_handler(Inline_Edit_deadline,text="edit_deadline")
    dp.register_callback_query_handler(Inline_Edit_average_price,text="edit_average_price")
    dp.register_callback_query_handler(Inline_Edit_back, text="back")
    dp.register_callback_query_handler(Inline_Edit_course, text="edit_course")
