import tkinter as tk
import pandas as pd
from pandastable import Table, TableModel

def display_dataframe_gui(df):
    """
    Displays a pandas DataFrame in a simple Tkinter window using the pandastable library.

    Args:
        df: The pandas DataFrame to display.
    """
    root = tk.Tk()
    root.title("DataFrame Viewer")

    frame = tk.Frame(root)
    frame.pack(fill='both', expand=True)

    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

    root.mainloop()

if __name__ == '__main__':
    # Example usage:
    data = {'col1': [1, 2, 3, 4],
            'col2': ['A', 'B', 'C', 'D'],
            'col3': [10.1, 11.2, 12.3, 13.4]}
    df_example = pd.DataFrame(data)
    display_dataframe_gui(df_example)