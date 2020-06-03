#Rest framework imports
from django.http import JsonResponse, HttpResponse
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

#Authentication
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
#from rest_framework.permissions import IsAuthenticated

#Error handling import - hasn't worked so far
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

#Own imports
from .serializers import *
from .models import *
from .custom_errors import *

#Token exception import
#from django.views.decorators.csrf import csrf_exempt

#Decoding encoding
import base64
from hashlib import sha256
from random import randint, random, choice
from datetime import datetime, timedelta, tzinfo
import pytz



#/users/
class UsersAPIview(APIView):
    def get(self, request):
        musers = Users.objects.all()
        serializer = UserGetSerializer(musers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        mydata = request.data
        dict_idx = self.__validate_request(mydata)
        if dict_idx:
            err_dict = {1:{'Error':"Incorrect amount of attributes, 'username' and 'password' required"},
                        2:{'Error':'Request must have password and username'}, 
                        3:{'Error':'Password and username must have length of atleast 5'}}
            return Response(err_dict[dict_idx], status=status.HTTP_400_BAD_REQUEST) 
        mydata['password']=sha256(mydata['password'].encode('utf-8')).hexdigest()
        serializer = UserPostSerializer(data=mydata)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def __validate_request(self, request_data):
        data_keys = request_data.keys()
        if len(data_keys)!=2:
            return 1

        if not 'password' in data_keys and not 'username' in data_keys:
            return 2

        if len(request_data['password'])<5 or len(request_data['username'])<5:
            return 3

        return


#/users/<str:usn>/
class UserAPIview(APIView):
    def get(self, request, usn):
        user = self.get_object(usn)
        if user:
            return Response({'Exists':True, 'username':user.username}, status=status.HTTP_200_OK)
        return self.doesnt_exist()

    def delete(self, request, usn):
        try:
            basic_auth = request.META['HTTP_AUTHORIZATION']
        except:
            return Response({'Error': 'Missing Authentication'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status=status.HTTP_400_BAD_REQUEST)
                
        authorization = Authorize()
        basic_validation = authorization.validate_basicauth(basic_auth)
        token_validation = authorization.validate_token(token)
        if basic_validation and token_validation:
            user = self.get_object(usn)
            if not user:
                return self.doesnt_exist()
            if user.username == authorization.token.user and user.username == authorization.username:
                user.delete()
                authorization.deactivate_token()
                return Response({'Message':'User successfully deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'Error':'User credentials invalid'})
        else:
            return authorization.get_response()

    def put(self, request, usn):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            user = self.get_object(usn)
            if not user:
                return self.doesnt_exist()
            errors = self.validate_edit(request.data)
            if errors:
                err_dict = {1: {'Error': 'Invalid amount of attributes, should only contain password and token'},
                            2: {'Error': 'Password missing from attributes'},
                            3: {'Error': 'Password must be of length atleast 5'}}
                return Response(err_dict[errors], status=status.HTTP_400_BAD_REQUEST)

            password = request.data["password"]
            password = sha256(password.encode('utf-8')).hexdigest()
            serializer = UserPutSerializer(user, data={'password':password})
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Successfully updated password'}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return authorization.get_response()

    def get_object(self, usn):
        try:
            user = Users.objects.get(username=usn) #can user __exact, leq, geq... etc
        except Users.DoesNotExist:
            return None
        return user

    def doesnt_exist(self):
        data = {'Error': 'User does not exist'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    def validate_edit(self, request_data):
        data_keys = request_data.keys()
        if len(data_keys)!=2:
            return 1

        if not 'password' in data_keys:
            return 2

        if len(request_data['password'])<5:
            return 3

        return


#/history/save/<str:usn>/
class SaveHistoryAPIview(APIView):
    def post(self, request, usn):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            score = request.data['score']
            user = request.data['user']
        except:
            return Response({'Error':'Missing attribute user or score'}, status = status.HTTP_400_BAD_REQUEST)
        mydata = {'user':user, 'score': score}
        
        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation and usn == user:
            serializer = SaveUserHistorySerializer(data=mydata)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        return authorization.get_response()


#/recent/<str:usn>/
class RecentHistoryAPIview(APIView):
    def get(self, request, usn):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            history = History.objects.filter(user=usn).order_by('-date')[:10]
            serializer = GetUserHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
       
        return authorization.get_response()


#/history/leaderboard/
class Top10APIview(APIView):
    def get(self, request):
        top_10 = History.objects.all().order_by('-score')[:10]
        serializer = GetUserHistorySerializer(top_10, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#/history/leaderboard/<str:usn>/
class UserTop10APIview(APIView):
    def get(self, request, usn):
        try:
            token = request.data['token']
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            top_10 = History.objects.filter(user=usn).order_by('-score')[:10]
            serializer = GetUserHistorySerializer(top_10, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return authorization.get_response()


#/tables/
class TablesAPIview(APIView):
    def get(self, request):
        tables = Tablenames.objects.all()
        serializer = TableSerializer(tables, many=True)

        mydata = serializer.data
        for data in mydata:
            table = data['tname']
            word_count = Hangman.objects.filter(tablename=table).count()
            data['wordcount']=word_count

        return Response(mydata, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usn = request.data['username']
        except:
            return Response({'Error': 'Username missing from request body'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tablename = request.data['tablename']
        except:
            return Response({'Error': 'Tablename missing from request body'}, status=status.HTTP_400_BAD_REQUEST)

        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            serializer = TableSerializer(data={'byuser':usn, 'tname':tablename})
            if serializer.is_valid():
                serializer.save()
                return Response({'Message':'Successfully added table named: '+tablename}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return authorization.get_response()


#/tables/<str:tablename>/
class TableAPIview(APIView):
    def delete(self, request, tablename):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            usn = request.data['username']
        except:
            return Response({'Error': 'Username missing from request body'}, status=status.HTTP_400_BAD_REQUEST)

        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            table_obj = self.get_table(tablename, usn)
            if not table_obj:
                return Response({'Error': 'Table not found'}, status=status.HTTP_404_NOT_FOUND)
            table_obj.delete()
            return Response({'Message':'Table successfully deleted'}, status=status.HTTP_200_OK)
        return authorization.get_response()

    def get_table(self, tablename:str, usn:str)->object:
        try:
            table_obj = Tablenames.objects.get(tname=tablename, byuser=usn)
        except Tablenames.DoesNotExist:
            return None
        return table_obj


#/tables/<str:tablename>/words/readfile/
class AddFileDataAPIview(APIView):
    def post(self, request, tablename):
        try:
            file_object = request.FILES['file']
        except:
            return Response({'Error':'Error retrieving file from request body'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usn = request.data['username']
        except:
            return Response({'Error':'Username missing from request body'}, status=status.HTTP_400_BAD_REQUEST)

        usn = usn.strip('"')
        usn = usn.strip("\\")
        usn = usn.strip(" ")
        if file_object.size>5500 and usn!="Default":
            return Response({'Error':'File too large 5KB max'}, status=status.HTTP_400_BAD_REQUEST) 
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        table_user = self.check_tablename(tablename)
        if not table_user:
            return Response({'Error':'Table does not exist'}, status=status.HTTP_404_NOT_FOUND)
        file_user= usn
        token = token.strip('"')
        token = token.strip("\\")
        if table_user!=usn:
            return Response({'Error':'User credentials do not match table creator', 'table_user':table_user, 'usn':usn, 
                            'fileuser': file_user, 'token': token}, status=status.HTTP_401_UNAUTHORIZED)

        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            data = []
            words = []
            for line in file_object:
                line = line.decode('utf-8')
                line = line.strip('\n')
                line = line.strip(' ')
                if line!="" and line!=None and line!="\n":
                    if line not in words:
                        words.append(line)
                        data.append({'word':line, 'tablename':tablename})
                
            
            serializer = WordSerializer(data=data, many=True)
            if serializer.is_valid():
                try:
                    serializer.save()
                except IntegrityError:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                return Response({'Message':'Successfully added '+str(len(words))+' words.'}, status=status.HTTP_201_CREATED)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return authorization.get_response()

    def check_tablename(self, tablename:str)->str:
        try:
            table_obj = Tablenames.objects.get(tname = tablename)
        except Tablenames.DoesNotExist:
            return None
        return table_obj.byuser


#/tables/<str:tablename>/words/
class WordAPIview(APIView):
    def get(self, request, tablename):
        try:
            word = choice(Hangman.objects.filter(tablename=tablename))
        except:
            return Response({'Error':'Empty/Invalid Table'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'word': word.word}, status=status.HTTP_200_OK)

    def post(self, request, tablename):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            usn = request.data['username']
        except:
            return Response({'Error': "Attribute 'username' missing from request body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            word = request.data['word']
        except:
            return Response({'Error': "Attribute 'word' missing from request body"}, status=status.HTTP_400_BAD_REQUEST)

        table_user = self.check_tablename(tablename)
        if not table_user:
            return Response({'Error':'Table does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if table_user!=usn:
            return Response({'Error':'User credentials do not match table creator'}, status=status.HTTP_401_UNAUTHORIZED)
        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            serializer = WordSerializer(data={'word': word, 'tablename':tablename})
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Successfully added word: '+word}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return authorization.get_response()
    
    def delete(self, request, tablename):
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            usn = request.data['username']
        except:
            return Response({'Error': "Attribute 'username' missing from request body"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            word = request.data['word']
        except:
            return Response({'Error': "Attribute 'word' missing from request body"}, status=status.HTTP_400_BAD_REQUEST)

        table_user = self.check_tablename(tablename)
        if not table_user:
            return Response({'Error':'Table does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if table_user!=usn:
            return Response({'Error':'User credentials do not match table creator'}, status=status.HTTP_401_UNAUTHORIZED)
        authorization = Authorize()
        token_validation = authorization.validate_token_request(token, usn)
        if token_validation:
            word_obj = self.get_word(tablename, word)
            if not word_obj:
                return Response({'Error':'Word not found'}, status=status.HTTP_404_NOT_FOUND)
            word_obj.delete()
            return Response({'Message': 'Successfully deleted word: '+word}, status=status.HTTP_200_OK)
        return authorization.get_response()

    def check_tablename(self, tablename:str)->bool:
        try:
            table_obj = Tablenames.objects.get(tname = tablename)
        except Tablenames.DoesNotExist:
            return None
        return table_obj.byuser

    def get_word(self, tablename:str, word:str):
        try:
            word_obj = Hangman.objects.get(word=word, tablename=tablename)
        except Hangman.DoesNotExist:
            return None
        return word_obj


#/login/
class LoginAPIview(APIView):
    def get(self, request):
        authorization = Authorize()
        try:
            basic_auth = request.META['HTTP_AUTHORIZATION']
        except:
            return Response({'Error': 'Missing Authentication'}, status = status.HTTP_400_BAD_REQUEST)
        #return Response(basic_auth) #debug
        basic_validation = authorization.validate_basicauth(basic_auth)
        #return Response(basic_validation) #debug
        if basic_validation:
            no_existing_tokens = authorization.validate_for_existing_token()
            #return Response(no_existing_tokens) #debug
            if no_existing_tokens:
                token = authorization.create_token()
                return Response({'token':token, 'active_time': str(authorization.TOKEN_TIMER)+" hours"}, status=status.HTTP_200_OK)
        return authorization.get_response()


#/logout/
class LogoutAPIview(APIView):
    def get(self, request):
        try:
            basic_auth = request.META['HTTP_AUTHORIZATION']
        except:
            return Response({'Error': 'Missing Authentication'}, status = status.HTTP_400_BAD_REQUEST)
        try:
            token = request.data["token"]
        except:
            return Response({'Error':'Missing token'}, status = status.HTTP_400_BAD_REQUEST)
                
        authorization = Authorize()
        basic_validation = authorization.validate_basicauth(basic_auth)
        token_validation = authorization.validate_token(token, True)
        if basic_validation and token_validation:
            try:
                authorization.deactivate_token(token)
                return Response({'Message': 'Successfully logged out'}, status = status.HTTP_200_OK)
            except:
                return Response({'Error':'Error saving updated token'}, status = status.HTTP_400_BAD_REQUEST)

        auth_response = authorization.get_response()
        return auth_response


#Makes the authorization
class Authorize:
    def __init__(self):
        self.TOKEN_TIMER = 2 #hours
        self.validated_basic = False
        self.validated_token = False
        self.username = None
        self.password = None
        self.token    = None

        self.simple_request_validation = False
        self.invalid_basicauth = False
        self.user_doesnt_exist = False
        self.token_doesnt_exist = False
        self.token_inactive = False
        self.other_existing_tokens = False
        
    def validate_token(self, request_token:str, logout:bool=False)->bool:
        """Must validate basicauth first. Takes token as string (should be sent via request body) and validates it against database
        \nIf valid -> True, sets class variable token
        \nIf invalid -> False"""
        if self.invalid_basicauth or not self.validate_basicauth:
            return False

        self.validated_token = True
        try:
            token_obj = AuthorizationToken.objects.get(token=request_token, active=True, user=self.username)
        except AuthorizationToken.DoesNotExist:
            self.token_doesnt_exist = True
            return False

        if not logout:
            isactive = self.validate_activity(token_obj)
            return isactive

        self.token = token_obj.token
        return True

    def validate_activity(self, token_obj:object)->bool:
        """Validates if a token is active or inactive. Is called internally from validate_token method."""
        token_timestamp = token_obj.date + timedelta(hours=self.TOKEN_TIMER)
        curr_timestamp = datetime.now().replace(tzinfo=pytz.UTC)
        if curr_timestamp>token_timestamp:
            self.token_inactive = True
            token_serializer = UpdateTokenSerializer(token_obj, data={'active': False})
            if token_serializer.is_valid(raise_exception=True):
                token_serializer.save()
            return False

        self.token = token_obj
        return True

    def validate_basicauth(self, basic_auth:str)->bool:
        """Takes basic authentication header as argument and validates the user information
        \nSend in with format: request.META['HTTP_AUTHORIZATION']
        \nIf valid -> True, sets class variables password and username
        \nIf invalid -> False"""
        self.validated_basic = True
        try:
            basic_auth = basic_auth.split(" ")[1]
            basic_auth = base64.b64decode(basic_auth).decode('UTF-8')
            user_pass = basic_auth.split(":")
        except:
            self.invalid_basicauth = True
            return False

        try:
            someuser = Users.objects.get(username=user_pass[0], password=sha256(user_pass[1].encode('utf-8')).hexdigest())
        except Users.DoesNotExist:
            self.user_doesnt_exist = True
            return False
        
        self.username = someuser.username
        self.password = someuser.password
        return True

    def validate_for_existing_token(self)->bool:
        """Must authenticate basic Auth before calling
        \nIf other tokens exists for user -> False, Sets class variable other_existing_tokens to True 
        \nIf no other token exist -> True"""
        #Updated functionality to get new token anytime requested instead of throwing error#
        if not self.validated_basic:
            raise BasicAuthNotValidated
        
        try:
            auth_tokens = AuthorizationToken.objects.filter(user=self.username, active=True)
        except AuthorizationToken.DoesNotExist:
            return True

        for token in auth_tokens:
            isactive = self.validate_activity(token)
            if isactive:
                token.active = False
                token.save()
                #self.other_existing_tokens = True
                #return False
        return True

    def validate_token_request(self, request_token:str, usn:str)->bool:
        """To validate a token without basic authentication
        \nIf valid -> True
        \nIf invalid ->False"""
        self.simple_request_validation = True
        try:
            token_obj = AuthorizationToken.objects.get(token=request_token, active=True, user=usn)
        except AuthorizationToken.DoesNotExist:
            self.token_doesnt_exist = True
            return False

        self.username = token_obj.user
        isactive = self.validate_activity(token_obj)
        return isactive

    def create_token(self)->str:
        """Creates a new token and saves to database
        Returns the token as string"""
        random_number = randint(2^8, 2^31)
        random_hash = hash(random_number)
        random_sha = sha256(str(random_hash).encode('utf-8')).hexdigest()
        dict_token = {'token':random_sha, 'user': self.username}
        serializer = CreateTokenSerializer(data=dict_token)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return random_sha

    def deactivate_token(self, my_token):
        """Validate token first to deactivate"""
        self.token_inactive = True
        token_object = AuthorizationToken.objects.get(token=my_token, active=True)
        token_serializer = UpdateTokenSerializer(token_object, data={'active': False})
        if token_serializer.is_valid(raise_exception=True):
            token_serializer.save()
        return

    def get_validation(self)->bool:
        """Returns the validation summary. 
        \nIf any of the validations haven't been made -> Raises IncompleteValidation
        \nIf both basicauth validation and token validation were successful -> True
        \nIn any other case -> False"""
        
        if not self.validated_basic or not self.validated_token:
            raise IncompleteValidation
        elif self.token_doesnt_exist or self.invalid_basicauth or self.token_inactive:
            return False

        return True

    def get_response(self)->object:
        """Returns a json http response according to authorization state"""
        if not self.validated_basic and not self.simple_request_validation:
            raise BasicAuthNotValidated

        elif self.other_existing_tokens:
            return Response({'Error':'A session is already in progress'}, status=status.HTTP_401_UNAUTHORIZED)

        elif self.invalid_basicauth:
            return Response({'Error':'Invalid authorization header'}, status=status.HTTP_401_UNAUTHORIZED)

        elif self.user_doesnt_exist:
            return Response({'Error':'Invalid user detected in authorization'}, status=status.HTTP_401_UNAUTHORIZED)

        elif not self.validated_token and not self.simple_request_validation:
            raise TokenNotValidated

        elif self.token_inactive:
            return Response({'Error': 'Token inactive'}, status=status.HTTP_401_UNAUTHORIZED)
    
        elif self.token_doesnt_exist:
            return Response({'Error': 'Token invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'Message':'Authorization successful'}, status=status.HTTP_200_OK)


