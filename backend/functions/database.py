import json
import random

def get_recent_messages():

  # Define the file name
  file_name = "Conversaciones.json"

  #Get prompt
  with open("data.json") as f:
    data = json.load(f)

  #asignar variable
  prompt = ""
  
  learn_instruction = {"role": "system", 
                       "content": prompt + "Keep your answers under 30 words"}
  
  # Initialize messages
  messages = []

#   Add Random Element
  x = random.uniform(0, 1)
  if x < 0.2:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will have some sarcastic humour. "
  elif x < 0.5:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will be in a rude "
  else:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will have some dark humour "

  # Append instruction to message
  messages.append(learn_instruction)

  # Get all messages
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append all rows of data
      if data:
        for item in data:
          messages.append(item)
  except:
    pass

  
  # Return messages
  return messages

# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "Conversaciones.json"

  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)