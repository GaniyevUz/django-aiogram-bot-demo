import sqlite3
from sqlite3 import IntegrityError

from root.settings import DATABASES


class Database:
    def __init__(self):
        self.path_to_db = DATABASES['default'].get('NAME')

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def get_chat(self, **kwargs):
        sql = "SELECT * FROM groups WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        result = self.execute(sql, parameters=parameters, fetchone=True)
        return result

    def get_all_chats(self, **kwargs):
        sql = "SELECT * FROM groups"
        result = self.execute(sql, fetchall=True)
        return result

    def new_chat(self, chat_id, username=None, title=None):
        sql = 'insert into groups(chat_id, username, title) values (?, ?, ?);'
        try:
            self.execute(sql, parameters=(chat_id, username, title), commit=True)
        except IntegrityError:
            pass

    # @property
    def get_invite_user_limit(self, group_id):
        sql = "select invite_user_limit from settings join groups g on g.id = settings.group_id where chat_id = ?;"
        limit = self.execute(sql, parameters=(group_id,), fetchone=True)
        if not limit:
            return 20
        return 20 if limit[0] <= 0 else limit[0]

    def add_user(self, first_name: str, last_name: str, telegram_id: int, group_id=None):
        sql = """INSERT INTO users(first_name, last_name, telegram_id, date_joined, group_id)
         values(?, ?, ?, CURRENT_TIMESTAMP, ?)"""
        self.execute(sql, parameters=(first_name, last_name, telegram_id, group_id), commit=True)

    @property
    def select_all_users(self):
        sql = 'SELECT telegram_id FROM users'
        return self.execute(sql, fetchall=True)

    def select_all_chat_users(self, chat_id):
        sql = 'SELECT telegram_id FROM users where group_id = ?'
        return self.execute(sql, parameters=(chat_id,), fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    @property
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)[0]

    def count_invitation(self, group_id, user_id):
        try:
            sql = 'select invated_users_count, can_send_message from invited_members where chat = ? and telegram = ?;'
            result = self.execute(sql, parameters=(group_id, user_id), fetchone=True)
            if not result:
                sql = 'insert into invited_members(invated_users_count, chat, telegram, can_send_message) ' \
                      'values (0, ?, ?, FALSE)'
                self.execute(sql, parameters=(group_id, user_id), commit=True)
                return 0, False
        except IntegrityError:
            return 0, False
        return result

    def increase_invitation(self, group_id, user_id):
        sql = 'update invited_members set invated_users_count = ?  where chat = ? and telegram = ?;'
        count = self.count_invitation(group_id, user_id)[0] + 1
        return self.execute(sql, parameters=(count, group_id, user_id), commit=True)

    def can_send_message(self, group_id, user_id):
        sql = 'update invited_members set can_send_message = TRUE where chat = ? and telegram = ?'
        return self.execute(sql, parameters=(group_id, user_id), commit=True)

    def delete_users(self):
        self.execute('delete from users where true;', commit=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
