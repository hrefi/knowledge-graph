from openai import OpenAI
# import spacy
import json
import tiktoken

client = OpenAI()

# Use GPT!
# Prompt engineering

def extractEntities(data: str):
   pass




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




# TODO: Use LLM for the two funxtions below

def textToList(text: str):
   """Transform the output text returned from the LLM model (i.e. the relationships)
   into a list of tuples corresponding to the relatonships"""
   # Split the string into groups based on the comma
   groups = text.split(',')
   # Process each group (split by the dash and trim whitespaces) to create triplets
   relationships = [tuple(map(str.strip, group.split('-'))) for group in groups]

   return relationships

def textToJson(text: str):
   """Transform the output text returned from the LLM model (i.e. the relationships) into a JSON for output"""
   jsonObjects = []
   # Split the string into groups based on the comma
   groups = text.split(',')
   for relationship in groups:
      try:
         src, rellationship, tgt = map(str.strip, relationship.split('-'))
         jsonObjects.append({"source": src, "relation": rellationship, "target": tgt})
      except:
         print(map(str.strip, relationship.split('-')))
         raise Exception('Relationships should have a format "entity 1 - relation - entity 2"')
   
   return json.dumps(jsonObjects, indent=4)




"""SpaCy code"""

# nlp = spacy.load("en_core_web_sm")  # Load a suitable model

# # all_text = " ".join(snippets)  # Combine snippets

# def process_with_nlp(text):
#    doc = nlp(text)
#    entities = {ent.text: ent.label_ for ent in doc.ents} 
#    relationships = []

#    for token in doc:
#       for child in token.children:
#          relationships.append((token.text, child.text, child.dep_))
         
#    # for sentence in doc.sents:
#    #    root = list(sentence.roots)[0]  # Get the sentence root
#    #    for dep in sentence.deps:
#    #       if dep[1] in ["subj", "obj"]:  # Consider subject/object dependencies
#    #          relationships.append((dep[0].text, root.text, dep[1]))

#    return entities, relationships 


# # To extract relationships, you need to process your text with the NLP model, find entities, and 
# # then determine the verbs or prepositions connecting these entities, which often indicate the relationships.

# def extract_relationships(text):
#    doc = nlp(text)
#    relationships = []

#    for ent in doc.ents:
#       # Initialize variables to store the closest verb and subject/object to the entity
#       subj = None
#       verb = None
#       obj = None
      
#       # Check if the entity's root head is a verb; if so, it's likely part of a relationship
#       if ent.root.head.pos_ == "VERB":
#          verb = ent.root.head
#          # Search for subject connected to the verb
#          for child in verb.children:
#             if child.dep_ in ["nsubj", "nsubjpass"]:  # subject or passive subject
#                subj = child
#             elif child.dep_ in ["dobj", "pobj", "obj"]:  # direct/indirect object
#                obj = child
                  
#          # If a subject or object and a verb are found, record the relationship
#          if subj and obj:
#             relationships.append((subj, verb, obj))
#          elif verb:  # If only a verb is found, include the entity and verb
#             relationships.append((ent, verb))
               
#    return relationships