import pandas as pd

def load_tickets(tickets: pd.DataFrame) -> pd.DataFrame:
    """
    Load tickets data and prepare combined text field.
    Summary is repeated 3 times to give more weight than Description.
    """
    tickets['text'] = tickets['Summary'] * 3 + " " + tickets['Description']
    return tickets
