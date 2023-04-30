from Google import google
from Google import utils
from termcolor import colored


if __name__ == "__main__":

    chat_transcript = []
    # get user input from terminal

    topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
    print(colored("\nPlease list 3 outcomes your would like to achieve!", "blue",attrs=["bold", "underline"]))
    outcome1 = input(colored("Outcome 1: ", "blue", attrs=["bold"]))
    outcome2 = input(colored("Outcome 2: ", "blue", attrs=["bold"]))
    outcome3 = input(colored("Outcome 3: ", "blue", attrs=["bold"]))
    full_topic = "Research Topic: " + topic + "\nTarget Outcome 1: " + outcome1 + "\nTarget Outcome 2: " + outcome2 + "\nTarget Outcome 3: " + outcome3
    maxDepth = utils.searchType()
    GPTsearchQuery = google.searchTitle(full_topic)
    searchQuery = utils.searchQueryOverride(GPTsearchQuery)
    resultLinks = google.google_official_search(searchQuery)
    results = google.searchContent(resultLinks,searchQuery, maxDepth)
            # Save the DataFrames to an Excel file with separate sheets
    print("'\U0001F4AF' SEARCH COMPLETED! Have a wonderful day \U0001F603\n\n") 


