from typing import Generator
import sqlite3
from db_client.db_config import DBConfig

class AppointmentDBClient:
    def __init__(self, db_config: DBConfig):
        self.db_config = db_config
        self.conn = sqlite3.connect(db_config.host)
        self.cursor = self.conn.cursor()
        
    def delete_appointment(self, appointment_id: int):
        query = "DELETE FROM appointments WHERE id = ?"
        self.cursor.execute(query, (appointment_id,))
        deleted_count = self.conn.commit()
        return deleted_count

    def check_appointment_exists(self, appointment_id: int):
        query = "SELECT EXISTS(SELECT 1 FROM appointments WHERE id = ?)"
        self.cursor.execute(query, (appointment_id,))
        return self.cursor.fetchone()[0]
        
