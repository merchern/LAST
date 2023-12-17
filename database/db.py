import random
import sqlite3
from loader import bot


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def reg_user(self, user_id, user_name):
        with self.connection:
            self.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (user_id, user_name, 0, 0,))

    def user_exists(self, user_id):
        with self.connection:
            data = self.cursor.execute("SELECT userid FROM users WHERE userid = ?", (user_id,)).fetchall()
            return bool(len(data))

    def check_adm_access(self, user_id):
        with self.connection:
            data_adm = self.cursor.execute("SELECT admin_id FROM admins WHERE admin_id = ?", (user_id,)).fetchall()
            return bool(len(data_adm))

    async def get_user_info(self, user_id):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM users WHERE userid = ?", (user_id,)).fetchall()

            for rows in data:
                if rows[3] == 0:
                    await bot.send_message(user_id, f"ID аккаунта: {rows[0]}\n"
                                                    f"Имя аккаунта: {rows[1]}\n"
                                                    f"Одобренных постов: {rows[2]}")
                elif rows[3] == 1:
                    await bot.send_message(user_id, "ты в бане аряя. доступен только запрос на удаление поста. если хочешь оспорить блокировку - пиши в поддержку")
                elif rows[3] == 2:
                    await bot.send_message(user_id, f"бан от @merchern . Пиши в лс, если тебя интересует причина. Сразу кидай свой ИД: {user_id}")


    async def request_photo(self, user_id, user_name, own, file_id, file_type):
        with self.connection:
            rand_id = random.randint(1, 999)
            data = self.cursor.execute("SELECT user_id FROM requests WHERE user_id = ?", (user_id,)).fetchall()
            admins = self.cursor.execute("SELECT admin_id FROM admins").fetchall()

            if not data:
                self.cursor.execute("INSERT INTO requests VALUES(?, ?, ?, ?, ?, ?)", (rand_id, user_id, user_name, own, file_id, file_type,))

                for res in admins:
                    await bot.send_photo(*res, file_id, caption=f"<b>Новая заявка на публикацию</b>\n\n"
                                                 f"ИД заявки: {rand_id}\n"
                                                 f"ИД отправителя: {user_id}\n"
                                                 f"Имя отправителя: {user_name}\n"
                                                 f"Имя владельца фото, возможно, контакты: {own}\n"
                                                 f"Тип файла: {file_type}\n")
            else:
                await bot.send_message(user_id, "у тебя уже висит одна заявка, жди пока её рассмотрят.")

    async def request_video(self, user_id, user_name, own, file_id, file_type):
        with self.connection:
            rand_id = random.randint(999, 9999)
            data = self.cursor.execute("SELECT user_id FROM requests WHERE user_id = ?", (user_id,)).fetchall()
            admins = self.cursor.execute("SELECT admin_id FROM admins").fetchall()

            if not data:
                self.cursor.execute("INSERT INTO requests VALUES(?, ?, ?, ?, ?, ?)", (rand_id, user_id, user_name, own, file_id, file_type,))

                for res in admins:
                    await bot.send_video(*res, file_id, caption=f"<b>Новая заявка на публикацию</b>\n\n"
                                                 f"ИД заявки: {rand_id}\n"
                                                 f"ИД отправителя: {user_id}\n"
                                                 f"Имя отправителя: {user_name}\n"
                                                 f"Имя владельца фото, возможно, контакты: {own}\n"
                                                 f"Тип файла: {file_type}\n")
            else:
                await bot.send_message(user_id, "у тебя уже висит одна заявка, жди пока её рассмотрят.")


    async def accept_post(self, id, vote):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM requests WHERE id = ?", (id,))

            for res in data:
                if res[5] == 'photo':
                    if vote == True:
                        await bot.send_photo(-1001772787084, res[4], caption="🦄 - норми\n"
                                                                             "💊 - просто круто класс топ\n"
                                                                             "🙉 - кринге люти")
                        await bot.send_message(res[1], "Твой пост был одобрен и опубликован")
                        self.cursor.execute("DELETE FROM requests WHERE id = ?", (id,))
                    elif vote == False:
                        await bot.send_photo(-1001772787084, res[4])
                        await bot.send_message(res[1], "Твой пост был одобрен и опубликован")
                        self.cursor.execute("DELETE FROM requests WHERE id = ?", (id,))
                elif res[5] == 'video':
                    if vote == True:
                        await bot.send_video(-1001772787084, res[4], caption="🦄 - норми\n"
                                                                             "💊 - просто круто класс топ\n"
                                                                             "🙉 - кринге люти")
                        await bot.send_message(res[1], "Твой пост был одобрен и опубликован")
                        self.cursor.execute("DELETE FROM requests WHERE id = ?", (id,))
                    elif vote == False:
                        await bot.send_video(-1001772787084, res[4])
                        await bot.send_message(res[1], "Твой пост был одобрен и опубликован")
                        self.cursor.execute("DELETE FROM requests WHERE id = ?", (id,))


    async def denied_post(self, id, reason, banned):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM requests WHERE id = ?", (id,)).fetchall()

            for res in data:
                remove = self.cursor.execute("DELETE FROM requests WHERE id = ?", (id,))

                if banned == True:
                    self.cursor.execute("UPDATE users SET banned = 1 WHERE userid = ?", (res[1],))
                    await bot.send_message(res[1], f"Твой пост был отклонен, а еще теперь ты в бане. Причина бана+отклонения: {reason}")
                    return remove
                elif banned == False:
                    await bot.send_message(res[1], f"Твой пост был отклонен. Причина: {reason}")
                    return remove
                
    async def request_remove(self, userid, user_name, link, reason):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM remove_requests WHERE userid = ?", (userid,)).fetchall()
            admins = self.cursor.execute("SELECT admin_id FROM admins").fetchall()
            rand_id = random.randint(0, 100)

            if not data:
                self.cursor.execute("INSERT INTO remove_requests VALUES(?, ?, ?, ?, ?)", (rand_id, userid, user_name, link, reason,))

                for res in admins:
                    await bot.send_message(*res, f"<b>Новая заявка на удаление поста</b>\n\n"
                                                 f"ИД заявки: {rand_id}\n"
                                                 f"ИД отправителя: {userid}\n"
                                                 f"Имя отправителя: {user_name}\n"
                                                 f"Причина удаления: {reason}\n"
                                                 f"Ссылка на пост: {link}\n")
            else:
                await bot.send_message(userid, "У тебя уже есть одна заявка на удаление. Не засирай БД и жди одобрения")

    async def request_remove_del(self, id, value):
        with self.connection:
            data = self.cursor.execute("SELECT * FROM remove_requests WHERE id = ?", (id,)).fetchall()

            for res in data:
                if value == True:
                    remove = self.cursor.execute("DELETE FROM remove_requests WHERE id = ?", (id,))
                    await bot.send_message(res[1], f"Твой запрос на удаление поста был одобрен")
                    return remove
                else:
                    remove = self.cursor.execute("DELETE FROM remove_requests WHERE id = ?", (id,))
                    await bot.send_message(res[1], f"Твой запрос на удаление поста был отклонен")
                    return remove
