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
        Column('Mark', []),
        Column('Internal_lab_ID', [IsDistinctValidation()]),
        Column('Selection_criterion', [CustomElementValidation(len0, 'Empty or too short.')], allow_empty=False),
        Column('Collection_date', [CustomElementValidation(len0, 'Empty or too short.')], allow_empty=False),
        Column('Patient_age', [CustomElementValidation(age, 'Invalid age.')], allow_empty=False),
        Column('Patient_sex', [CustomElementValidation(lambda s: len(str(s)) > 1, 'Empty or too short.')], allow_empty=False),
        Column('Patient_status', [CustomElementValidation(lambda s: len(str(s)) > 1, 'Empty or too short.')], allow_empty=False),
        Column('Type', []),
        Column('Sminet_LID', [IsDistinctValidation()], allow_empty=True),
        Column('Pseudo_ID', []),
        Column('Region', [CustomElementValidation(lambda s: len(str(s)) > 1, 'Empty or too short.')]),
        Column('Region_code', []),
        Column('Lab', []),
        Column('Lab_code', []),
        Column('Host', []),
        Column('Passage_details', []),
        Column('Sequencing_technology', []),
        Column('Library_method', []),
        Column('Lane', []),
        Column('Fastq1', []),
        Column('Fastq2', []),
        Column('Fast5', []),
        Column('Seq_path', []),
        Column('Comment', [])
    ])

    errors = schema.validate(df)

    if errors:
        txt_errors = []
        for error in errors:
            txt_errors.append(str(error))

        return txt_errors

    return []
