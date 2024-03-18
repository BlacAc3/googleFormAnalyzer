from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as cooking
from django.conf import settings

###############AI import##################
import google.generativeai as genai
##########################################



def index(request, **kwargs):
    return render(request, "solution/index.html")

#########-- htmx --##########
def htmx_test(request):
    print("htmx works!!")
    return 

##########-- Rendering to index the AI output --##########
def makesoup(request):
    url = request.POST.get("url")
    question_and_answer = get_questions_and_answer(url)
    return render(request, "solution/index.html",{
        "boxes":question_and_answer,
    })

##########-- Getting the string only from the list --##########
def improve_list(list :list)-> list:
    new_list = []
    for item in list:
        if item.string is None:
            continue
        new_list.append(item.string)
    return new_list


##########-- Scraping the Web --##########
def get_questions_and_answer(url :str) ->list:
    # url = "https://docs.google.com/forms/d/e/1FAIpQLSfIpvY6Cmzzkosn7am8x3_jRG7QKR0PsQjpUdeb7OeQxqlB-Q/viewform?usp=sf_link"
    response = requests.get(url)
    soup = cooking(response.content, "html.parser")
    #Getting containers of question and it's options
    containers = soup.findAll(class_="geS5n")
    #Creating empty list of containers with questions and answers
    new_containers=[]
    index: int = 0
    for box in containers:
    ##### Scraping questions and answers from each individual container######
        new_box =[]
        index= index + 1
        new_box.append(index)
        ###### Scraping question #####
        question = box.find(class_="M7eMe")
        ###### Adding question to container 1 #########
        new_box.append(question.text)
        ###### Scraping answers #######
        answers = box.findAll(class_="aDTYNe")
        ###### Asking AI #######
        try:
            if not answers :
                ###### if the answer box doesnt have options simply ask the question ######
                clean_answers = askAI(question.text)
            else:
                ###### prompt AI with question and answer options ######
                new_ans= [answer.string for answer in answers]
                clean_answers = askAI(f"This is the {question}, these are the options: {new_ans}, return the correct option text(only, with the number before it(if its the first option, 1 comes before the text)) to the question, if you can't understand then just randomly pick an option")
            ###### Adding AI answers to container ######
            new_box.append(clean_answers)
            ###### Appending container to list of containers ######
            new_containers.append(new_box)
        except:
            new_box.append("Sorry, as an AI I cant answer this!!")
    return new_containers


######## Asking AI ########
def askAI(text: str):
    GOOGLE_API_KEY=settings.API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    print(markdown_to_text(response.text))
    return markdown_to_text(response.text)


######## Turning markdown to text ########
def markdown_to_text(markdown_text):
    lines = markdown_text.splitlines()  # Split into lines
    text = ""
    for line in lines:
        # Remove leading/trailing whitespace and asterisks/underscores for emphasis/strong
        stripped_line = line.strip(" *_*")
        # Remove bold formatting (may need adjustment based on markdown dialect)
        text += stripped_line.replace("**", "").replace("__", "") + "\n"
        # Remove headers (assumes headers use # symbols)
        text = text.lstrip("#")
    return text.strip()  # Remove trailing newline