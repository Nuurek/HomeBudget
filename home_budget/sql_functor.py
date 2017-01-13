from django.db import connection
from collections import namedtuple


class SQLFunctor:

    def __init__(self):
        self.cursor = connection.cursor()

    def get_bill_total(self, bill_pk):
        query = "SELECT CALCULATE_BILL({}) FROM dual" % bill_pk
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_bills_details(self):
        query = "SELECT sklepy.sieci_sklepow_nazwa AS shop_name, " \
                "paragony.sklepy_adres AS shop_address, " \
                "paragony.czas_zakupu AS purchase_date, " \
                "CALCULATE_BILL(paragony.id) AS total " \
                "FROM paragony JOIN sklepy " \
                "ON paragony.sklepy_adres = sklepy.adres"
        self.cursor.execute(query)
        return self.namedtuple_fetchall()
        # return self.cursor.fetchall()

    def namedtuple_fetchall(self):
        desc = self.cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in self.cursor.fetchall()]
