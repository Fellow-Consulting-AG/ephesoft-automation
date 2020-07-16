import pandas as pd

from ephesoftAutomation.helper import util


def add_count_to_dict(dictionary, key):
    if key not in dictionary:
        dictionary[key] = 0
    dict_val = dictionary[key]
    dictionary[key] = dict_val + 1
    dictionary[key] = dict_val + 1


class FieldResult(object):

    def __init__(self, field_name, actual_value, extracted_value):
        self.field_name = field_name
        self.actual_value = actual_value
        self.extracted_value = extracted_value


class BatchComparisonResult(object):

    def __init__(self):

        self.total_count = {}
        self.correct_values_with_high_ocr = {}
        self.correct_values = {}
        self.wrong_values = {}
        self.missing_values = {}

        self.dicts = [self.total_count, self.correct_values_with_high_ocr, self.wrong_values, self.missing_values,
                      self.correct_values]

        self.field_results: [str, [FieldResult]] = {}

    def add_key_to_dicts(self, key):
        for dic in self.dicts:
            if key not in dic:
                dic[key] = 0

    def increment_correct_results(self, field_name):
        self.add_key_to_dicts(field_name)
        add_count_to_dict(self.total_count, field_name)
        add_count_to_dict(self.correct_values, field_name)

    def increment_correct_with_high_ocr_results(self, field_name):
        self.add_key_to_dicts(field_name)
        add_count_to_dict(self.total_count, field_name)
        add_count_to_dict(self.correct_values_with_high_ocr, field_name)
        add_count_to_dict(self.correct_values, field_name)

    def increment_wrong_results(self, field_name):
        self.add_key_to_dicts(field_name)
        add_count_to_dict(self.total_count, field_name)
        add_count_to_dict(self.wrong_values, field_name)

    def increment_missing_results(self, field_name):
        self.add_key_to_dicts(field_name)
        add_count_to_dict(self.total_count, field_name)
        add_count_to_dict(self.missing_values, field_name)

    def add_field_error_info(self, doc_id, field_info: FieldResult):
        if doc_id not in self.field_results:
            fields = [field_info]
            self.field_results[doc_id] = fields
        else:
            self.field_results[doc_id].append(field_info)

    def get_data(self):
        raw_data = {'Field name': list(self.total_count.keys()),
                    'Total': list(self.total_count.values()),
                    'Correct (High OCR)': list(self.correct_values_with_high_ocr.values()),
                    'Correct': list(self.correct_values.values()),
                    'Missing': list(self.missing_values.values()),
                    'Wrong': list(self.wrong_values.values())}

        return raw_data

    def get_data_frame(self):
        raw_data = self.get_data()

        df = pd.DataFrame(raw_data)
        df['Percent Correct'] = (df['Correct'] / df['Total']) * 100
        df['Percent Missing'] = df['Missing'] / df['Total'] * 100
        df['Percent Error'] = df['Wrong'] / df['Total'] * 100

        pd.set_option('display.max_columns', None)
        return df

    def print_results(self):
        df = self.get_data_frame()
        print(df)

    def print_extraction_errors(self):
        for doc_id in self.field_results:
            print(doc_id)
            for field in self.field_results[doc_id]:
                if util.check_if_empty_or_none(field.extracted_value):
                    print("Missing: Field name: ", field.field_name, " - Expected value: ", field.actual_value)
                else:
                    print("False: ", field.field_name, " - Extracted value: ", field.extracted_value,
                          " - Expected Value: ",
                          field.actual_value)
            print('-----------')

    def export_to_excel(self, filename):
        #        filename = 'results_' + str(datetime.datetime.now()) + '.xlsx'
        #        if document_name is not None:
        #            filename = document_name + '-' + datetime.datetime.now().strftime("%d-%m-%Y") + '.xlsx'

        data = self.get_data_frame()

        writer = pd.ExcelWriter(filename, engine='xlsxwriter')

        data.to_excel(writer, startrow=1, sheet_name='Results', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Results']

        for i, col in enumerate(data.columns):
            # find length of column i
            column_len = data[col].astype(str).str.len().max()
            # Setting the length if the column header is larger
            # than the max column value length
            column_len = max(column_len, len(col)) + 2
            # set the column length
            worksheet.set_column(i, i, column_len)

        writer.save()
