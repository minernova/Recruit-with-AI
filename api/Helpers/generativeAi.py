import openai
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from api.Helpers import .utils


"""
This method takes the data from the resume and 
generates a summary of the resume based on the prompt
Returns the summary of the resume
"""
def Generate_Summary_From_Resume_PDF(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Summary)
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

"""
This method returns the prompt template that is used 
to generate the summary of the resume
"""
def Prompt_Template_For_Resume_Summary():
    PROMPT_TEMPLATE = """
        Can you provide a comprehensive summary of my resume, ensuring all details about my educational background, professional experience, projects, and skills are included? based on the below context :

        {context}

    """
    return PROMPT_TEMPLATE

"""
This method returns the prompt template that is used 
to generate the questions from the resume
"""
def Prompt_Template_For_Resume_Questions():
    PROMPT_TEMPLATE = """
        Generate 5 interview questions based on the provided resume data. Ensure that 4 questions are technical and related to the candidate's skills and experiences, while 1 question is more generic. Only generate the questions without a prior salutation or anything else. The resume is for a technical person.

        {context}

    """
    return PROMPT_TEMPLATE

"""
This method returns the prompt template that is used 
to generate the name from the resume
"""
def Prompt_Template_For_Resume_Candidate_Name():
    PROMPT_TEMPLATE = """
        Based on the given resume data, what is the name in this resume. just give the name and nothing more.

        {context}

    """
    return PROMPT_TEMPLATE

"""
This method returns the prompt template that is used 
to generate the email from the resume
"""
def Prompt_Template_For_Resume_Candidate_Email():
    PROMPT_TEMPLATE = """
        Based on the given resume data, what is the email in this resume. just give the name and nothing more.

        {context}

    """
    return PROMPT_TEMPLATE


"""
This method used OpenAI Embedding model
to generate the embedding of the given text.
Return a list of float with the embeddings
"""
def generateEmbeddingOpenAI(text: str) -> list[float]:
    openai_client = openai.OpenAI(api_key = API_KEY_OPENAI)
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002", 
        input=text
    )
    return response.data[0].embedding

"""
This method returns the questions generated 
based on the resume content
"""
def Generate_Questions_From_Resume(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Questions)
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

"""
This method returns the name of the candidate 
that he has provided in the resume
"""
def Generate_Name_From_Resume(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Candidate_Name)
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

"""
This method returns the email of the candidate 
that he has provided in the resume
"""
def Generate_Email_From_Resume(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Candidate_Email)
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

