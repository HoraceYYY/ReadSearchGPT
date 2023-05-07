from Google import google, async_google
from Google import utils, async_utils
from termcolor import colored
import time, asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

class DepthLevel(str, Enum):
    quick = "quick"
    thorough = "thorough"
    deep = "deep"

class Search(BaseModel):
    program = 1
    topic: str
    objectives_input: list[str]
    searchDomain: str | None = None
    max_depth: DepthLevel = DepthLevel.quick  # Use the DepthLevel Enum

    _depth_mapping = {
        DepthLevel.quick: 1,
        DepthLevel.thorough: 2,
        DepthLevel.deep: 3,
    }

    def get_depth_value(self):
        return self._depth_mapping.get(self.max_depth, None)

app = FastAPI()

@app.post("/search/")
async def startSearching(search: Search):
    start_time = time.time()
    topic = search.topic
    objectives_input = search.objectives_input
    userDomain = search.searchDomain
    max_depth = search.get_depth_value()  # Get the integer value of max_depth

    non_empty_objectives = [f"{topic}: {obj}" for i, obj in enumerate(objectives_input) if obj]
    objectives = "\n".join(non_empty_objectives) # this is a str for open ai prompts
    resultLinks = []
    for objective in non_empty_objectives:
        if userDomain != None: # if the user wants to search within a domain. None if the user keep the UI field empty
            searchDomain = async_utils.get_domain(userDomain)
            objective = objective + " site:" + searchDomain
        
        resultLinks += async_google.google_official_search(objective, max_depth)

    if program == "1":
        status, file_path = asyncio.run(async_google.main(resultLinks, topic, objectives, searchDomain, max_depth))
    elif program == "0":
        google.searchContent(resultLinks, topic, objectives, searchDomain, max_depth)

    end_time = time.time()
    execution_time = end_time - start_time
    
    return status, execution_time, file_path




if __name__ == "__main__":
    program = input('Enter "1" to run asycn or "0" to run linear: ')
    start_time = time.time()
    topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
    print(colored("\nPlease list 3 outcomes your would like to achieve!", "blue",attrs=["bold", "underline"]))
    objectives_input = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]
    non_empty_objectives = [f"{i + 1}. {obj}" for i, obj in enumerate(objectives_input) if obj]
    objectives = topic + "\n"+ "\n".join(non_empty_objectives)
    print(colored("\nIf there is a domain you would like to search within, paste any link from the domain. Otherwise enter 'None'.", "blue", attrs=["bold", "underline"]))
    searchDomain = input(colored("Search Domain: ", "blue", attrs=["bold"])).lower()
    max_depth = utils.searchType()

    if searchDomain != "none":
        searchDomain = utils.get_domain(searchDomain)
        topic = topic + " site:" + searchDomain
    resultLinks = google.google_official_search(topic)
    
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

