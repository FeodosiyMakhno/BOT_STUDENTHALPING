import sqlite3
def sql_request(request):  # функция для sql запросов
  
  atribute = None
  try:
    sqlite_connection = sqlite3.connect('db/client.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("")
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                      Id_user INT NOT NULL PRIMARY KEY,
                      user_name TEXT,
                      surname TEXT,
                      nick_name TEXT,
                      Date_REG TEXT,
                      Date_Last TEXT
    )''')
    sqlite_connection.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS works(
                      ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      Id_userID INT NOT NULL,
                      course INT ,
                      subject TEXT,
                      description TEXT,
                      FILEType TEXT,
                      FILE TEXT,
                      deadline TEXT,
                      average_price TEXT,
                      buy_or_sell TEXT,
                      FOREIGN KEY (Id_userID) references users(Id_user)
    )''')
    sqlite_connection.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS message(
                      ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      Id_sender INT NOT NULL,
                      Id_recipient INT NOT NULL,
                      message TEXT,
                      Id_works INT not null
                      
    )''')
    sqlite_connection.commit()
    cursor.execute(request)
    sqlite_connection.commit()
    atribute = cursor.fetchall()
    cursor.execute("SELECT * FROM users")
    print("USER: ",cursor.fetchall())
    print("\n")
    cursor.execute("SELECT * FROM works")
    print("WORKS: ",cursor.fetchall())
    print("\n")
    cursor.execute("SELECT * FROM message")
    print("MESSAGE: ",cursor.fetchall())

    cursor.close()
  except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
  finally:
    if (sqlite_connection):
      sqlite_connection.close()
    return atribute      

def main():
  pass

if __name__ == "__main__":
  main()