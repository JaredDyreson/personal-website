from datetime import datetime
import pathlib

class Service():
    def __init__(self, name: str, date: datetime, 
                    odometer_reading: float, part_sku: str,
                    invoices: pathlib.Path):

        if not(isinstance(name, str) and
               isinstance(date, datetime) and
               isinstance(odometer_reading, float) and
               isinstance(part_sku, str) and
               isinstance(invoices, pathlib.Path)):
               # invoices.exists()):
               raise ValueError

        self.name = name
        self.date = date
        self.odometer_reading = odometer_reading
        self.part_sku = part_sku
        self.invoices = invoices

    @property
    def sqlformat(self) -> tuple:
        return (self.name, self.date, self.odometer_reading, self.part_sku, str(self.invoices.absolute()))
