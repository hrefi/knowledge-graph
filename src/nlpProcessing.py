# #### Prompting

# System (?): "You extract the most important and relevant specific entities from a text and find how they relate."

# Identify Entities (?):
# """Identify all unique specific entities related to {query} that are mentioned in the text below. These entities could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text."""
# + identify all unique entities related to {X} mentioned in the text. This includes organizations, awards, clubs, people, and other specific entities: "Given the text, identify all unique specific entities (organizations, awards, clubs, and teams) mentioned in relation to X."
# + Given the text, identify all unique specific entities (like organizations, awards, clubs, teams) mentioned in relation to Hristo Stoichkov.
# - Examples: professional roles, educational background, investment activities, board positions, geographical location, personal interests, achievements, investments, co-workers, etc.
# - Categorise (?): Prompt the model to identify and list named entities related to Stoichkov, categorizing them into persons, organizations, awards, etc.
# + Remove duplicate entities

# Extract Relationships from Entities:
# """Extract the relevant relationships between {query} and the entities you identified above. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. The relationship should not be a form of the verb 'be', e.g., 'is', 'are', 'was', 'were'. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc."""
# + Extract Relationships - once you have a list of entities, extract relationships between X and these entities. Clearly state the format of the relationships (with example) and the constraints for the relationships (e.g., maximum of two words, the relationship should be a verb or a noun): "For each entity identified related to X, extract the relationship between them and X. The relationship should be expressed in a maximum of two words, and the output format should be 'X - relationship - entity'. Focus on relationships where the entity is a specific organization, award, person, professional affiliation, etc."
# + extract all relevant entities from the information above and the relationships between Hristo Stoichkov and these entities. The output should be a list of relationships in the format "entity from the  input - relationship - entity from the text". The relationship can be a verb (e.g., works, located, etc.) and sometimes a noun (e.g., co-worker, investment, etc.) and should be maximum 2 words. The entity from the text should be a specific entity, i.e. organization, award, person, professional affiliations, etc.
# + extract the relationships between X and various entities, adhering to the format "entity from the input - relationship - entity from the text"

# Extract Relationships Directly (without Identifying Entities first):
# """Step 1: Identify all unique specific entities related to {query} that are mentioned in the text below. These entities could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text.\n\nStep 2: Extract the relevant relationships between {query} and the entities you have identified. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. The relationship should not be a form of the verb 'be', e.g., 'is', 'are', 'was', 'were'. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc.\n\nOnly output the list of relationships."""
# + identify all relevant entities and extract the relationships between Yigit Ihlamur and these entities in the specified format. Be concise and specific. Think step-by-step
# - Examples: If {query} is a person, these could be ... If {query} is a company, these could be ...
# + Prompt for Structured Outputs: "For each identified relationship involving Hristo Stoichkov, format the response as 'Entity 1 - Relationship - Entity 2'."
# - Relationships can be between the Entities found and other entities in the text
# - for any of the discovered entities find if they have relationships to other entities in the provided information
# + Refine the previously extracted relationships to ensure they follow the specified format strictly 'Hristo Stoichkov - relationship - entity' and the relationship is described in no more than two words. Simplify complex descriptions if necessary.

# JSON / Lists output
# + Give me that data as a python list of tuples of three elements, where for each "X-Y-Z" above there is a corresponding tuple (X, Z, Y)

# + directly come up with relationships without entities
# + output JSON/list
#    + create two functions to further do that
# + -- directly output JSON/list - didnt'work well
# - if the list of relationships is longer than 30 get only the top 30 (can be a parameter)

# Further Questions:
# """What relationships of the entity Vela Partners can you find in the text? The relationship should be maximum 2 words and can be a verb or a noun. Focus on specific relationships where the entity is not abstract, but a specific person, company, location, university, professional affiliation, etc. Only output the list of relationships."""
# (not implemented) Refinements and Verification:
# + Refinement (optional) - if the relationships extracted are too broad or not in the specified format, you can further refine the prompt to narrow down the responses or adjust the relationship descriptions: "Refine the previously extracted relationships to ensure they follow the specified format strictly 'X - relationship - entity' and the relationship is described in no more than two words. Simplify complex descriptions if necessary."
# - Verify and Validate: "Verify the completeness and accuracy of the relationships extracted. If any relationship is missing or inaccurately described, correct it based on the information provided."
# - Remove duplicate relationships (keep multiple relationships between the same two entities if they are different)
# - "Consider each relationship from above separately. ... Remove relationships that lack context."
# - Further: Design prompts that focus specifically on relationship extraction between entities: "Identify and describe the relationship between Hristo Stoichkov and any organizations or awards mentioned."
# - Further: Consider each relationship separately. Search the text for entities that relate in the same way as the current relationship. Add any new unique, relevant entities to the list if you find any.
# - Direct Questions - a second Bing search for each relationship (type): “Yigit Ihlamur” AND “Vela Partners” / "What teams did Hristo Stoichkov play for?"
# - Guided Extraction and Guided Extraction: "List all teams Hristo Stoichkov played for in a bullet point format."



from openai import OpenAI
import ast

client = OpenAI()

