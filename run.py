import gspread
from google.oauth2.service_account import Credentials
from collections import Counter
from fractions import Fraction 
import matplotlib.pyplot as plt


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
    print("3. view data visualization")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == '1':
        input_data()
    elif choice == '2':
        view_data_analysis()
    elif choice == '3':
        view_data_visualization()    
    elif choice == '4':
        exit()
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        main_menu()


survey_questions = [
     "1: what is your age?\n",
     "2: Do you think Instagram influencers are having a positive impact on young people's self-esteem? Please type one of the following - strongly disagree, disagree, neutral, agree, strongly agree\n",
     "3: How much does Instagram or other social media affect what you purchase in the beauty industry? Please type one of the following - a lot, a little, a moderate amount, not much at all, a significant amount\n",
     "4: How often do you wear makeup? Please type one of the following - rarely, daily, occasionally, weekly, monthly\n",
     "5: Do you feel investing in skin care products is worth it? Please type one of the following - strongly disagree, disagree, neutral, agree, strongly agree\n",
     "6: How would you rate your self-esteem and body image? Please type one of the following - very low, low, neutral, high, very high\n",
     "7: Do you subscribe to beauty boxes or services that provide you with new products regularly? Please type one of the following - yes, no\n",
     "8: How much do you typically spend on beauty products each month? Please type one of the following - under £25, £25 - £50, £50 - £100, £100 - £200, £200 - £300, over £300\n",
     "9: Do you have a step by step skincare routuine? Please type one of the following - yes, no\n",
     "10: Do you feel more attractive when you are wearing makeup? Please type one of the following - yes, no\n"
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
    print("Choose a question number to analyze (1-10):\n" + "\n".join(survey_questions))
    question_number = int(input())

    # Ensure the chosen question number is valid
    if question_number < 1 or question_number > 10:
        print("Invalid question number. Please choose a number between 1 and 10.")
        return

    
    if question_number == 1:
    # Special case for analyzing the age question
        age_responses = [int(age) for age in worksheet.col_values(1)[1:]]
        # Calculate statistics only if there are age responses
        print(f"Analysis for question number {question_number}:")
        average_age = sum(age_responses) / len(age_responses)
        oldest_age = max(age_responses)
        youngest_age = min(age_responses)
        print(f"Average Age: {average_age:.2f}")
        print(f"Oldest Person: {oldest_age}")
        print(f"Youngest Person: {youngest_age}")
    else:
        # Retrieve the chosen question
        responses = worksheet.col_values(question_number)
        # Ensure that the question text is not counted as a vote
        question_text = responses[0]
        non_empty_responses = [response for response in responses[1:] if response != question_text]
        response_counts = Counter(non_empty_responses)
        
        print(f"Analysis for question number {question_number}:")
        for response, count in response_counts.items():
            print(f"{response}: {count} voters") # Exit early, no need to proceed with the rest of the code
        # Retrieve the chosen question
        responses = worksheet.col_values(question_number)
        # Ensure that the question text is not counted as a vote
        question_text = responses[0]
        non_empty_responses = [response for response in responses[1:] if response != question_text]
        response_counts = Counter(non_empty_responses)
        

        print("View as:")
        print("1. Decimal")
        print("2. Fraction")
        print("3. Percentage")
        view_option = input("Enter your choice (1/2/3): ")

        if view_option == '1':
            # Display as decimal
            for response, count in response_counts.items():
                print(f"{response}: {count / len(responses):.2f}")
        if view_option == '2':
        # Display as a fraction
            total_responses = len(responses)
            for response, count in response_counts.items():
                fraction = Fraction(count, total_responses)  # Use the Fraction class to calculate fractions
                print(f"{response}: {fraction}")
            
        elif view_option == '3':
        # Display as a percentage
            for response, count in response_counts.items():
                percentage = (count / len(responses)) * 100
                print(f"{response}: {percentage:.2f}%")

def view_data_visualization():
    print("Data Visualization Menu")
    
    question_number = int(input("Enter the question number you want to visualize (1-10): "))
    
    if question_number < 1 or question_number > 10:
        print("Invalid question number. Please choose a number between 1 and 10.")
        return

    print("1. Bar Chart")
    print("2. Histogram (for age)")
    print("3. Table")
    visualization_option = input("Enter your choice (1/2/3): ")

    



if __name__ == '__main__':
    main_menu()
                