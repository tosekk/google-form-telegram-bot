"""This file handles messages and keyboard callbacks.
"""

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from main import bot, dp
from functions import init_problems_keyboard, insert_report


# Dictionary to hold the answers
user_info = {}


class Form(StatesGroup):
    """State machine class

    Args:
        StatesGroup (StatesGroup): States Group parent class
    """
    name = State()
    score = State()


@dp.message_handler(commands=['start'])
async def welcome(message: Message) -> None:
    """Welcome function

    Args:
        message (Message): /start command message
    """
    
    hello_message = "Hello! What is your name?"
    
    await Form.name.set()
    await bot.send_message(message.chat.id, hello_message)

    
@dp.message_handler(state=Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """Get and save the name in user_info

    Args:
        message (Message): User's name
        state (FSMContext): name state
    """
    
    user_info["fullname"] = message.text
    problems_keyboard = init_problems_keyboard()
    
    await state.finish()
    await bot.send_message(message.chat.id,
                           f"Okay, {message.text}. What is your problem?",
                           reply_markup=problems_keyboard)
 

@dp.message_handler(state=Form.score)
async def process_score(message: Message, state: FSMContext) -> None:
    """Get and save the score in user_info

    Args:
        message (Message): Number between 1 and 10
        state (FSMContext): score state
    """
    
    score = int(message.text)
    
    result = insert_report(user_info['fullname'], user_info['problem'],
                           score)
    
    await state.finish()
    await bot.send_message(message.chat.id, result)
    await bot.send_message(message.chat.id,
                           "Thank you for filling the survey!")
 

@dp.callback_query_handler(lambda call: call.data.startswith('problem_'))
async def process_callback_problems(call: CallbackQuery) -> None:
    """Get the problem and save it in user_info

    Args:
        call (CallbackQuery): Pressed button
    """
    
    await bot.answer_callback_query(call.id)
    
    problem = call.data.split('_')[1]
    user_info["problem"] = problem
    score_message = "Please write your score between 1 and 10. 1 - Very Bad, 10 - Very Good."
    
    await Form.score.set()
    await bot.send_message(call.message.chat.id, score_message)
    