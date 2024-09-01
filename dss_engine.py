
import timeit
from datetime import datetime
from idlelib import query
import re
import pandas as pd
from database import PatientData

# CDSS_Project/
# │
# ├── dss_engine.py       # Script to load and manipulate data
# ├── knowledge_base.py    # Script to manage the knowledge base
# ├── database.py          # Script to manage data storage and queries
# └── user_interface.py         # Script to create the user interface


class DSSEngine:
    def __init__(self, patient_data):
        self.db = patient_data

    def retrieval_question(self, query):
        DB = self.db
        (patient_first_name, patient_last_name, loinc_num,
         valid_date, valid_time, physician_date, physician_time) = query
        print('query:   ', query)
        without_valid_time = False

        # Check if date and time are provided
        if valid_date is None:
            return "No record found, insert valid start time."
        
        if physician_date is None or physician_time is None:
            return "No record found, insert valid physician view time."

        # Determine time by date or both, datw and time. Depend on user choice.
        if valid_time is None:
            without_valid_time = True
            valid_date_record_time = pd.Timestamp(f'{valid_date}').date()
        else:
            valid_record_time = pd.Timestamp(f'{valid_date} {valid_time}')

        # Determine date and time according to physician view.
        physician_record_time = pd.Timestamp(f'{physician_date} {physician_time}')

        # filter data to retrieve relevant records
        patient_data = DB.get_patient_data(patient_first_name, patient_last_name)
        patient_data_columns = ['loinc_num', 'value','unit','valid_start_time','transaction_time']
        patient_data_df = pd.DataFrame(patient_data, columns=patient_data_columns)
        patient_data_df_loinc = patient_data_df[(patient_data_df['loinc_num'] == loinc_num)]
        patient_data_df_loinc_phys = patient_data_df_loinc[(patient_data_df_loinc['transaction_time'] <= physician_record_time)]
        
        # retrieve records where match the user inserted date and time
        if without_valid_time:
            data_patient = patient_data_df_loinc_phys.copy()
            # Create a column with date only, user insert date but not excact time
            data_patient['valid_date_start_time'] = patient_data['valid_start_time'].dt.date
            required_records = data_patient[data_patient['valid_date_start_time'] == valid_date_record_time]
            required_records = required_records.loc[required_records['valid_start_time'].idxmax()]
        else:
            # If user insert both, date and time
            required_records = patient_data_df_loinc_phys[(patient_data_df_loinc_phys['valid_start_time'] == valid_record_time)]

        return required_records

    def retrieval_history_question(self, query):
        DB = self.db
        (patient_first_name, patient_last_name, loinc_num,
         valid_start_date, valid_start_time, valid_end_date, valid_end_time) = query
        print(query)
        # Check if date and time are provided
        if valid_start_date is None:
            return "No record found, insert valid start time."

        valid_start_record_time = pd.Timestamp(f'{valid_start_date} {valid_start_time}')
        valid_end_record_time = pd.Timestamp(f'{valid_end_date} {valid_end_time}')
        print(valid_start_record_time)
        print(valid_end_record_time)
        # Filter data to retrieve relevant records
        patient_data = DB.get_patient_data(patient_first_name, patient_last_name)
        patient_data_columns = ['loinc_num', 'value','unit','valid_start_time','transaction_time']
        patient_data_df = pd.DataFrame(patient_data, columns=patient_data_columns)
        patient_data_loinc = patient_data_df[(patient_data_df['loinc_num'] == loinc_num)]
        patient_data_in_range = patient_data_loinc[(patient_data_loinc['valid_start_time'] >= valid_start_record_time)]
        patient_data_in_range = patient_data_in_range[(patient_data_in_range['valid_start_time'] <= valid_end_record_time)]

        return patient_data_in_range

    def update_record(self, new_value, query):
        DB = self.db
        (patient_first_name, patient_last_name, loinc_num,
         valid_date, valid_time, transaction_date, transaction_time) = query
        print(query)
        # Check if date and time are provided
        if valid_date is None or valid_time is None:
            return "No record found, insert valid start time."
        
        if transaction_date is None or transaction_time is None:
            return "No record found, insert valid transaction time."

        valid_record_time = pd.Timestamp(f'{valid_date} {valid_time}')
        transaction_record_time = pd.Timestamp(f'{transaction_date} {transaction_time}')

        # filter data to retrieve relevant records
        patient_data = DB.get_patient_data(patient_first_name, patient_last_name)
        patient_data_columns = ['loinc_num', 'value','unit','valid_start_time','transaction_time']
        patient_data_df = pd.DataFrame(patient_data, columns=patient_data_columns)
        patient_data_loinc = patient_data_df[(patient_data_df['loinc_num'] == loinc_num)]
        patient_data_valid_time = patient_data_loinc[(patient_data_loinc['valid_start_time'] == valid_record_time)]
        required_record = patient_data_valid_time[(patient_data_valid_time['transaction_time'] == transaction_record_time)]

        if not required_record.empty:
            # Get the index of the matching record
            index_to_update = required_record.index[0]

            # Update the 'Value' column for this record
            required_record.loc[index_to_update, 'value'] = new_value
            print(f"Updated record at index {index_to_update}:")
            print(required_record.loc[index_to_update])
        else:
            print("No matching record found.")
        
        return required_record

    def delete_record(self, query):
        DB = self.db
        (patient_first_name, patient_last_name, loinc_num,
         valid_date, valid_time, transaction_date, transaction_time) = query

        # Check if date and time are provided
        if valid_date is None or transaction_date is None:
            return "No record found, insert valid start time or transaction time."

        valid_record_time = pd.Timestamp(f'{valid_date} {valid_time}')
        transaction_record_time = pd.Timestamp(f'{transaction_date} {transaction_time}')

        # filter data to retrieve relevant records
        patient_data = DB.get_patient_data(patient_first_name, patient_last_name)
        patient_data_columns = ['loinc_num', 'value','unit','valid_start_time','transaction_time']
        patient_data_df = pd.DataFrame(patient_data, columns=patient_data_columns)
        patient_data_to_save = patient_data_df.copy()
        # Check which record to drop, required record
        patient_data_df_loinc = patient_data_df[(patient_data_df['loinc_num'] == loinc_num)]
        patient_data_valid_time = patient_data_df_loinc[(patient_data_df_loinc['valid_start_time'] == valid_record_time)]
        required_record = patient_data_valid_time[(patient_data_valid_time['transaction_time'] == transaction_record_time)]

        if not required_record.empty:
            # Get the index of the matching record
            rows_to_drop = required_record.index[0]
            print(patient_data_to_save)
            patient_data_to_save = patient_data_to_save.drop(rows_to_drop)
            print(f'Record {rows_to_drop} as been removed:')
        else:
            print('There is no records in inserted time')

        return ("The update was successful.", required_record.iloc[0])


if __name__ == "__main__":

    patient_data = PatientData(host="localhost", user="root", password="q6rh3b", database="patient_data")
    engine = DSSEngine(patient_data)

    # query = ['Eyal', 'Rothman', '11218-5', '17/05/2018', '17:00:00', '25/05/2018',  '10:00:00']
    # result = engine.retrieval_question(query)
    # print(result)
    
    # query = ['Eyal', 'Rothman', '11218-5', '17/05/2018', '6:00:00', '21/05/2018', '15:00:00']
    # result = engine.retrieval_history_question(query)
    # print(result)
    
    # query = ['Eyal', 'Rothman', '11218-5', '17/05/2018', '13:11:00', '27/05/2018', '10:00:00']
    # engine.update_record('4444', query)

    query = ['Eyal', 'Rothman', '11218-5', '17/05/2018', '13:11:00', '27/05/2018', '10:00:00']
    result = engine.delete_record(query)
    print(result[0])
    print(result[1])


