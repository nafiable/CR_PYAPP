import time

def Wait(seconds):
    """
    Pauses the execution of the program for a specified number of seconds.

    Args:
        seconds (int): The number of seconds to wait.
    """
    time.sleep(seconds)

if __name__ == '__main__':
    print("Waiting for 3 seconds...")
    Wait(3)
    print("Done waiting.")