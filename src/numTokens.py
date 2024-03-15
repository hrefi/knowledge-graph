# Helper functions to find the length in tokens of a query before calling the OpenAI API

import tiktoken

def numTokensStr(string: str, model: str = "gpt-4"):
   """Calculate the number of tokens in a text string."""
   try:
      encoding = tiktoken.encoding_for_model(model)
   except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")

   numTokens = len(encoding.encode(string))
   return numTokens

def numTokensChat(messages: list, model: str ="gpt-4"):
   """Calculate approximately the number of tokens in a list of messages."""
   try:
      encoding = tiktoken.encoding_for_model(model)
   except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")

   numTokens = 0
   for message in messages:
      numTokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
      for key, value in message.items():
         numTokens += len(encoding.encode(value))
         # if key == "name":  # if there's a name, the role is omitted
         #    numTokens += -1  # role is always required and always 1 token
   numTokens += 2  # every reply is primed with <im_start>assistant
   return numTokens
