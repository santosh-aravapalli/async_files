import os,asyncio,aiofiles
from django.contrib import messages
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Employee
from asgiref.sync import sync_to_async


# Create your views here.

def simple_upload(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST['age']
        designation  = request.POST['designation']
        location = request.POST['location']
        address = request.POST['address']

        try:
            Employee.objects.create(
                name=name,
                age = age,
                designation=designation,
                location=location,
                address = address
            )
        except Exception as e:
            messages.error(request,str(e))

        myfile = request.FILES['myfile']
        if str(myfile).split('.')[1] == 'csv':
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return HttpResponse("file is saved in :{}".format(uploaded_file_url))
        else:
            messages.error(request,"file is not csv format")
    return render(request,'simple_file_upload.html')


async def handle_uploaded_file(f):
    if str(f).split('.')[1] == 'csv':
        fs = FileSystemStorage()
        filename = fs.save(f.name, f)
        uploaded_file_url = fs.url(filename)
        async with aiofiles.open(f"media/{f.name}", "wb+") as destination:
            for chunk in f.chunks():
                await destination.write(chunk)
        return "file is uploades : {}".format(uploaded_file_url)
    else:
        return "file is not csv"

@sync_to_async
def db_insertion(data):
    try:
        Employee.objects.create(**data)
    except Exception as e:
        print(str(e))


async def async_uploader(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST['age']
        designation = request.POST['designation']
        location = request.POST['location']
        address = request.POST['address']
        data = {
            "name": name,
            "age": age,
            "designation": designation,
            "location": location,
            "address": address
        }

        await db_insertion(data)
        await handle_uploaded_file(request.FILES["myfile"])

        return HttpResponse("file uploaded in ")

    return render(request, "async_file_upload.html")
