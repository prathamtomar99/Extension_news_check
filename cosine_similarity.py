import spacy

nlp = spacy.load("en_core_web_md")

def find_similarity(big_doc,small_doc):
    big_doc = nlp (big_doc)
    small_doc = nlp(small_doc)
    similarity_score = big_doc.similarity(small_doc)
    return similarity_score
    
# print(find_similarity("in Hinjewadi on Friday evening. police identified the deceased students as Pranjali Mahesh Yadav (21) and Ashlesha Narendra Gawande (22) police said a speeding cement mixer truck lost control and overturned on the two-wheeler around 5 pm - police say he was crushed under the truck.","Two Students Killed as Cement Mixer Overturns in Hinjewadi"))