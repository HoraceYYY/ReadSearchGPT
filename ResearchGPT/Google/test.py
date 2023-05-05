from bs4 import BeautifulSoup
import os, requests, sys, json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import utils, math
import openai
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, unquote_plus, urljoin
from termcolor import colored

# topic = input(colored("What would you like to search:", "blue", attrs=["bold", "underline"]) + " ")
# objectives_input = [input(colored(f"Objective {i + 1}: ", "blue", attrs=["bold"])) for i in range(3)]
# non_empty_objectives = [f"{i + 1}. {obj}" for i, obj in enumerate(objectives_input) if obj]
# objectives = topic + "\n"+ "\n".join(non_empty_objectives)


import os
import pandas as pd
import asyncio

async def updateExcel(excel_name, excelsheet, data):
    folder_path = 'Results'
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    file_name = f"{folder_path}/{excel_name}.xlsx"  # Create the Excel file name
    if os.path.isfile(file_name):  # Check if the file exists
        xls = await asyncio.to_thread(pd.ExcelFile, file_name)  # If the file exists, read the existing Excel file
        if excelsheet in xls.sheet_names:  # Check if the sheet exists in the Excel file
            sheet_data = {}  # Create a dictionary to store all the sheets because they will be overwritten
            for sheet in xls.sheet_names:  # Read all the sheets and store them in the dictionary
                if sheet == excelsheet:
                    sheet_data[sheet] = data.copy()  # Overwrite the specified sheet with the updated data
                else:
                    sheet_df = await asyncio.to_thread(pd.read_excel, xls, sheet_name=sheet)
                    sheet_data[sheet] = sheet_df  # Store the data of the other sheets

            writer = await asyncio.to_thread(pd.ExcelWriter, file_name)  # Write all the sheets to the Excel file
            for sheet, df in sheet_data.items():
                await asyncio.to_thread(df.to_excel, writer, sheet_name=sheet, index=False)
            await asyncio.to_thread(writer.save)
        else:  # If the sheet doesn't exist, write the new data as a new sheet
            writer = await asyncio.to_thread(pd.ExcelWriter, file_name, mode='a')
            await asyncio.to_thread(data.to_excel, writer, sheet_name=excelsheet, index=False)
            await asyncio.to_thread(writer.save)
    else:  # If the file doesn't exist, write the new data as a new sheet
        await asyncio.to_thread(data.to_excel, file_name, sheet_name=excelsheet, index=False)
    return

# Some sample data for testing
data = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

asyncio.run(updateExcel('test_file', 'Sheet1', data))



