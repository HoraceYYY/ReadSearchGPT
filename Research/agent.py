from Google import google
from Google import utils

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
        google.searchContent(resultLinks,searchQuery, maxDepth)
        print("SEARCH COMPLETED! \n\n") 


