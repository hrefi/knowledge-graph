from openai import OpenAI
import ast

client = OpenAI()

msg_system = """You extract the most important and relevant entities from a text and find how they are connected."""

def get_completion(messages, model="gpt-3.5-turbo", max_tokens=256, temperature=1, response_type=None):
   args = {
      "model": model,
      "messages": messages,
      "max_tokens": max_tokens,
      "temperature": temperature # min: 0, max: 2
   }

   if response_type is not None:
      args["response_type"] = response_type

   completion = client.chat.completions.create(**args)

   return completion.choices[0].message


def extract_entities(query: str, data: str, model: str = "gpt-3.5-turbo"):
   """Extract entities relevant to the query from the given data using OpenAI's GPT model.

   Parameters:
      query (str): The entity from the input query.
      data (str): Text with information related to the query.
      model (str): Model to use, defaults to "gpt-3.5-turbo".

   Returns:
      tuple: A tuple containing the context (list of messages) and the model's output.
   """
   # Constructing the Prompt:

   # Identify all unique specific entities related to {query} that are mentioned in the text below. 
   # These entities could include people, companies, locations, universities, professional affiliations, etc.
   # Only include entities mentioned in the text.
   msg_entities = f"""Identify all unique specific entities related to {query} that are mentioned in the text below. These entities could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text."""
   # Text:
   # """
   # {data}
   # """
   msg_entities += f"""\n\nText:\n\"\"\"\n{data}\n\"\"\""""
   
   messages=[
      {"role": "system", "content": msg_system},
      {"role": "user", "content": msg_entities}
   ]

   completion = get_completion(messages=messages, model=model)

   # return the context (previous messages in the chat may be needed for context in the future) and the LLM output
   return messages, completion


def extract_relationships_from_entities(query: str, context: list = [], model: str = "gpt-3.5-turbo"):
   """Extract relevant relationships between the query and entities provided in the context
   
   Parameters:
      query (str): The entity from the input query.
      context (list): Previous messages in the chat, providing context.
      model (str): Model to use, defaults to "gpt-3.5-turbo".

   Returns:
      tuple: A tuple containing the updated context and the model's output.
   """
   # Constructing the Prompt:

   # Extract the relevant relationships between {query} and the entities you identified above. 
   # The relationships should be in the format "{query} - relationship - identified entity". 
   # The relationship should be maximum 2 words and can be a verb or a noun. 
   # The relationship should not be a form of the verb 'be' or 'have'.
   # Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc., not an attribute to {query}.
   msg_relationships = f"""Extract the relevant relationships between {query} and the entities you identified above. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. The relationship should not be a form of the verb 'be' or 'have'. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc., not an attribute to {query}."""

   messages = context + [{"role": "user", "content": msg_relationships}]

   completion = get_completion(messages=messages, model=model)

   # return the context (previous messages) and the LLM output
   return messages, completion


def extract_relationships_directly(query: str, data: str, model: str = "gpt-3.5-turbo"):
   """Extract relationships/connections between the query and relevant entities found in the data
   
   Parameters:
      query (str): The entity from the input query.
      data (str): Text with information related to the query.
      model (str): Model to use, defaults to "gpt-3.5-turbo".

   Returns:
      tuple: A tuple containing the context and the model's output.
   """
   # Constructing the Prompt:

   # Step 1: Identify all unique specific entities related to {query} that are mentioned in the text below. 
   # These entities could include people, companies, locations, universities, professional affiliations, etc. 
   # Only include entities mentioned in the text.
   msg_relationships = f"""Step 1: Identify all unique specific entities related to {query} that are mentioned in the text below. These entities could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text."""
   # Step 2: Extract the relevant relationships between {query} and the entities you have identified. 
   # The relationships should be in the format "{query} - relationship - identified entity". 
   # The relationship should be maximum 2 words and can be a verb or a noun. 
   # The relationship should not be a form of the verb 'be' or 'have'. 
   # Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc., not an attribute to {query}.
   msg_relationships += f"""\n\nStep 2: Extract the relevant relationships between {query} and the entities you have identified. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. The relationship should not be a form of the verb 'be' or 'have'. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc., not an attribute to {query}."""
   # Step 3: Ensure that all relationships follow the rules:
   # 1. The relationships must be in the format "{query} - relationship - identified entity".
   # 2. The relationship must not be a form of the verb 'be', e.g., 'is', 'are', 'was', 'were'.
   # 3. The relationship must not be a form of the verb 'have', e.g., 'has', 'had'.
   # Remove the relationships that don't follow the rules.
   msg_relationships += f"""\n\nStep 3: Ensure that all relationships follow the rules:\n1. The relationships must be in the format \"{query} - relationship - identified entity\".\n2. The relationship must not be a form of the verb 'be', e.g., 'is', 'are', 'was', 'were'.\n3. The relationship must not be a form of the verb 'have', e.g., 'has', 'had'.\n Remove the relationships that don't follow the rules."""
   # Think step-by-step. Only output the list of relationships.
   msg_relationships += """\n\nThink step-by-step. Only output the list of relationships."""
   # Text:
   # """
   # {data}
   # """
   msg_relationships += f"""\n\nText:\n\"\"\"\n{data}\n\"\"\""""

   messages=[
      {"role": "system", "content": msg_system},
      {"role": "user", "content": msg_relationships}
   ]

   completion = get_completion(messages=messages, model=model)

   # return the context (previous messages) and the LLM output
   return messages, completion



