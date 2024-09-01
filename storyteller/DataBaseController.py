import sqlite3

class DataBaseController():
    def __init__(self) -> None:
        self.connection = sqlite3.connect("story.db")
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Characters (
            id INTEGER PRIMARY KEY,
            tg_user_id TEXT NOT NULL,
            char_name TEXT,
            char_prompt TEXT
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Stories (
            id INTEGER PRIMARY KEY,
            tg_user_id TEXT NOT NULL,
            story_name TEXT,
            story_text TEXT,
            story_images TEXT
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Rooms (
            room_id INTEGER PRIMARY KEY,
            tg_users_ids TEXT NOT NULL,
            all_story TEXT,
            prev_story TEXT
            )''')
        
        self.connection.commit()
    
    def add_char(self, tg_user_id, char_name, prompt):
        self.cursor.execute('''
                            INSERT INTO Characters (tg_user_id, char_name, char_prompt) VALUES (?,?,?)
                            ''',
                            (tg_user_id, char_name, prompt)
                            )
        self.connection.commit()
    
    def delete_char(self, tg_user_id, char_id):
        self.cursor.execute(f'''
                            DELETE FROM Characters WHERE tg_user_id = {tg_user_id} AND id = {char_id}
                            '''
                            )
        self.connection.commit()

    def get_all_chars(self, tg_user_id):
        chars = self.cursor.execute(f'''
                            SELECT * FROM Characters WHERE tg_user_id = {tg_user_id}
                            '''
                            )
        data = []
        for i in chars.fetchall():
            data.append(
                {
                    "name":i[2],
                    "id":str(i[0]),
                    "info":i[3]
                }
            )
        return data
               
    def get_char_prompt(self, tg_user_id, char_id):
        prompt = self.cursor.execute(f'''
                            SELECT char_name, char_prompt FROM Characters WHERE tg_user_id = {tg_user_id} AND id = {char_id}
                            '''
                            )
        return ", ".join(prompt.fetchone())
    
    def add_story(self, tg_user_id, story_name, story_text, story_images):
        self.cursor.execute('''
                            INSERT INTO Stories (tg_user_id, story_name, story_text, story_images) VALUES (?,?,?,?)
                            ''',
                            (tg_user_id, story_name, story_text, story_images)
                            )
        self.connection.commit()
    
    def get_all_stories(self, tg_user_id):
        chars = self.cursor.execute(f'''
                            SELECT * FROM Stories WHERE tg_user_id = {tg_user_id}
                            '''
                            )
        data = []
        for i in chars.fetchall():
            data.append(
                {
                    "id":str(i[0]),
                    "story_name":i[2],
                    "story_text":i[3],
                    "story_images": [img for img in i[4].split(", ")]
                }
            )
        return data
    
    def delete_story(self, tg_user_id, story_id):
        self.cursor.execute(f'''
                            DELETE FROM Stories WHERE tg_user_id = {tg_user_id} AND id = {story_id}
                            '''
                            )
        self.connection.commit()
    
        
if __name__ == "__main__":
    db = DataBaseController()
    print(db.get_char_prompt(992368341, 3))