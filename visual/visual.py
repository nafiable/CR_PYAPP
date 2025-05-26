import tkinter as tk
import pandas as pd
from pandastable import Table, TableModel
import logging

logger = logging.getLogger(__name__)

def display_dataframe_gui(df):
    """
    Displays a pandas DataFrame in a simple Tkinter window using the pandastable library.

    Args:
        df: The pandas DataFrame to display.
    """
    root = tk.Tk()
    logger.info("Creating Tkinter window.")
    root.title("DataFrame Viewer")

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    logger.info("Displaying DataFrame in a table.")
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

    root.mainloop()
    logger.info("Tkinter window closed.")
if __name__ == '__main__':
    # Example usage:
    data = {'col1': [1, 2, 3, 4],
            'col2': ['A', 'B', 'C', 'D'],
            'col3': [10.1, 11.2, 12.3, 13.4]}
    df_example = pd.DataFrame(data)
    display_dataframe_gui(df_example)