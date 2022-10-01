
from aiogram.utils import executor
from create_bot import dp,bot
from handlers import client
import config
import keyboards 


async def on_startup(_):
  await bot.send_message(config.ID_USERTWO,"Bot Include..", reply_markup=keyboards.kb_menu)
  print("BOT CONNECTS")

client.register_handlers_client(dp)




executor.start_polling(dp,skip_updates=True,on_startup=on_startup)