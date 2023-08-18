from rest_framework import generics, permissions, views, status
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserLoginSerializer
from .models import Video
from .serializers import VideoSerializer, UserSerializer
from .video_stream import VideoStream
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from .forms import UserRegistrationForm, VideoCreationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated



import cv2
from threading import Thread
from django.http import StreamingHttpResponse
from .video_stream import VideoStream




def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Retrieve and store the authentication token
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key

            return JsonResponse({'message': 'Registration successful', 'token': token.key})
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Retrieve and store the authentication token
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key

            return JsonResponse({'message': 'Login successful', 'token': token.key})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def video_create(request):
    if request.method == 'POST':
        form = VideoCreationForm(request.POST)
        if form.is_valid():
            video = form.save()
            return redirect('video-list')
    else:
        form = VideoCreationForm()
    return render(request, 'video_create.html', {'form': form})


@login_required
def video_edit(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoCreationForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('video-list')
    else:
        form = VideoCreationForm(instance=video)
    return render(request, 'video_edit.html', {'form': form, 'video': video})

@login_required
def video_delete(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        return redirect('video-list')
    return render(request, 'video_delete.html', {'video': video})





class VideoStreamView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, video_id):
        try:
            video = Video.objects.get(pk=video_id)

            def generate_frames():
                video_stream = VideoStream(video.video_path)
                video_stream.start()

                while not video_stream.stopped:
                    frame = video_stream.frame
                    if frame is not None:
                        _, buffer = cv2.imencode('.jpg', frame)
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")

        except Video.DoesNotExist:
            return Response({'message': 'Video not found.'}, status=status.HTTP_404_NOT_FOUND)


# class VideoListView(generics.ListCreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(title__icontains=search_query)
#         return queryset
    


class VideoDetailView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'video_detail.html', {'video': video})



# API views
class VideoListAPI(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Video.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query))
        return queryset

class VideoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ... other methods ...

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





@api_view(['GET'])
def api_documentation(request):
    endpoints = {
        'User Authentication': {
            'Login': '/api/login/',
            'Logout': '/api/logout/',
            'Register User': '/api/register/',
        },
        'Videos': {
            'Get All Videos': '/api/videos/',
            'Create Video': '/api/videos/',
            'Get Video Details': '/api/videos/<id>/',
            'Update Video': '/api/videos/<id>/',
            'Delete Video': '/api/videos/<id>/',
        },
        'Video Streaming': {
            'Stream Video': '/api/videos/<id>/stream/',
        },
        'Search Videos': {
            'Search Videos': '/api/videos/?search=<search_query>',
        },
        # Add other endpoints as needed...
    
        # ... add more custom endpoints ...
    }
    return Response(endpoints)


def video_search(request):
    search_query = request.GET.get('search', None)
    if search_query:
        videos = Video.objects.filter(Q(title__icontains=search_query))
    else:
        videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})



class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)



class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]





        

# class VideoListView(generics.ListCreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search_query = self.request.query_params.get('search', None)
#         if search_query:
#             queryset = queryset.filter(Q(title__icontains=search_query))
#         return queryset