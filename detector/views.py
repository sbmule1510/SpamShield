from django.shortcuts import render, redirect
from .mongo import users_collection, history_collection
import re
from .spam_rules import check_spam
from bson import ObjectId
import threading
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    return render(request, 'detector/home.html')

def about(request):
    return render(request, 'detector/about.html')

def register(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("register_email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password != confirm_password:
                return render(request, "detector/register.html", {
                    "error": "Passwords do not match!"
                })
            existing_user = users_collection.find_one({
                "email": email
            })
            if existing_user:
                return render(request, "detector/register.html", {
                    "error": "Email already registered. Please login."
                })
            user = {
                "name": name,
                "email": email,
                "password": password
            }
            users_collection.insert_one(user)
            return redirect("/login/")
        except Exception:
            return render(request, "detector/register.html", {
                "error": "Something went wrong. Please try again."
            })
    return render(request, "detector/register.html")

def login(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = users_collection.find_one({
                "email": email,
                "password": password
            })
            if user:
                request.session["user_email"] = email
                request.session["user_name"] = user["name"]
                return redirect("/dashboard/")
            else:
                return render(request, "detector/login.html", {
                    "error": "Invalid Email or Password"
                })
        except Exception:
            return render(request, "detector/login.html", {
                "error": "Something went wrong. Please try again."
            })
    return render(request, "detector/login.html")

def dashboard(request):
    print(request.session.items())
    if "user_email" not in request.session:
        return redirect("/login/")
    return render(request, "detector/dashboard.html")

def logout(request):
    request.session.flush()
    return redirect("/login/")

def detect_spam(request):
    if "user_email" not in request.session:
        return redirect("/login/")
    result = ""
    if request.method == "POST":
        try:
            form_type = request.POST.get("form_type")
            if form_type == "single":
                subject = request.POST.get("subject", "").strip()
                message = request.POST.get("message", "").strip()
                result_container = {}
                def spam_task():
                    result_container["result"] = check_spam(subject, message)
                thread = threading.Thread(target=spam_task)
                thread.start()
                thread.join()
                result = result_container["result"]
                history_collection.insert_one({
                    "user_email": request.session["user_email"],
                    "subject": subject,
                    "message": message,
                    "result": result
                })
            elif form_type == "batch":
                uploaded_file = request.FILES.get("email_file")
                if uploaded_file:
                    file_data = uploaded_file.read().decode("utf-8")
                    result_container = {}
                    def spam_task():
                        result_container["result"] = check_spam("Batch Upload", file_data)
                    thread = threading.Thread(target=spam_task)
                    thread.start()
                    thread.join()
                    result = result_container["result"]
                    history_collection.insert_one({
                        "user_email": request.session["user_email"],
                        "subject": "Batch Upload",
                        "message": file_data,
                        "result": result
                    })
                else:
                    result = "Please select a text file."
        except Exception:
            result = "Something went wrong. Please try again."
    return render(request, "detector/detect_spam.html", {
        "result": result
    })

def history(request):
    if "user_email" not in request.session:
        return redirect("/login/")
    print("Logged User:", request.session["user_email"])
    user_email = request.session["user_email"]
    data = list(history_collection.find({
        "user_email": user_email
    }))
    for item in data:
        item["id"] = str(item["_id"])
    total_emails = history_collection.count_documents({
        "user_email": user_email
    })
    spam_emails = history_collection.count_documents({
        "user_email": user_email,
        "result": "Spam Email Detected!"
    })
    safe_emails = history_collection.count_documents({
        "user_email": user_email,
        "result": "Safe Email"
    })
    return render(request, "detector/history.html", {
        "data": data,
        "total_emails": total_emails,
        "spam_emails": spam_emails,
        "safe_emails": safe_emails
    })

def profile(request):
    if "user_email" not in request.session:
        return redirect("/login/")
    user = users_collection.find_one({
        "email": request.session["user_email"]
    })
    return render(request, "detector/profile.html", {
        "user": user
    })

def delete_history(request, id):
    if "user_email" not in request.session:
        return redirect("/login/")
    try:
        history_collection.delete_one({
            "_id": ObjectId(id)
        })
    except Exception:
        pass
    return redirect("/history/")

@api_view(['POST'])
def spam_api(request):
    subject = request.data.get("subject", "")
    message = request.data.get("message", "")
    result = check_spam(subject, message)
    return Response({
        "subject": subject,
        "result": result
    })