from openai import OpenAI
import ast

client = OpenAI()

msgSystem = """You extract the most important and relevant entities from a text and find how they are connected."""


def extractEntities(query: str, data: str, model: str = "gpt-3.5-turbo"):
   """Extract entities relevant to the query from the given data

   Parameters:
   query: the entity from the input query
   data: text with information related to the query
   model: "gpt-3.5-turbo" is the default model, "gpt-4-turbo-preview" is recommended but it's more expensive
   """
   # the data is provided at the end of our query
   msgEntities = f"""Identify all unique specific entities related to {query} that are mentioned in the text below. These could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text.\n\nText:\n\"\"\"\n{data}\n\"\"\""""
   
   messages=[
      {"role": "system", "content": msgSystem},
      {"role": "user", "content": msgEntities}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=256,
      temperature=1 # min: 0, max: 2
   )

   # return the context (previous messages in the chat may be needed for context in the future) and the LLM output
   return messages, completion.choices[0].message


def extractRelationshipsFromEntities(query: str, context: list = [], model: str = "gpt-3.5-turbo"):
   """Extract relevant relationships/connections between the query and entities provided in the context
   
   Parameters:
   query: the entity from the input query
   context: expected to contain previous messages in the LLM chat, providing context, such as text related to the query and identified entities from the text
   model: "gpt-3.5-turbo" is the default model, "gpt-4-turbo-preview" is recommended but it's more expensive
   """
   msgRelationships = f"""Extract the relevant relationships between {query} and the entities you identified above. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc."""

   messages = context + [{"role": "user", "content": msgRelationships}]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=256,
      temperature=1
   )

   # return the context (previous messages) and the LLM output
   return messages, completion.choices[0].message


def extractRelationshipsDirectly(query: str, data: str, model: str = "gpt-3.5-turbo"):
   """Extract relationships/connections between the query and relevant entities found in the given data
   
   Parameters:
   query: the entity from the input query
   data: text with information related to the query
   model: "gpt-3.5-turbo" is the default model, "gpt-4-turbo-preview" is recommended but it's more expensive
   """
   # the data is provided at the end of our query
   msgRelationships = f"""Step 1: Identify all unique specific entities related to {query} that are mentioned in the text below. These entities could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text.\n\nStep 2: Extract the relevant relationships between {query} and the entities you have identified. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc.\n\nOnly output the list of relationships.\n\nText:\n\"\"\"\n{data}\n\"\"\""""

   messages=[
      {"role": "system", "content": msgSystem},
      {"role": "user", "content": msgRelationships}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=256,
      temperature=1
   )

   # return the context (previous messages) and the LLM output
   return messages, completion.choices[0].message



def textToJson(data: str, max_tokens: int = 1024, model: str = "gpt-3.5-turbo"):
   """Transform the output text returned from the LLM model (i.e. the relationships) into a JSON string
   Note: This function uses an LLM to convert the data into a JSON. Alternatively, a function using regular expressions and string 
   operations can be used, but the input data is a string returned by an LLM, so its structure might not be consistent"""

   msgList = f"""Convert the list of relationships below into a JSON object:\n\nschema:\n\{{\n "relationships": {{\"src\", \"relationship\", \"tgt\"\}}[]\n}}\n\n\"\"\"{data}\"\"\""""

   messages=[
      {"role": "system", "content": "JSON"},
      {"role": "user", "content": msgList}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      response_format={"type": "json_object"}, # enable JSON mode - the model is constrained to only generate strings that parse into valid JSON object
      max_tokens=max_tokens
   )

   return completion.choices[0].message.content


def textToList(data: str, max_tokens: int = 1024, model: str = "gpt-3.5-turbo"):
   """Transform the output text returned from the LLM model (i.e. the relationships) into a list of tuples corresponding to the relatonships.
   Note: This function uses an LLM to convert the data into a Python list. Alternatively, a function using regular expressions and string 
   operations can be used, but the input data is a string returned by an LLM, so its structure might not be consistent"""

   msgList = f"""Convert the list of relationships below into a list of tuples. Each tuple should have 3 elements of type string. Only output a Python list.\n\n\"\"\"{data}\"\"\""""

   messages=[
      {"role": "system", "content": """Output a Python list."""},
      {"role": "user", "content": msgList}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=max_tokens
   )

   # Parse and clean the LLM output
   relationships = completion.choices[0].message.content
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




# def textToJson(text: str):
#    """Transform the output text returned from the LLM model (i.e. the relationships) into a JSON for output
#    Note: This function relies on string operations and expects a predictable and structured input text"""
#    jsonObjects = []
#    # Split the string into groups based on the comma
#    groups = text.split(',')
#    for relationship in groups:
#       try:
#          src, rellationship, tgt = map(str.strip, relationship.split('-'))
#          jsonObjects.append({"source": src, "relation": rellationship, "target": tgt})
#       except:
#          print(map(str.strip, relationship.split('-')))
#          raise Exception('Relationships should have a format "entity 1 - relation - entity 2"')
   
#    return json.dumps(jsonObjects, indent=4)

# def textToList(text: str):
#    """Transform the output text returned from the LLM model (i.e. the relationships) into a list of tuples corresponding to the relatonships
#    Note: This function relies on string operations and expects a predictable and structured input text"""
#    # Split the string into groups based on the comma
#    groups = text.split(',')
#    # Process each group (split by the dash and trim whitespaces) to create triplets
#    relationships = [tuple(map(str.strip, group.split('-'))) for group in groups]

#    return relationships
