import xml.etree.ElementTree as ET
import csv
import datetime
from decimal import *

#from ephesoftAutomation.helper import results

from ephesoftAutomation.helper import results, constants as const, preferences as pref, util


# Compares extracted values with original values
def get_comparison_results(ephesoft_results, original_csv_values):
    result = results.BatchComparisonResult()
    actual_values_doc_dict = get_actual_values_dict(original_csv_values)
    extracted_values_doc_dict = get_ephesoft_extracted_values_dict(ephesoft_results)

    for docId in actual_values_doc_dict:
        original_values_dict = actual_values_doc_dict[docId]
        
        if docId in extracted_values_doc_dict:

            extracted_val_dict = extracted_values_doc_dict[docId]

            for field_name in extracted_val_dict:
                extracted_field = extracted_val_dict[field_name]
                extracted_value = extracted_field["Value"]
                ocr_threshold = extracted_field["OcrConfidenceThreshold"]
                ocr_confidence = extracted_field["OcrConfidence"]

                if field_name in original_values_dict:
                    original_value = original_values_dict[field_name]

                    if is_matched_complex(field_name, extracted_value, original_value):
                        if ocr_confidence > ocr_threshold:
                            result.increment_correct_with_high_ocr_results(field_name)
                        else:
                            result.increment_correct_results(field_name)
                    else:
                        if util.check_if_empty_or_none(extracted_value):
                            result.increment_missing_results(field_name)
                        else:
                            result.increment_wrong_results(field_name)

                        extraction_info = results.FieldResult(field_name, original_value, extracted_value)
                        result.add_field_error_info(docId, extraction_info)

        else:
            print(docId+ " is missing from extracted documents.")

    return result


def get_actual_values_dict(file_path):
    original_values = {}
    print(file_path)
    with open(file_path, 'r') as file:
        # with open(original_values_file_path, 'r',encoding = "ISO-8859-1") as file:
        csv_file = csv.DictReader(file, delimiter=pref.CSV_DELIMITER)
        for row in csv_file:
            original_values[row[pref.KEY_FIELD]] = dict(row)
    return original_values


def get_ephesoft_extracted_values_dict(file_path):
    extracted_values = {}
    results_file_path = file_path
    if results_file_path.endswith('.zip'):
        results_file_path = util.extract_zip(results_file_path)

    root = ET.parse(results_file_path).getroot()
    # iterating over all documents to comapare results
    for docs in root.findall('Documents/Document'):

        # getting value for key identifier
        key_field_value = ''
        if pref.KEY_FIELD == const.Fields.KEY_IDENTIFIER:
            key_field_value = docs.find("Identifier").text
        else:
            for field in docs.findall('DocumentLevelFields/DocumentLevelField'):
                if field.find("Name").text == pref.KEY_FIELD:
                    key_field_value = field.find("Value").text
                    break

        doc_dict = {}
        for field2 in docs.findall('DocumentLevelFields/DocumentLevelField'):
            field_name = field2.find("Name").text
            row = {"Name": field_name,
                   "Value": field2.find("Value").text,
                   "OcrConfidenceThreshold": field2.find("OcrConfidenceThreshold").text,
                   "OcrConfidence": field2.find("OcrConfidence").text}
            doc_dict[field_name] = row

        extracted_values[key_field_value] = doc_dict
    return extracted_values


def is_matched(val1, val2):
    if val1 == val2:
        return 1
    elif (util.check_if_empty_or_none(val1)) and (util.check_if_empty_or_none(val2)):
        return 1
    return 0


def is_matched_complex(field_name, extracted_value, original_value):
    if field_name in pref.FIELDS_TO_ADV_CLEAN_BEFORE_COMPARISON:
        original_value = advance_clean_value(field_name, original_value)
        extracted_value = advance_clean_value(field_name, extracted_value)
    elif field_name in pref.FIELDS_TO_CLEAN_BEFORE_COMPARISON:
        original_value = util.clean_value(original_value)
        extracted_value = util.clean_value(extracted_value)

    if is_matched(extracted_value, original_value):
        return 1
    elif not ((util.check_if_empty_or_none(extracted_value)) == (util.check_if_empty_or_none(original_value))):
        return 0

    if field_name in pref.DATE_FIELDS:
        original_value = original_value.replace(" ", "")
        # print(original_value)

        org_date_val = original_value
        for dt_format in pref.ORIGINAL_VAL_DATE_FORMATS:
            try:
                org_date_val = datetime.datetime.strptime(original_value, dt_format).strftime(
                    pref.EXTRACTED_VAL_DATE_FORMAT)
                break
            except:
                print("Wrong date format", dt_format)
        # print(org_date_val)

        return extracted_value == org_date_val

    if field_name == const.Fields.IBAN_EXTRACTED:
        extracted_value = extracted_value.replace(" ", "")
        original_value = original_value.replace(" ", "")
        iban1 = extracted_value.split(",")
        iban2 = original_value.split(",")
        result = util.intersection(iban1, iban2)
        return len(result) > 0
    elif field_name == const.Fields.TAX_RATE or field_name == const.Fields.NET_AMOUNT or field_name == const.Fields.TOTAL_AMOUNT or field_name == const.Fields.TAX_AMOUNT:
        if field_name == const.Fields.TAX_RATE:
            extracted_value = extracted_value.replace("%", "").replace(" ", "")
            original_value = original_value.replace("%", "").replace(" ", "")

        if field_name in pref.ORIGINAL_CURRENCY_FIELDS_NON_US_FORMAT:
            original_value = original_value.replace(".", "").replace(",", ".")
        else:
            original_value = original_value.replace(",", "")

        if field_name in pref.EXTRACTED_CURRENCY_FIELDS_NON_US_FORMAT:
            extracted_value = extracted_value.replace(".", "").replace(",", ".")
        else:
            extracted_value = extracted_value.replace(",", "")

        try:
            # print(extracted_value)
            # print(original_value)
            amount1 = Decimal(extracted_value)
            amount2 = Decimal(original_value)
            # print(amount1)
            # print(amount2)
            return amount1 == amount2
        except ValueError:
            return 0


def advance_clean_value(field_name, val):
    if val is None:
        return val

    if field_name == const.Fields.PAYMENT_TERMS:
        for word in const.PAYMENT_TERMS_STOP_WORDS:
            val = val.replace(word, "")

    if field_name not in pref.MULTI_OPTION_FIELDS:
        val = val.replace(",", "")

    val = val.replace(".", "").replace("-", "").replace(" ", "")

    return val
