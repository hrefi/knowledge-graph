import spacy

# Preprocess Text - remove irrelevant sections, such as navigation menus or footers, using heuristics or HTML structure analysis

# Use GPT as well as spaCy !

# Entity Extraction
# Relationship Extraction
# Refining Results: Relationship Filtering, Entity Disambiguation


nlp = spacy.load("en_core_web_sm")  # Load a suitable model

# all_text = " ".join(snippets)  # Combine snippets

def process_with_nlp(text):
   doc = nlp(text)
   entities = {ent.text: ent.label_ for ent in doc.ents} 
   relationships = []

   for token in doc:
      for child in token.children:
         relationships.append((token.text, child.text, child.dep_))
         
   # for sentence in doc.sents:
   #    root = list(sentence.roots)[0]  # Get the sentence root
   #    for dep in sentence.deps:
   #       if dep[1] in ["subj", "obj"]:  # Consider subject/object dependencies
   #          relationships.append((dep[0].text, root.text, dep[1]))

   return entities, relationships 


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