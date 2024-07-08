from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
import PyPDF2
from pypdf import PdfReader
import io
import requests
from .generativeAi import *
from api.utils import db
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse


@api_view(['GET'])
def Home(request):
    return Response("Welcome, to Findonic AI!")


"""
This is a POST call that uploads the data to mongoDB
Along with that it also generates a summary of the data and 
created the embeddings of the summary and puts it to the server
"""
@api_view(['POST'])
def Upload_Data_To_Mongo(request): 
    
    message = ''
    users = db['Users']

    try:
        _id = users.insert_one(request.data)
    except Exception as error:
        print(error)
        return HttpResponse("Could not add the User Data. ", error)
    else:
        message += 'Added the User Data. '


    if request.FILES['file']:
        
        pdfFileObj = request.FILES['file'].read() 
        reader = PdfReader(io.BytesIO(pdfFileObj))

        resume = ""
        for page in reader.pages:
            resume += page.extract_text() + ""
        
        summary = Generate_Summary_From_Resume_PDF(text)
        embedding = generateEmbeddingOpenAI(summary)

        try:
            doc = users.find_one(_id)
            doc['resume_summary'] = summary
            dock['resume_embedding'] = embedding
            users.replace_one({'_id': doc['_id']}, doc)
        except Exception as error:
            message += "Unable to add the summary or the embedding"
            return HttpResponse(message, error)
        else:
            message += "Added the resume summart and the embedding."
            return HttpResponse(message, error)
    else:
        message += 'No Resume Uploaded.'
        return HttpResponse(message)


@api_view(['GET'])
def Generate_Questions_On_Resume(request): 
    user_id = request.data['_id']

    #get the text from the text-file
    summary = Get_Text_From_Resume(request)

    questions = Generate_Questions_From_Resume(summary)

    return JsonResponse(questions)
    
def Get_Text_From_Resume(request):
    return ""

@api_view(['POST'])
def Get_Name_Email_From_Resume(request):
    url = request.data['url']

    response = requests.get(url)
    f = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(f)
    pages = reader.pages
    # get all pages data
    text = "".join([page.extract_text() for page in pages])

    response_data = {}
    response_data['name'] = Generate_Name_From_Resume(text)
    response_data['email'] = Generate_Email_From_Resume(text)
    
    return JsonResponse(response_data)

@api_view(['POST'])
def Get_Summary_Questions_From_Resume(request):
    url = request.data['url']

    response = requests.get(url)
    f = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(f)
    pages = reader.pages
    # get all pages data
    text = "".join([page.extract_text() for page in pages])

    response_data = {}
    response_data['questions'] = Generate_Questions_From_Resume(text)
    response_data['summary'] = Generate_Summary_From_Resume_PDF(text)
    
    return JsonResponse(response_data)

@api_view(['POST'])
def Get_Question_For_The_AI_Interviewer(request):
    transcript = request.data

    response_data = {}
    response_data['answer'] = Generate_Question_For_The_AI_Interviewer(transcript)

    return JsonResponse(response_data)