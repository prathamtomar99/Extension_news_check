import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
load_dotenv()
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
# from langchain import PromptTemplate, LLMChain
from langchain.chains import LLMChain

# print(src_key)
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

model1 = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer1 = T5Tokenizer.from_pretrained('t5-small')
model2 = RobertaForSequenceClassification.from_pretrained('roberta-large-mnli')
tokenizer2 = RobertaTokenizer.from_pretrained('roberta-large-mnli')

gemini_api_key = os.getenv("GEMINI")
# print(gemini_api_key)

def get_main_info_from_user_content(text):
    inputs = tokenizer1(text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = model1.generate(
        inputs['input_ids'],
        max_length=150,  # Control the max length of the summary
        num_beams=4,     # Use beam search for better results
        no_repeat_ngram_size=2,  # Avoid repeating phrases
        early_stopping=True
    )

    return tokenizer1.decode(summary_ids[0], skip_special_tokens=True)


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=f"{gemini_api_key}"
)

def get_headline(text):
    messages = [
        (
            "system",
            "Give me one proper breif headline/heading for the scene / content which includes major info about content",
        ),
        ("human", f"{text}"),
    ]
    return llm.invoke(messages).content

# Function to check if the claim is correct based on a large paragraph
def check_claim_with_large_paragraph(claim, large_paragraph):
    sentences = large_paragraph.split('.')

    for sentence in sentences:
        input_text = f"premise: {sentence.strip()} hypothesis: {claim.strip()}"
        inputs = tokenizer2(input_text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model2(**inputs)

        prediction = torch.argmax(outputs.logits, dim=-1).item()
        if prediction == 2:
            return "Claim is correct."
    return "Claim is incorrect."


# res = get_main_info_from_user_content("""Two girl students on a two-wheeler died after they came under a cement mixer truck that overturned on them in Hinjewadi on Friday evening.
# Police identified the deceased students as Pranjali Mahesh Yadav (21) and Ashlesha Narendra Gawande (22), both residing at an apartment in Mulshi taluka of Pune district.
# Police said Pranjali was a native of Tembhurni in Solapur and Ashlesha hails from Amravati district. Both were final year Bachelor of Computer Applications (BCA) students at a private college in Pune.
# Police said a speeding cement mixer truck on the Hinjewadi  Maan road lost control and overturned at the Vadjai Nagar corner around 5 pm.
# The truck overturned on the two-wheeler that was taking a turn at the corner. The impact was such that two girl students on the two-wheeler were crushed under the truck.""")
# res2 = get_headline("""Two girl students on a two-wheeler died after they came under a cement mixer truck that overturned on them in Hinjewadi on Friday evening.
# Police identified the deceased students as Pranjali Mahesh Yadav (21) and Ashlesha Narendra Gawande (22), both residing at an apartment in Mulshi taluka of Pune district.
# Police said Pranjali was a native of Tembhurni in Solapur and Ashlesha hails from Amravati district. Both were final year Bachelor of Computer Applications (BCA) students at a private college in Pune.
# Police said a speeding cement mixer truck on the Hinjewadi. Maan road lost control and overturned at the Vadjai Nagar corner around 5 pm.
# The truck overturned on the two-wheeler that was taking a turn at the corner. The impact was such that two girl students on the two-wheeler were crushed under the truck.""")

# claim = "They were 2 girls who died in the incident"
# large_paragraph = res


# print(res)
# print(res2)
# result = check_claim_with_large_paragraph("Two Students Killed as Cement Mixer Overturns in Hinjewadi", large_paragraph)
# print(result)