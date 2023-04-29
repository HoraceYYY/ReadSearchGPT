from Google import google
from Google import utils
import pandas as pd

if __name__ == "__main__":

    chat_transcript = []
    # get user input from terminal
    while True:
        topic = input("What would you like to research (DONE to quite): ")
        if topic.lower() == "done":
            print("Bye!")
            exit()
        print("List 3 key outcomes your would like to achieve!")
        outcome1 = input("Outcome 1: ")
        outcome2 = input("Outcome 2: ")
        outcome3 = input("Outcome 3: ")
        full_topic = "Research Topic: " + topic + "\nTarget Outcome 1: " + outcome1 + "\nTarget Outcome 2: " + outcome2 + "\nTarget Outcome 3: " + outcome3
        
        maxDepth = utils.searchType()
        searchQuery = google.searchTitle(full_topic)
        resultLinks = google.google_official_search(searchQuery)
        results = google.searchContent(resultLinks,searchQuery, maxDepth)
                # Save the DataFrames to an Excel file with separate sheets
        with pd.ExcelWriter(f'{searchQuery}.xlsx', engine='openpyxl') as writer:
            results['clean'].to_excel(writer, sheet_name='Filtered Data', index=False)
            results['raw'].to_excel(writer, sheet_name='Raw Data', index=False)
        
        print("SEARCH COMPLETED! \n\n") 


