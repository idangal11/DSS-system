import pandas as pd
import random
import datetime
import mysql.connector

class PatientData:
    def __init__(self, host, user, password, database):
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db_connection.cursor()

    # Get patient by first name and last name
    def get_patient_data(self, first_name, last_name):
        self.cursor.execute(
            "SELECT loinc_num, value, unit, valid_start_time, transaction_time\
            FROM patients p\
            JOIN test_results t ON p.id = t.patient_id\
            WHERE first_name = %s AND last_name = %s",
            (first_name, last_name,)
        )
        return self.cursor.fetchall()
        


    # Add a patient to the database
    def add_patient(self, id, first_name, last_name):
        self.cursor.execute(
            "INSERT INTO patients (id, first_name, last_name) VALUES (%s, %s, %s)",
            (id, first_name, last_name)
        )
        self.db_connection.commit()
        return self.cursor.lastrowid

    # Add test results for a patient
    def add_test_result(self, id, patient_id, loinc_num, value, unit, valid_start_time, transaction_time):
        self.cursor.execute(
            "INSERT INTO test_results (id, patient_id, loinc_num, value, unit, valid_start_time, transaction_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id, patient_id, loinc_num, value, unit, valid_start_time, transaction_time)
        )
        self.db_connection.commit()

    # Get patient test results
    def get_test_results(self, patient_id):
        self.cursor.execute(
            "SELECT loinc_num, value, unit, valid_start_time, transaction_time FROM test_results WHERE patient_id = %s",
            (patient_id,)
        )
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.db_connection.close()

if __name__ == "__main__":
    pd = PatientData(host="localhost", user="root", password="q6rh3b", database="patient_data")

    data = pd.get_patient_data('Eyal', 'Rothman')
    print(type(data))
    # for d in data:
    #     print(d)

    # Add patients
    # idan_id = pd.add_patient(3, "Idan", "Gal")

    # Add test results
    # pd.add_test_result(51, 1, '11218-5', 4500, 'cells/ml', '2018-05-17 13:11:00', '2018-05-27 10:00:00')
    # pd.add_test_result(23, 2, '11218-5', 5500, 'cells/ml', '2018-05-18 15:00:00', '2018-05-21 10:00:00')

    # # Retrieve and print test results for Eyal
    # test_results = kb.get_test_results(eyal_id)
    # for result in test_results:
    #     print(result)

