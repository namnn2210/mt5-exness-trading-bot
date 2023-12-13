import json
import os

import pandas

import mt5_lib

settings_filepath = "settings.json"


def get_project_settings(import_filepath):
    """
    Function to import settings from settings.json
    :param import_filepath: path to settings.json
    :return: settings as a dictionary object
    """
    # Test the filepath to make sure it exists
    if os.path.exists(import_filepath):
        # If yes, import the file
        f = open(import_filepath, "r")
        # Read the information
        project_settings = json.load(f)
        # Close the file
        f.close()
        # Return the project settings
        return project_settings
    # Notify user if settings.json doesn't exist
    else:
        raise ImportError("settings.json does not exist at provided location")


# Function to repeat startup proceedures
def start_up(project_settings):
    """
    Function to manage start up proceedures for App. Includes starting/testing exchanges
    initializing symbols and anything else to ensure app start is successful.
    :param project_settings: json object of the project settings
    :return: Boolean. True if app start up is successful. False if not.
    """
    # Start MetaTrader 5
    startup = mt5_lib.start_mt5(project_settings=project_settings)
    # If startup successful, let user know
    if startup:
        print("MetaTrader startup successful")
        # Initialize symbols
        # Extract symbols from project settings
        symbols = project_settings["mt5"]["symbols"]
        # Iterate through the symbols to enable
        for symbol in symbols:
            outcome = mt5_lib.initialize_symbol(symbol)
            # Update the user
            if outcome is True:
                print(f"Symbol {symbol} initalized")
            else:
                raise Exception(f"{symbol} not initialized")
        return True
    # Default return is False
    return False


if __name__ == '__main__':
    print("Let's build an awesome trading bot!!!")
    # Import settings.json
    project_settings = get_project_settings(import_filepath=settings_filepath)
    print(project_settings)
    # Run through startup proceedure
    startup = start_up(project_settings=project_settings)
    print(startup)
    # Make it so that all columns are shown
    symbols = project_settings['mt5']['symbols']
    for symbol in symbols:
        candlesticks = mt5_lib.get_candlesticks(symbol=symbol, timeframe=project_settings['mt5']['timeframe'],
                                                number_of_candles=1000)
        pandas.set_option('display.max_columns',None)
        print(candlesticks)
