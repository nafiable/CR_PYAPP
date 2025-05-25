import pandas as pd
from visual import display_dataframe_gui
from utils.wait_utils import Wait

def main():
    """
    Example demonstrating how to use display_dataframe_gui and Wait.
    """
    # Create a sample pandas DataFrame
    data = {'Column A': [10, 20, 30, 40, 50],
            'Column B': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
            'Column C': [True, False, True, False, True]}
    df = pd.DataFrame(data)

    print("Displaying DataFrame in a GUI window...")
    # Display the dataframe in the GUI
    display_dataframe_gui(df)

    print("Pausing execution for 10 seconds...")
    # Pause execution for 10 seconds to view the GUI
    Wait(10)

    print("Execution resumed after 10 seconds.")

if __name__ == "__main__":
    main()