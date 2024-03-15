# Helper functions to find the length in tokens of a query before calling the OpenAI API

import tiktoken

def num_tokens_str(string: str, model: str = "gpt-4"):
   """Calculate the number of tokens in a text string.
   
   Parameters:
      string (str): The input text to tokenize.
      model (str): The model used for encoding, default is 'gpt-4'.

   Returns:
      int: The number of tokens in the input string.
   """
   try:
      encoding = tiktoken.encoding_for_model(model)
   except KeyError:
      # default to 'cl100k_base' encoding on failure
      encoding = tiktoken.get_encoding("cl100k_base")

   num_tokens = len(encoding.encode(string))
   return num_tokens

def num_tokens_chat(messages: list, model: str ="gpt-4"):
   """Calculate approximately the number of tokens in a list of messages.
   
   Parameters:
      messages (list): A list of message dictionaries with 'role' and 'content'.
      model (str): The model used for encoding, default is 'gpt-4'.

   Returns:
      int: The approximate total number of tokens across all messages.
   """
   try:
      encoding = tiktoken.encoding_for_model(model)
   except KeyError:
      # default to 'cl100k_base' encoding on failure
      encoding = tiktoken.get_encoding("cl100k_base")

   num_tokens = 0
   for message in messages:
      # Add tokens for the message wrapper and content.
      num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
      for key, value in message.items():
         num_tokens += len(encoding.encode(value))

   num_tokens += 2  # Every reply is primed with <im_start>assistant
   return num_tokens
