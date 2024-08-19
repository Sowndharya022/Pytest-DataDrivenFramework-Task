# Using Data Driven Testing Framework (DDTF), Page Object Model (POM), Explicit Wait, Expected Conditions, Pytest kindly do the following task as mentioned below :-
# 1) Create an Excel file which will comprise of Test ID, Username, Password, Date, Time of Test, Name of Tester, Test Result for login into the portal.
# 2) Go to the URL https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
# 3) Login into the Portal using the Username and Password provided in the Excel file. Try to use 5 Username and Password.
# 4) If the Login is successful your Python code will write in the Excel file whether your Test Passed or Test Failed.
# 5) Do not use sleep() method

import pytest
import pandas as pd
from pages.login_page import LoginPage
from datetime import datetime
import os


def get_login_data():
    login_data = []
    # Read the CSV file with login data
    df = pd.read_csv('data/login_data.csv')
    for index, row in df.iterrows():
        login_data.append((row['username'], row['password'], index + 1))  # Use index + 1 for Test ID
    return login_data


def update_test_result(test_id, result, tester_name):
    file_path = 'data/test_result.csv'

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")

    try:
        # Read the results CSV file
        df = pd.read_csv(file_path)

        # Check if 'TesterName' column exists, create if not
        if 'TesterName' not in df.columns:
            df['TesterName'] = ''

        # Update the test result and additional details
        if test_id in df['Test ID'].values:
            df.loc[df['Test ID'] == test_id, 'Test Result'] = result
            df.loc[df['Test ID'] == test_id, 'Date'] = datetime.now().strftime('%Y-%m-%d')
            df.loc[df['Test ID'] == test_id, 'Time'] = datetime.now().strftime('%H:%M:%S')
            df.loc[df['Test ID'] == test_id, 'TesterName'] = tester_name
        else:
            raise ValueError(f"Test ID {test_id} not found in the file.")

        # Write the updated data back to the CSV file
        df.to_csv(file_path, index=False)
    except PermissionError as e:
        print(f"Permission error: {e}")
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


@pytest.mark.usefixtures("setup")
class TestLogin:

    @pytest.mark.parametrize("username, password, test_id", get_login_data())
    def test_login(self, username, password, test_id):
        login_page = LoginPage(self.driver)
        login_page.login(username, password)

        # Check if the login is successful
        if "dashboard" in self.driver.current_url:  # Adjust according to the actual success indicator
            result = "Passed"
        else:
            result = "Failed"

        # Get the tester's name.
        tester_name = "Sowndharya"

        # Update the test result in the CSV file
        update_test_result(test_id, result, tester_name)

        # Assertion to check the test result
        assert result == "Passed"
