import pandas as pd
import numpy as np


def read_contract(path):
    col_names = [
        "contractid", "planid", "org_type", "plan_type", "partd", "snp", "eghp",
        "org_name", "org_marketing_name", "plan_name", "parent_org", "contract_date"
    ]
    df = pd.read_csv(
        path,
        skiprows=1,
        names=col_names,
        encoding="latin1",
        dtype={
            'contractid': str, 'planid': float, 'org_type': str, 'plan_type': str,
            'partd': str, 'snp': str, 'eghp': str, 'org_name': str,
            'org_marketing_name': str, 'plan_name': str, 'parent_org': str,
            'contract_date': str
        }
    )
    return df


def read_enroll(path):
    col_names = ["contractid", "planid", "ssa", "fips", "state", "county", "enrollment"]
    df = pd.read_csv(
        path,
        skiprows=1,
        names=col_names,
        na_values="*",
        encoding="latin1",
        dtype={
            'contractid': str, 'planid': float, 'ssa': float, 'fips': float,
            'state': str, 'county': str, 'enrollment': float
        }
    )
    return df


def load_month(m, y):
    c_path = f"../ma-data/ma/enrollment/Extracted Data/CPSC_Contract_Info_{y}_{m}.csv"
    e_path = f"../ma-data/ma/enrollment/Extracted Data/CPSC_Enrollment_Info_{y}_{m}.csv"

    contract_info = read_contract(c_path).drop_duplicates(
        subset=['contractid', 'planid'], keep='first'
    )
    enroll_info = read_enroll(e_path)

    merged = contract_info.merge(
        enroll_info, on=['contractid', 'planid'], how='left'
    )
    merged['month'] = int(m)
    merged['year'] = y
    return merged


