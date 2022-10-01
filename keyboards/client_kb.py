from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup


kb_menu=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('📝 Мои задания'),KeyboardButton('🔍 Найти задание')).add(KeyboardButton('✉️ Ответы'))

kb_client_cancel=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('❌Отмена'))

inline_client=InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text="Сохранить",callback_data='save_post'),InlineKeyboardButton(text="Написать",callback_data='write_client')).add(InlineKeyboardButton(text="Получить файл",callback_data='show_file')).add(InlineKeyboardButton(text="Слeдующий пост",callback_data='next_post'))

kb_return_menu=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('⬅️ Главное меню'))

inline_message_check=InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text="Закрепить задание на нем",callback_data='progress'),InlineKeyboardButton(text="Написать",callback_data='write_client')).add(InlineKeyboardButton(text="Удалить смс",callback_data='delete message'))

kb_client_my_works=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('⬇️ Загрузить работу')).add(KeyboardButton('🗄️ Просмотр моих заданий')).add(KeyboardButton('⬅️ Главное меню'))

kb_client_cancel_and_loading_file = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('⬇️Загрузить файл'),KeyboardButton('❌Отмена'))

inline_close_post_file=InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text="Закрыть файл",callback_data='close_post_file'))

inline_my_post=InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text="Удалить",callback_data='delete_post'),InlineKeyboardButton(text="Редактировать",callback_data='edit_post')).add(InlineKeyboardButton(text="Получить файл",callback_data='show_file')).add(InlineKeyboardButton(text="Слeдующий пост",callback_data='next_post'))



Inline_select_edit_buttons=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="📕Предмет📓",callback_data='edit_subject')).add(InlineKeyboardButton(text="🏫Курс🗓️",callback_data='edit_course')).add(InlineKeyboardButton(text="📝Описание📝",callback_data='edit_description')).add(InlineKeyboardButton(text="📁Файл💿",callback_data='edit_file')).add(InlineKeyboardButton(text="⏳Дедлайн🕐",callback_data='edit_deadline')).add(InlineKeyboardButton(text="💵Относительная цена💰",callback_data='edit_average_price')).add(InlineKeyboardButton(text="⬅️Назад",callback_data='back'))