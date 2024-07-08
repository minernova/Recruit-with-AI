from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('addUserData/', views.Upload_Data_To_Mongo, name="UploadDataToMongo"),
    path('getNameEmailResume/', views.Get_Name_Email_From_Resume, name="GetNameAndEmailFromResume"),
    path('getSummaryQuestionsResume/', views.Get_Summary_Questions_From_Resume, name="GetSummaryAndQuestionsFromResume"),
    path('getTranscriptAIInterview/', views.Get_Question_For_The_AI_Interviewer, name="GetQuestionForTheAIInterviewer"),
]