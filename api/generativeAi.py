import openai
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from .utils import *
import pymongo
from bson import ObjectId


# Common variables
client = pymongo.MongoClient("mongodb+srv://AiInterviewer:O7ixij8bmyKCOBPa@cluster0.yfqpbv6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
userCollection = client.aidev.users
transcriptCollection = client.aidev.userTranscript
questionaireCollection = client.aidev.questionnaires


# Helper Methods
"""
This method takes the data from the resume and 
generates a summary of the resume based on the prompt
Returns the summary of the resume
"""
def Generate_Summary_From_Resume_PDF(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Summary())
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
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Questions())
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

"""
This method returns the name of the candidate 
that he has provided in the resume
"""
def Generate_Name_From_Resume(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Candidate_Name())
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

"""
This method returns the email of the candidate 
that he has provided in the resume
"""
def Generate_Email_From_Resume(resume):
    prompt_template = ChatPromptTemplate.from_template(Prompt_Template_For_Resume_Candidate_Email())
    prompt = prompt_template.format(context=resume)

    model = ChatOpenAI(openai_api_key=API_KEY_OPENAI)
    response_text = model.predict(prompt)

    return response_text

def Generate_Question_For_The_AI_Interviewer(transcript):

    if transcript['type'] == 'userAction' and transcript['data'] == 'STARTED':
        AIInterviewer_Helper_Start(transcript)
        
        # Returning Nothing, because in this case we are just storing/initializing the data
        return ""
    elif transcript['type'] == 'userAction' and transcript['data'] == 'ENDED':
        # Should never come here
        print('Ended Block')
    else:
        return AIInterviewer_Helper_GenerateNextQuestion(transcript)
    
def AIInterviewer_Helper_Start(transcript):
    userId = ObjectId(transcript['userId'])

    # transcript Id Generation
    user_transcript_id = Get_Or_Generate_TranscriptId_In_Users(userId)
    
    # Create the starting transcript based on the questions
    full_transcript = Create_New_Transcript(userId)

    # Insertion / Creation of the transcript document
    Get_Or_Generate_User_Transcript(userId, user_transcript_id, full_transcript)

"""
Created the transcript based on the questions generated
"""
def Create_New_Transcript(userId):
    # Query the document by ID
    userDocument = userCollection.find_one({"_id": userId})

    # Get the questionnaire document Id
    questionnaireId = userDocument['questionnaire']

    # Query the Questionnaire document
    questionnaireDocument = questionaireCollection.find_one({"_id": questionnaireId})

    # Get the questions to configure the initial transcript
    questions = questionnaireDocument['questions']

    # Build the full_transcript content dynamically
    full_transcript_content = (
        "You are an AI Interviewer and you will ask questions given to you one by one. "
        f"These are the questions: {questions} "
        "Please also ask follow up questions, if there is a need and make it more natural. After the user has answered these questions, "
        "you can say thank you for joining the call and have a good rest of your day. Say thank you in your own way"
    )

    # Define the full transcript
    full_transcript = [
        {
            "role": "system",
            "content": full_transcript_content
        }
    ]

    full_transcript.append({"role":"assistant", "content": "Hello, My name is Alex and I will be your AI Interviewer for today. Are you ready to get things started?"})

    return full_transcript


"""
This method gets or generates the transcript Id in the Users table
"""
def Get_Or_Generate_TranscriptId_In_Users(userId):
    # Query the document by ID
    userDocument = userCollection.find_one({"_id": userId})

    #region Get/Generate Transcript Id

    # getting the transcript Id from the User table if it exists or generates a new one
    # if it does not exist
    user_transcript_id = ''

    # Check if the key "userTranscript" exists in the document
    if userDocument:
        user_transcript_id = userDocument.get("userTranscript")
        if not user_transcript_id:
            user_transcript_id = ObjectId()
            userCollection.update_one(
                {"_id": userId},
                {"$set": {"userTranscript": user_transcript_id}}
            )

    return user_transcript_id

"""
This method generates or adds the new transcript for the transcript 
document in the UserTranscript table
"""
def Get_Or_Generate_User_Transcript(userId, user_transcript_id, full_transcript):
    transcriptDocument = transcriptCollection.find_one({"_id": user_transcript_id})

    if not transcriptDocument:
        newTranscriptDocument = {
            "_id": user_transcript_id,
            "userId": userId,
            'transcript': [full_transcript]
        }
        transcriptCollection.insert_one(newTranscriptDocument)
    else:
        transcriptCollection.update_one(
            {"_id": user_transcript_id},
            {"$push": {"transcript": full_transcript}}
        )
def AIInterviewer_Helper_GenerateNextQuestion(transcript):
    userId = ObjectId(transcript['userId'])
    
    # Query the document by ID
    userDocument = userCollection.find_one({"_id": userId})

    # Get the trascript Id
    user_transcript_id = userDocument.get("userTranscript")

    # Get the data spoken by the user
    userSpeech = transcript['data']

    # Get the document from the UserTranscript table
    transcriptDocument = transcriptCollection.find_one({"_id": user_transcript_id})

    allTranscripts = transcriptDocument['transcript']

    # Get the last transcript because the user interview will be going on that transcript
    last_full_transcript = allTranscripts[-1]

    # update the transcript
    last_full_transcript.append({"role":"user", "content": userSpeech})

    # generate a response from the LLM based on this transcript
    openai_client = openai.OpenAI(api_key = API_KEY_OPENAI)
    
    response = openai_client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = last_full_transcript
    )

    # append the generated response
    ai_response = response.choices[0].message.content
    last_full_transcript.append({"role":"assistant", "content": ai_response})

    # Replace the last full_transcript in the additionalList
    allTranscripts[-1] = last_full_transcript

    print(last_full_transcript)
    
    # update the document
    transcriptCollection.update_one(
            {"_id": user_transcript_id},
            {"$set": {"transcript": allTranscripts}}
        )
    
    # return the ai response
    return ai_response