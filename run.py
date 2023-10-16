import gspread
from google.oauth2.service_account import Credentials
from collections import Counter

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
     "1: what is your age?",
     "2: Do you think Instagram influencers are having a positive impact on young people's self-esteem? Please type one of the following - strongly disagree, disagree, neutral, agree, strongly agree",
     "3: How much does Instagram or other social media affect what you purchase in the beauty industry? Please type one of the following - a lot, a little, a moderate amount, not much at all, a significant amount",
     "4: How often do you wear makeup? Please type one of the following - rarely, daily, occasionally, weekly, monthly",
     "5: Do you feel investing in skin care products is worth it? Please type one of the following - strongly disagree, disagree, neutral, agree, strongly agree",
     "6: How would you rate your self-esteem and body image? Please type one of the following - very low, low, neutral, high, very high",
     "7: Do you subscribe to beauty boxes or services that provide you with new products regularly? Please type one of the following - yes, no",
     "8: How much do you typically spend on beauty products each month? Please type one of the following - under £25, £25 - £50, £50 - £100, £100 - £200, £200 - £300, over £300",
     "9: Do you have a step by step skincare routuine? Please type one of the following - yes, no",
     "10: Do you feel more attaractive when you are wearing makeup? Please type one of the following - yes, no"
]

worksheet = SHEET.get_worksheet(0)

def input_data():
    valid_responses = [
        None,  # The first question (age) can be any integer
        ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"],  # Question 2
        ["a lot", "a little", "a moderate amount", "not much at all", "a significant amount"],  # Question 3
        ["rarely", "daily", "occasionally", "weekly", "monthly"],  # Question 4
        ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"],  # Question 5
        ["very low", "low", "neutral", "high", "very high"],  # Question 6
        ["yes", "no"],  # Question 7
        ["under £25", "£25 - £50", "£50 - £100", "£100 - £200", "£200 - £300", "over £300"],  # Question 8
        ["yes", "no"],  # Question 9
        ["yes", "no"],  # Question 10
    ]

    responses = []
   
    for i, question in enumerate(survey_questions):
        while True:
            response = input(f"{question}: ").lower()

            if i == 0:  # For the age question
                if response.isdigit():
                    responses.append(response)
                    break
                else:
                    print("Invalid response. Please enter a valid age (an integer).")
            else:
                valid_options = valid_responses[i]
                if response in valid_options:
                    responses.append(response)
                    break
                else:
                    print(f"Invalid response. Please choose one of the following options: {', '.join(valid_options)}")

    # Find the last row with data
    last_row = len(worksheet.col_values(1)) + 1

    for col, response in enumerate(responses, start=1):
        worksheet.update_cell(last_row, col, response)


def view_data_analysis():
    print("Data Analysis Menu")
    print("Choose a question number to analyze (1-10):")
    question_number = int(input())

    # Ensure the chosen question number is valid
    if question_number < 1 or question_number > 10:
        print("Invalid question number. Please choose a number between 1 and 10.")
        return

    # Retrieve the chosen question
    chosen_question = survey_questions[question_number - 1]

    # Retrieve the responses for the chosen question from the spreadsheet
    responses = worksheet.col_values(question_number)
    print(responses)


if __name__ == '__main__':
    main_menu()
                