import pandas as pd

def read_excel(uploaded_file):
    """
    Reads the first column from Excel.
    Assumes one log entry per row.
    """
    try:
        df = pd.read_excel(
            uploaded_file,
            engine="openpyxl"
        )
        if df.empty:
            return []
        first_column = df.columns[0]
        logs = (
            df[first_column]
            .dropna()
            .astype(str)
            .tolist()
        )
        return logs
    except Exception as e:
        raise Exception(f"Excel Read Error : {str(e)}")