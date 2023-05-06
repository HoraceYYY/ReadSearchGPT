from Google import google, async_google
from Google import utils, async_utils
from termcolor import colored
import time, asyncio


if __name__ == "__main__":
    program = input('Enter "1" to run asycn or "0" to run linear: ')
    start_time = time.time()
    topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
    print(colored("\nPlease list 3 outcomes your would like to achieve!", "blue",attrs=["bold", "underline"]))
    objectives_input = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]
    non_empty_objectives = [f"{topic}: {obj}" for i, obj in enumerate(objectives_input) if obj]
    objectives = "\n".join(non_empty_objectives) # this is a str for open ai prompts
    print(colored("\nIf there is a domain you would like to search within, paste any link from the domain. Otherwise enter 'None'.", "blue", attrs=["bold", "underline"]))
    userDomain = input(colored("Search Domain: ", "blue", attrs=["bold"])).lower()
    max_depth = utils.searchType()

    resultLinks = []
    for objective in non_empty_objectives:
        if userDomain != "none": # if the user wants to search within a domain
            searchDomain = async_utils.get_domain(userDomain)
            objective = objective + " site:" + searchDomain
        
        resultLinks += async_google.google_official_search(objective)

    if program == "1":
        results = asyncio.run(async_google.main(resultLinks, topic, objectives, searchDomain, max_depth))
    elif program == "0":
        results = google.searchContent(resultLinks, topic, objectives, searchDomain, max_depth)
    else:
        print("Invalid input.")
        exit()
           
    print("\U0001F4AF\U0001F4AF\U0001F4AF SEARCH COMPLETED! \n\U0001F603\U0001F603\U0001F603 Have a wonderful day!\n\n") 
    end_time = time.time()
    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = int(execution_time % 60)

    print(f"Execution time: {hours} hours, {minutes} minutes, {seconds} seconds \n\n")

