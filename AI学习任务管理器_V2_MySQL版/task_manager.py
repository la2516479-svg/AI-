from database import Database


class TaskManager:
    def __init__(self):
        self.db = Database()

    def add_task(self, title, subject, minutes, priority):
        sql = """
        INSERT INTO study_tasks (title, subject, minutes, priority)
        VALUES (%s, %s, %s, %s)
        """
        self.db.execute(sql, (title, subject, minutes, priority))

    def get_all_tasks(self):
        sql = """
        SELECT id, title, subject, minutes, priority, completed, created_at
        FROM study_tasks
        ORDER BY completed ASC, id DESC
        """
        return self.db.fetch_all(sql)

    def search_tasks(self, keyword):
        sql = """
        SELECT id, title, subject, minutes, priority, completed, created_at
        FROM study_tasks
        WHERE title LIKE %s
           OR subject LIKE %s
        ORDER BY id DESC
        """
        pattern = f"%{keyword}%"
        return self.db.fetch_all(sql, (pattern, pattern))

    def complete_task(self, task_id):
        sql = """
        UPDATE study_tasks
        SET completed = TRUE
        WHERE id = %s
        """
        self.db.execute(sql, (task_id,))
        return self.db.cursor.rowcount > 0

    def delete_task(self, task_id):
        sql = """
        DELETE FROM study_tasks
        WHERE id = %s
        """
        self.db.execute(sql, (task_id,))
        return self.db.cursor.rowcount > 0

    def close(self):
        self.db.close()