msg_system = """You extract the most important and relevant entities from a text and find how they are connected."""


def extract_entities(query: str, data: str, model: str = "gpt-3.5-turbo"):
   """Extract entities relevant to the query from the given data

   Parameters:
   query: the entity from the input query
   data: text with information related to the query
   model: "gpt-3.5-turbo" is the default model, "gpt-4-turbo-preview" is recommended but it's more expensive
   """
   # the data is provided at the end of our query
   msg_entities = f"""Identify all unique specific entities related to {query} that are mentioned in the text below. These could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text.\n\nText:\n\"\"\"\n{data}\n\"\"\""""
   
   messages=[
      {"role": "system", "content": msg_system},
      {"role": "user", "content": msg_entities}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=256,
      temperature=1 # min: 0, max: 2
   )

   # return the context (previous messages in the chat may be needed for context in the future) and the LLM output
   return messages, completion.choices[0].message


def extract_relationships_from_entities(query: str, context: list = [], model: str = "gpt-3.5-turbo"):
   """Extract relevant relationships/connections between the query and entities provided in the context
   
   Parameters:
   query: the entity from the input query
   context: expected to contain previous messages in the LLM chat, providing context, such as text related to the query and identified entities from the text
   model: "gpt-3.5-turbo" is the default model, "gpt-4-turbo-preview" is recommended but it's more expensive
   """
   msg_relationships = f"""Extract the relevant relationships between {query} and the entities you identified above. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. The relationship should not be a form of the verb 'be' or 'have'. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc., not an attribute to {query}."""

   messages = context + [{"role": "user", "content": msg_relationships}]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=256,
      temperature=1
   )

   # return the context (previous messages) and the LLM output
   return messages, completion.choices[0].message


def extract_relationships_directly(query: str, data: str, model: str = "gpt-3.5-turbo"):
   """Extract relationships/connections between the query and relevant entities found in the given data
   
   Parameters:
   query: the entity from the input query
   data: text with information related to the query
   model: "gpt-3.5-turbo" is the default model, "gpt-4-turbo-preview" is recommended but it's more expensive
   """
   # the data is provided at the end of our query
   msg_relationships = f"""Step 1: Identify all unique specific entities related to {query} that are mentioned in the text below. These entities could include people, companies, locations, universities, professional affiliations, etc. Only include entities mentioned in the text.\n\nStep 2: Extract the relevant relationships between {query} and the entities you have identified. The relationships should be in the format \"{query} - relationship - identified entity\". The relationship should be maximum 2 words and can be a verb or a noun. The relationship should not be a form of the verb 'be' or 'have'. Focus on relationships where the entity is a specific person, company, location, university, professional affiliation, etc., not an attribute to {query}.\n\nStep 3: Ensure that all relationships follow the rules:\n1. The relationships must be in the format \"{query} - relationship - identified entity\".\n2. The relationship must not be a form of the verb 'be', e.g., 'is', 'are', 'was', 'were'.\n3. The relationship must not be a form of the verb 'have', e.g., 'has', 'had'.\n Remove the relationships that don't follow the rules.\n\nThink step-by-step. Only output the list of relationships.\n\nText:\n\"\"\"\n{data}\n\"\"\""""

   messages=[
      {"role": "system", "content": msg_system},
      {"role": "user", "content": msg_relationships}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      max_tokens=256,
      temperature=1
   )

   # return the context (previous messages) and the LLM output
   return messages, completion.choices[0].message



def text_to_json(data: str, max_tokens: int = 2048, model: str = "gpt-3.5-turbo"):
   """Transform the output text returned from the LLM model (i.e. the relationships) into a JSON string
   Note: This function uses an LLM to convert the data into a JSON. Alternatively, a function using regular expressions and string 
   operations can be used, but the input data is a string returned by an LLM, so its structure might not be consistent"""

   msg_list = f"""Convert the list of relationships below into a JSON object:\n\nschema:\n\{{\n "relationships": {{\"src\", \"relationship\", \"tgt\"\}}[]\n}}\n\n\"\"\"{data}\"\"\""""

   messages=[
      {"role": "system", "content": "JSON"},
      {"role": "user", "content": msg_list}
   ]

   completion = client.chat.completions.create(
      model=model,
      messages=messages,
      response_format={"type": "json_object"}, # enable JSON mode - the model is constrained to only generate strings that parse into valid JSON object
      max_tokens=max_tokens
   )

   return completion.choices[0].message.content


def text_to_list(data: str, max_tokens: int = 2048, model: str = "gpt-3.5-turbo"):
   """Transform the output text returned from the LLM model (i.e. the relationships) into a list of tuples corresponding to the relatonships.
   Note: This function uses an LLM to convert the data into a Python list. Alternatively, a function using regular expressions and string 
   operations can be used, but the input data is a string returned by an LLM, so its structure might not be consistent"""

   msg_list = f"""Convert the list of relationships below into a list of tuples. Each tuple should have 3 elements of type string. Only output a Python list.\n\n\"\"\"{data}\"\"\""""

   messages=[
      {"role": "system", "content": """Output a Python list."""},
      {"role": "user", "content": msg_list}
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
