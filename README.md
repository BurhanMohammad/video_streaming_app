# Project Documentation

Welcome to the documentation for [Your Project Name]! This documentation provides a comprehensive overview of the project's functionality, features, and usage.

## Table of Contents

1. [Introduction](#introduction)
2. [User Authentication](#user-authentication)
3. [Video Management](#video-management)
4. [Video Streaming](#video-streaming)
5. [API Endpoints](#api-endpoints)
6. [Search Videos](#search-videos)
7. [Additional Notes](#additional-notes)

## Introduction

Video Streaming App is a web application that allows users to manage and stream videos. The application is built using Django, Django Rest Framework, and OpenCV for video streaming. It provides a user-friendly interface for users to register, log in, manage their videos, and stream videos. This documentation covers various aspects of the project to help you understand its features and how to use them effectively.

## User Authentication

User authentication is a key feature of the application, allowing users to securely access their accounts.

### Register User

- Endpoint: `/api/register/` (POST)
- This endpoint allows users to register by providing their desired username and password.
- Upon successful registration, a user account is created, and an authentication token is generated.
- Example:
  ```http
  POST /api/register/
  Content-Type: application/json
  
  {
    "username": "newuser",
    "password": "newpassword"
  }
### Register User
- Endpoint: `/api/register/` (POST)
- Users can log in using their registered credentials to access their accounts.
- Upon successful login, an authentication token is generated.
- Example:
  ```http
  POST /api/login/
  Content-Type: application/json

   {
  "username": "existinguser",
  "password": "userpassword"
    } 
```

### Logout
- Endpoint:   ` /api/logout/ ` (POST)
-Allows authenticated users to log out and invalidate their authentication token.
- Example:
  ```http
    POST /api/logout/
    Authorization: Token <auth_token>
  ```  
    
## Video Management
Users can manage their videos, including creating, updating, and deleting videos.

### Create Video
- Endpoint: `/api/videos/` (POST)
-Allows authenticated users to create a new video by providing a title and video file URL.
- Example:
 ```http
  POST /api/videos/
  Authorization: Token <auth_token>
  Content-Type: multipart/form-data

  title=Sample+Video
  video_file=<video_file_data>
```
## Update Video
-Endpoint: `/api/videos/<video_id>/` (PUT)

-Allows authenticated users to update the details of an existing video.
-Example:
```http
   PUT /api/videos/<video_id>/
   Authorization: Token <auth_token>
   Content-Type: application/json

 {
    "title": "Updated Video Title"
  }
```
## Delete Video

- Endpoint: `/api/videos/<video_id>/` (DELETE)

- Allows authenticated users to delete a video.
- Example:
```http
 DELETE /api/videos/<video_id>/
 Authorization: Token <auth_token>
```
## Get Video List
-Endpoint: `/api/videos/` (GET)
-Allows authenticated users to retrieve a list of all available videos.
-Optionally, users can search for videos by providing a search query.
-Example:
```http
 GET /api/videos/
 Authorization: Token <auth_token>
```
## Get Video Details
-Endpoint: `/api/videos/<video_id>/` (GET)
-Allows authenticated users to retrieve details of a specific video.
-Example:
```http
 GET /api/videos/<video_id>/
 Authorization: Token <auth_token>
```
## Video Streaming

The application supports video streaming using OpenCV with multithreading.


## Stream Video

-Endpoint: `/api/videos/<video_id>/stream/` (GET)
-Allows authenticated users to stream a video in real-time using OpenCV.
-Example:
```http
 GET /api/videos/<video_id>/stream/
 Authorization: Token <auth_token>
```

## API Endpoints
The application provides the following API endpoints for different functionalities:

-User Authentication: `/api/register/`, `/api/login/`, `/api/logout/`
-Video Management: `/api/videos/`, `/api/videos/<video_id>/`, `/api/videos/<video_id>/stream/`
-API Documentation: `/api/documentation/`

## Search Videos
Users can search for videos based on title.

## Search Videos
- Endpoint: `/api/videos/?search=<search_query>` (GET)
-Allows authenticated users to search for videos using a search query.
-Example:
```http
 GET /api/videos/?search=cat
 Authorization: Token <auth_token>
```
## Additional Notes
-The provided documentation offers an overview of the project's features and usage. Refer to the actual code files for detailed implementation and examples.
-Make sure to install the required packages and dependencies before running the project.
-If you encounter any issues or have questions, feel free to reach out to the project maintainers.



