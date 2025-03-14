import requests
import json
import os
from crewai_tools import ScrapeWebsiteTool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
import os
from cosine_similarity import find_similarity
from content_loading import get_headline,get_main_info_from_user_content
load_dotenv()

gemini_api_key = os.getenv("GEMINI")
# print(gemini_api_key)


llm_summarise = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=f"{gemini_api_key}"
)
# print(llm_summarise.invoke("hi").content)

# https://rapidapi.com/bfd-id/api/google-news13/playground/apiendpoint_d0fcac20-4d75-4d96-ba2c-7733c9fab8b1
def fetch_google_news(query, num_results=5, language="en-US"):
    url = "https://google-search72.p.rapidapi.com/search"
    querystring = {"q": query, "lr": language, "num": str(num_results)}
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY", 
        "9ccf2b0a2emshfbc2441c39df50bp170e75jsnef1081d76d1f"),
        # "2434174db5mshfd0b322ede0eecfp147051jsn9c2a4f63a4b4"),
        "x-rapidapi-host": "google-search72.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        response_data = response.json()
        if "items" in response_data and response_data["items"]:
            return response_data
        else:
            return "No response found for the given query."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def print_response_google_news(response):
    if response['status'] == 'success' and 'items' in response:
        for index, item in enumerate(response['items'], start=1):
            print(f"Item {index}:")
            print(f"Title: {item['title']}")
            print(f"Snippet: {item['snippet']}")
            print(f"Link: {item['link']}")
            print(f"Display Link: {item['displayLink']}\n")
    else:
        print("No response found.")

# fetch_google_news('hinjewadi crahs')

def create_summary_llm_fetch_google_news(link):
    # print(link + ":")
    tool = ScrapeWebsiteTool(website_url=link)
    text = tool.run()
    prompt = text
    messages = [
        (
            "system",
            "i will give u a story summarise it. Try to include all major points like time date, number of people, hteir gender age,place where it happended etc.",
        ),
        ("human", f"{prompt}"),
    ]
    answer = llm_summarise.invoke(messages).content
    return answer,text

def generate_summary_dictionary_llm_fetch_google_news(user_input, headline):
    # Convert CrewAI output to string if needed
    if hasattr(user_input, 'raw_output'):
        user_input = str(user_input.raw_output)
    elif not isinstance(user_input, str):
        user_input = str(user_input)

    headline = get_headline(user_input)

    print(headline)
    response = fetch_google_news(headline)
    results = []
    print(response)
    print(headline)

    if response['status'] == 'success' and 'items' in response:
        for index, item in enumerate(response['items'], start=1):
            sum_news, description = create_summary_llm_fetch_google_news(item['link'])
            print(sum_news)
            print(user_input)
            similarity = find_similarity(sum_news, user_input)
            result = {
                'Title': item['title'],
                'Link': item['link'],
                'Description': description,
                'Summary': sum_news,
                'Similarity': similarity
            }
            results.append(result)

    else:
        print("No response found.")

    return results

# # # print(generate_summary_dictionary_llm_fetch_google_news(fetch_google_news("Hnjewadi crash")))
# user_input = """Two girl students on a two-wheeler died after they came under a cement mixer truck that overturned on them in Hinjewadi on Friday evening.Police identified the deceased students as Pranjali Mahesh Yadav (21) and Ashlesha Narendra Gawande (22), both residing at an apartment in Mulshi taluka of Pune district. Police said Pranjali was a native of Tembhurni in Solapur and Ashlesha hails from Amravati district. Both were final year Bachelor of Computer Applications (BCA) students at a private college in Pune.Police said a speeding cement mixer truck on the Hinjewadi Maan road lost control and overturned at the Vadjai Nagar corner around 5 pm.The truck overturned on the two-wheeler that was taking a turn at the corner. The impact was such that two girl students on the two-wheeler were crushed under the truck."""
# headline = ""
# dict = generate_summary_dictionary_llm_fetch_google_news(user_input,headline)
# print(dict)