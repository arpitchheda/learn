# python -m venv open_ai
# Activate the virtual environment open_ai
# python -m pip install openai==0.28.0

import openai

# Set OpenAI API configuration
openai.api_type = "azure"
openai.api_key = "{AZURE_OPENAI_SECRET_KEY}"
openai.api_base = "{AZURE_OPENAI_END_POINT}"
openai.api_version = "2024-02-15-preview"

# Define constants for the OpenAI model and parameters
AZURE_OPENAI_MODEL = 'gpt-4o-global-standard'
AZURE_OPENAI_SYSTEM_MESSAGE = "You are an IT Expert."
AZURE_OPENAI_TEMPERATURE = 0.0
AZURE_OPENAI_TOP_P = 1.0
AZURE_OPENAI_MAX_TOKENS = 50
AZURE_OPENAI_STOP_SEQUENCE = None
AZURE_OPENAI_FREQUENCY_PENALTY = 0.0
AZURE_OPENAI_PRESENCE_PENALTY = 0.0

def get_initial_message_list_from_prompt(prompt):
    """
    Create the initial conversation history with the system and user messages.
    
    Args:
    prompt (str): The user's prompt.
    
    Returns:
    list: Initial conversation history.
    """
    initial_conversation_history = [
        {"role": "system", "content": AZURE_OPENAI_SYSTEM_MESSAGE},
        {"role": "user", "content": prompt}
    ]
    return initial_conversation_history

def chat_completion(conversation_history):
    """
    Generate a response from the OpenAI model based on the conversation history.
    
    Args:
    conversation_history (list): The conversation history.
    
    Returns:
    dict: The response from the OpenAI model.
    """
    print("Conversation history " + str(conversation_history))
    response = openai.ChatCompletion.create(
        engine=AZURE_OPENAI_MODEL,
        messages=conversation_history,
        temperature=AZURE_OPENAI_TEMPERATURE,
        top_p=AZURE_OPENAI_TOP_P,
        max_tokens=AZURE_OPENAI_MAX_TOKENS,
        stop=AZURE_OPENAI_STOP_SEQUENCE,
        frequency_penalty=AZURE_OPENAI_FREQUENCY_PENALTY,
        presence_penalty=AZURE_OPENAI_PRESENCE_PENALTY,
        stream=False
    )
    return response

def chat_with_openai(prompt):
    """
    Handle the chat interaction with the OpenAI model.
    
    Args:
    prompt (str): The user's prompt.
    
    Returns:
    dict: The answer, conversation history, and response from the OpenAI model.
    """
    print("Prompt ", prompt)
    conversation_history = get_initial_message_list_from_prompt(prompt)
    response, answer = None, ''
    response = chat_completion(conversation_history)
    answer += response["choices"][0]["message"]["content"]
    conversation_history.append({"role": response["choices"][0]["message"]["content"], "content": answer})
    return {"answer": answer, "conversation_history": conversation_history, "response": response}

# Define a standard prompt for testing
standard_prompt = "Can you write essay 60 to 70 words on topic "

# Test the chat_with_openai function
test_response = chat_with_openai(standard_prompt + "Testing")
print(test_response["answer"])
print(test_response["response"]["usage"]["completion_tokens"])
print(test_response["response"]["choices"][0]["finish_reason"])

def chat_with_openai_v2(prompt, next_prompt="Your reply was incomplete due to the token limit. Can you please return the truncated part of your message and please dont add anything extra around it as I am appending your previous reply"):
    """
    Handle the chat interaction with the OpenAI model, including handling token limits.
    
    This function aims to manage conversations with the OpenAI model, ensuring that if the response is truncated due to token limits, 
    it can request the remaining part of the response and append it to the initial response.
    
    Args:
    prompt (str): The user's prompt.
    next_prompt (str): The prompt to use if the initial response is truncated.
    
    Returns:
    dict: The answer, conversation history, and response from the OpenAI model.
    """
    # Initialize the conversation history with the system and user messages
    conversation_history = get_initial_message_list_from_prompt(prompt)
    response, answer = None, ''
    reponse_list = []
    
    # Get the initial response from the OpenAI model
    response = chat_completion(conversation_history)
    reponse_list.append(response)
    
    # Check if the response was truncated due to token limits
    if response["choices"][0]["finish_reason"] == 'length':
        # Append the initial response to the answer
        answer += response["choices"][0]["message"]["content"]
        # Update the conversation history with the initial response
        conversation_history.append({"role": response["choices"][0]["message"]["role"], "content": answer})
        # Add the next prompt to request the remaining part of the response
        conversation_history.append({"role": "user", "content": next_prompt})
        # Get the next part of the response from the OpenAI model
        next_response = chat_completion(conversation_history)
        # Append the next part of the response to the answer
        answer += " " + next_response["choices"][0]["message"]["content"]
        # Update the conversation history with the next part of the response
        conversation_history.append({"role": next_response["choices"][0]["message"]["role"], "content": answer})
        reponse_list.append(next_response)
    else:
        # If the response was not truncated, append it to the answer
        answer += response["choices"][0]["message"]["role"]
        # Update the conversation history with the complete response
        conversation_history.append({'role': response["choices"][0]["message"]["role"], 'content': answer})
    
    # Return the final answer, conversation history, and list of responses
    return {"answer": answer, "conversation_history": conversation_history, "response": reponse_list}


# Define a list of topics for testing
topic_list = ["Testing", "Cloud", "Web Application"]

# Test the chat_with_openai_v2 function with different topics
for topic in topic_list:
    print("Topic Name " + topic)
    test_response_v2 = chat_with_openai_v2(standard_prompt + topic)
    print("For Topic Name " + topic + " " + test_response_v2["answer"])
    print(test_response_v2["response"][0]["usage"]["completion_tokens"])
    print(test_response_v2["response"][0]["choices"][0]["finish_reason"])
    if len(test_response_v2["response"]) > 1:
        print(test_response_v2["response"][1]["usage"]["completion_tokens"])
        print(test_response_v2["response"][1]["choices"][0]["finish_reason"])