def text_to_json(data: str, max_tokens: int = 4096, model: str = "gpt-3.5-turbo"):
   """Transform text returned from the model, i.e. the relationships, into a JSON string using an LLM.

   Parameters:
      data (str): Text to transform.
      max_tokens (int): Maximum number of tokens for the LLM.
      model (str): Model to use, defaults to "gpt-3.5-turbo".

   Returns:
      str: The transformed text as a JSON string.
   """
   # Constructing the Prompt:

   # Convert the list of relationships below into a JSON object:
   msg_list = """Convert the list of relationships below into a JSON object:"""
   # schema:
   # {
   #  "relationships": {"src", "relationship", "tgt"}[]
   # }
   msg_list += f"""\n\nschema:\n{{\n "relationships": {{\"src\", \"relationship\", \"tgt\"}}[]\n}}"""
   # """
   # {data}
   # """
   msg_list += f"""\n\n\"\"\"\n{data}\n\"\"\""""

   messages=[
      {"role": "system", "content": "JSON"},
      {"role": "user", "content": msg_list}
   ]

   # enable JSON mode - the model is constrained to only generate strings that parse into valid JSON object
   completion = get_completion(
      messages=messages, 
      model=model, 
      max_tokens=max_tokens, 
      response_format={"type": "json_object"}
   )

   return completion.content


def text_to_list(data: str, max_tokens: int = 4096, model: str = "gpt-3.5-turbo"):
   """Transform text from the model, i.e. the relationships, into a list of tuples using an LLM.

   Parameters:
      data (str): Text to transform.
      max_tokens (int): Maximum number of tokens for the LLM.
      model (str): Model to use, defaults to "gpt-3.5-turbo".

   Returns:
      list: The transformed text as a list of tuples.
   """
   # Constructing the Prompt:
   
   # Convert the list of relationships below into a list of tuples. 
   # Each tuple should have 3 elements of type string. Only output a Python list.
   msg_list = """Convert the list of relationships below into a list of tuples. Each tuple should have 3 elements of type string. Only output a Python list."""
   # """
   # {data}
   # """
   msg_list += f"""\n\n\"\"\"\n{data}\n\"\"\""""

   messages=[
      {"role": "system", "content": """Output a Python list."""},
      {"role": "user", "content": msg_list}
   ]

   completion = get_completion(
      messages=messages, 
      model=model, 
      max_tokens=max_tokens
   )

   # Parse and clean the LLM output
   relationships = completion.content
   try:
      # Remove substrings around Python code and parse the output
      relationships = relationships.replace("```python", "").replace("```", "").strip()
      relationships = ast.literal_eval(relationships)

      # Validate that the parsed output is indeed a list
      if not isinstance(relationships, list):
         raise ValueError("Parsed output is not a list.")
      
      return relationships
   except (ValueError, SyntaxError) as e:
      raise ValueError("Failed to parse LLM output into a Python list.") from e

