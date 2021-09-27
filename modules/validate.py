import pandas as pd
from io import StringIO
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation, TrailingWhitespaceValidation, \
    CanConvertValidation, \
    MatchesPatternValidation, InRangeValidation, InListValidation, CustomSeriesValidation, IsDistinctValidation, \
    CustomElementValidation


def len0(x):
    if x:
        return len(str(x)) > 0
    return False


def age(x):
    if x:
        return 0 <= int(x) <= 115
    return False


def validate(df):
    schema = Schema([
        Column('mark', []),
        Column('internal_lab_id', [IsDistinctValidation()]),
        Column('selection_criterion', [CustomElementValidation(len0, 'Empty or too short.')], allow_empty=False),
        Column('collection_date', [CustomElementValidation(len0, 'Empty or too short.')], allow_empty=False),
        Column('patient_age', [CustomElementValidation(age, 'Invalid age.')], allow_empty=False),
        Column('patient_sex', [CustomElementValidation(lambda s: len(str(s)) > 1, 'Empty or too short.')], allow_empty=False),
        Column('patient_status', [CustomElementValidation(lambda s: len(str(s)) > 1, 'Empty or too short.')], allow_empty=False),
        Column('type', []),
        Column('sminet_lid', [IsDistinctValidation()], allow_empty=True),
        Column('pseudo_id', []),
        Column('region', [CustomElementValidation(lambda s: len(str(s)) > 1, 'Empty or too short.')]),
        Column('region_code', []),
        Column('lab', []),
        Column('lab_code', []),
        Column('host', []),
        Column('passage_details', []),
        Column('seq_technology', []),
        Column('library_method', []),
        Column('lane', []),
        Column('fastq', []),
        Column('fast5', []),
        Column('seq_path', []),
        Column('comment', [])
    ])

    errors = schema.validate(df)

    if errors:
        txt_errors = []
        for error in errors:
            txt_errors.append(str(error))

        return txt_errors

    return []
