from Google import google
from Google import utils
from termcolor import colored


if __name__ == "__main__":
        
    topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
    print(colored("\nPlease list 3 outcomes your would like to achieve!", "blue",attrs=["bold", "underline"]))
    objectives_input = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]
    non_empty_objectives = [f"{i + 1}. {obj}" for i, obj in enumerate(objectives_input) if obj]
    objectives = "\n".join(non_empty_objectives)
    maxDepth = utils.searchType()
    #GPTsearchQuery = google.searchTitle(full_topic)
    #searchQuery = utils.searchQueryOverride(GPTsearchQuery)
    resultLinks = google.google_official_search(topic)
    results = google.searchContent(resultLinks, topic, objectives, maxDepth)
           
    print("\U0001F4AF\U0001F4AF\U0001F4AF SEARCH COMPLETED! \n\U0001F603\U0001F603\U0001F603 Have a wonderful day!\n\n") 


