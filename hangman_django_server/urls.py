from django.urls import path
from .views import *
urlpatterns = [
    path('hangman/api/v1/users/login/', LoginAPIview.as_view()),
    path('hangman/api/v1/users/logout/', LogoutAPIview.as_view()),

    path('hangman/api/v1/users/', UsersAPIview.as_view()),#create a user / get all users
    path('hangman/api/v1/users/<str:usn>/', UserAPIview.as_view()),#update a user / delete a user / confirm user existance

    path('hangman/api/v1/tables/', TablesAPIview.as_view()), #Get list of all word tables / Add new table
    path('hangman/api/v1/tables/<str:tablename>/', TableAPIview.as_view()), #Remove table and all words associated
    path('hangman/api/v1/tables/<str:tablename>/words/', WordAPIview.as_view()), #Get random word / Add word / delete word 
    path('hangman/api/v1/tables/<str:tablename>/words/readfile/', AddFileDataAPIview.as_view()), #Read a file to a specific table

    path('hangman/api/v1/history/save/<str:usn>/', SaveHistoryAPIview.as_view()),#add to history
    path('hangman/api/v1/history/recent/<str:usn>/', RecentHistoryAPIview.as_view()), #Get users most recent games
    path('hangman/api/v1/history/leaderboard/', Top10APIview.as_view()), #Get highscores
    path('hangman/api/v1/history/leaderboard/<str:usn>/', UserTop10APIview.as_view()) #Get user higscores
]