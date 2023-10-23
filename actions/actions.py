# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import List, Dict, Text, Any
from rasa_sdk import FormValidationAction, Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class WelcomeUser(Action):
    """Sends a welcome message to the user"""

    def name(self) -> Text:
        return "welcome_user"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        welcome_message = f"Welcome {username}!"
        dispatcher.utter_message(welcome_message)

        return []

class GetAccountBalance(FormValidationAction):
    """Collects user information to provide account balance details"""

    def name(self):
        return "get_account_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")

        # Make a request to the authentication service to verify the password
        auth_url = f"https://backend-5glg.onrender.com/{username}/{password}"  # Replace with your actual URL
        response = requests.get(auth_url)

        if response.status_code == 200 and response.json().get("status") == "success":
            # Password is correct
            # Continue with fetching account balance
            account_number = tracker.get_slot("account_number")
            # You can use the account_number to fetch actual account balance from your backend/database
            account_balance = fetch_account_balance(username, account_number)  # Implement this function
            if account_balance:
                dispatcher.utter_message(f"Your account balance is Rs. {account_balance}.")
            else:
                dispatcher.utter_message("Sorry, we couldn't find your account balance.")
        else:
            # Password is incorrect
            dispatcher.utter_message("Invalid username or password. Please try again.")

        return []

class GetAccountTransactions(Action):
    """Collects user information to provide account transaction details"""

    def name(self) -> Text:
        return "get_account_transactions"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        password = tracker.get_slot("password")

        # Make a request to the authentication service to verify the password
        auth_url = f"https://backend-5glg.onrender.com/{username}/{password}"  # Replace with your actual URL
        response = requests.get(auth_url)

        if response.status_code == 200 and response.json().get("status") == "success":
            # Password is correct
            # Continue with fetching account transactions
            account_number = tracker.get_slot("account_number")
            # You can use the account_number to fetch actual account transactions from your backend/database
            transactions = fetch_account_transactions(username, account_number)  # Implement this function
            if transactions:
                response_message = "\n".join(transactions)
                dispatcher.utter_message(f"Here are your account transactions.\n{response_message}")
            else:
                dispatcher.utter_message("Sorry, we couldn't find your account transactions.")
        else:
            # Password is incorrect
            dispatcher.utter_message("Invalid username or password. Please try again.")

        return []

class GetResponseAction(Action):
    def name(self) -> Text:
        return "get_response"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Get the question from the user utterance
        question = tracker.latest_message["text"]

        # Send the question to the Flask app and get the response
        response = requests.post(
            "http://79f1-34-168-179-52.ngrok-free.app/", json={"question": question}
        ).json()

        dispatcher.utter_message(str(response)[12:-2])

        return []

# Implement the fetch_account_balance function as per your database/backend logic
def fetch_account_balance(username, account_number):
    # Implement the logic to fetch account balance from your database/backend
    # Replace this with your actual implementation
    url = f"https://backend-5glg.onrender.com/{username}/account"
    response = requests.get(url)
    data = response.json()

    if account_number in data:
        return str(data[account_number]["balance"])
    else:
        return None

# Implement the fetch_account_transactions function as per your database/backend logic
def fetch_account_transactions(username, account_number):
    # Implement the logic to fetch account transactions from your database/backend
    # Replace this with your actual implementation
    url = f"https://backend-5glg.onrender.com/{username}/account"
    response = requests.get(url)
    data = response.json()

    if account_number in data and "transaction" in data[account_number]:
        transactions = data[account_number]["transaction"]["3332"]
        transaction_details = [
            f"Amount: {str(transactions['amount'])}, "
            f"Description: {transactions['transaction_description']}, "
            f"Timestamp: {transactions['transaction_timestamp']}"
            # for transaction in transactions.values()
        ]
        return transaction_details
    else:
        return []
