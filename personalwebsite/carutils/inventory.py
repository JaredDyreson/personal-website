import sqlite3
import pathlib
from personalwebsite.carutils.service import Service
from datetime import datetime

class Inventory():
    def __init__(self, connection):
        if not(isinstance(connection, sqlite3.Connection)):
            raise ValueError
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.table_name = "services"
        self.init()

    def __del__(self):
        self.connection.close()

    def init(self):
        try:
            self.cursor.execute(f"""CREATE TABLE {self.table_name} (
                               service_name text,
                               date text,
                               odometer_reading integer,
                               part_sku text,
                               invoices text
                               )""")
        except Exception:
            pass

    def insert_service(self, service: Service):
        if not(isinstance(service, Service)):
            raise ValueError

        self.cursor.execute("INSERT INTO services VALUES(?, ?, ?, ?, ?)", service.sqlformat)
        self.connection.commit()

    def get_services_by_name(self, service: str) -> list:
        """
        Return a list of services that meet a criteria
        """

        if not(isinstance(service, str)):
            raise ValueError
        self.cursor.execute("SELECT * FROM services WHERE service_name=?", (service,))
        return self.cursor.fetchall()

    def get_all_services(self) -> list:
        self.cursor.execute("SELECT * FROM services")
        return self.cursor.fetchall()
        

    def remove_service(self, service: Service):
        if not(isinstance(service, Service)):
            raise ValueError

        self.cursor.execute("""DELETE from services WHERE service_name = ? AND date = ?
                                AND odometer_reading = ? AND part_sku = ? AND invoices = ?
                            """, service.sqlformat)
        self.connection.commit()
