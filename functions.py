"""This file gets the form data and sends the user info gathered through the bot to fill
Google form.
"""

import requests


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup


from config import view_url, response_url


def get_problems() -> list:
    """Get the list of problems

    Returns:
        list: Problems
    """
    
    problems = []
    
    website = requests.get(view_url)
    soup = BeautifulSoup(website.text, 'lxml')
    
    for i in soup.find_all('span'):
        try:
            if i['dir'] == 'auto':
                problems.append(i.text)
        except:
            pass
    
    return problems


def init_problems_keyboard() -> InlineKeyboardMarkup:
    """Create Inline Keyboard from the problems with respective callback data

    Returns:
        InlineKeyboardMarkup: Keyboard
    """
    
    problems = get_problems()
    
    problems_keyboard = InlineKeyboardMarkup()
    
    for i in problems:
        callback = 'problem_' + i
        button = InlineKeyboardButton(i, callback_data=callback)
        problems_keyboard.add(button)
    
    return problems_keyboard


def insert_report(name: str, problem: str, score: int) -> str:
    """Send user info to fill the form

    Args:
        name (str): User name
        problem (str): User's problem
        score (int): User's score

    Returns:
        str: Completion message
    """
    
    form_data = {
        'entry.1993810016': name,
        'entry.1967993514': problem,
        'entry.70599208': score,
    }
    
    requests.post(response_url, data=form_data)
    return "Report sent!"