from Google import google
from Google import utils
import pandas as pd
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
    searchQuery = google.searchTitle(full_topic)
    searchQuery = utils.searchQueryOverride(searchQuery)
    resultLinks = google.google_official_search(searchQuery)
    results = google.searchContent(resultLinks,searchQuery, maxDepth)
            # Save the DataFrames to an Excel file with separate sheets
    with pd.ExcelWriter(f'{searchQuery}.xlsx', engine='openpyxl') as writer:
        results['clean'].to_excel(writer, sheet_name='Filteblue Data', index=False)
        results['raw'].to_excel(writer, sheet_name='Raw Data', index=False)
    
    print("SEARCH COMPLETED! Have a wonderful day :)\n\n") 


