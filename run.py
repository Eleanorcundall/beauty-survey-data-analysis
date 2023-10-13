import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('beauty-survey-data')

def main_menu():
    print("Welcome to the Beauty Survey Data Analysis")
    print("1. Input Your Own Data")
    print("2. View Data Analysis")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        input_data()
    elif choice == '2':
        view_data_analysis()
    elif choice == '3':
        exit()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        main_menu()


survey_questions = [
     "Question 1: what is your age?",
     "Question 2: Do you think Instagram influencers are having a positive impact on young people's self-esteem? Please type one of the following - Strongly disagree, Disagree, Neutral, Agree, Strongly agree",
     "Question 3: How much does Instagram or other social media affect what you purchase in the beauty industry? Please type one of the following - A lot, A little, A moderate amount, Not much at all, A significant amount",
     "Question 4: How often do you wear makeup? Please type one of the following - Rarely, Daily, Occasionally, Weekly, Monthly",
     "Question 5: Do you feel investing in skin care products is worth it? Please type one of the following - Strongly disagree, Disagree, Neutral, Agree, Strongly agree",
     "Question 6: How would you rate your self-esteem and body image? Please type one of the following - Very low, Low, Neutral, High, Very High",
     "Question 7: Do you subscribe to beauty boxes or services that provide you with new products regularly? Please type one of the following - Yes, No",
     "Question 8: How much do you typically spend on beauty products each month? Please type one of the following - under £25, £25 - £50, £50 - £100, £100 - £200, £200 - £300, Over £300",
     "Question 9: Do you have a step by step skincare routuine? Please type one of the following - Yes, No",
     "Question 10: Do you feel more attaractive when you are wearing makeup? Please type one of the following - Yes, No"
]

worksheet = SHEET.get_worksheet(1)

def input_data():
    responses = []

    for question in survey_questions:
        response = input(f"{question}: ")  # Get the response from the user
        responses.append(response)

    # Find the last row with data
    last_row = len(worksheet.col_values(1)) + 1

    for col, response in enumerate(responses, start=1):
        worksheet.update_cell(last_row, col, response)


def view_data_analysis():
    # Your code for data analysis goes here
    pass

if __name__ == '__main__':
    main_menu()
                