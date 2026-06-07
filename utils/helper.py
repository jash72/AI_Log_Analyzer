import os
from datetime import datetime


def ensure_directory(path):

    if not os.path.exists(path):
        os.makedirs(path)


def generate_report_name():

    now = datetime.now()

    return (
        "comparison_report_"
        + now.strftime("%Y%m%d_%H%M%S")
        + ".xlsx"
    )


def safe_text(text):

    if text is None:
        return ""

    return str(text)