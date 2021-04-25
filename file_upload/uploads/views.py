import os,asyncio,aiofiles
from django.contrib import messages
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Employee
from asgiref.sync import sync_to_async
from time import time

# Create your views here.

def simple_upload(request):
    if request.method == "POST":
        t = time()
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
            return HttpResponse("file is saved in :{} and in time of :{}".format(uploaded_file_url,time()-t))
        else:
            messages.error(request,"file is not csv format")
    return render(request,'simple_file_upload.html')


async def handle_uploaded_file(data,f):
    if str(f).split('.')[1] == 'csv':
        #fs = FileSystemStorage()
        #filename = fs.save(f.name, f)
        #uploaded_file_url = fs.url(filename)
        await db_insertion(data)
        async with aiofiles.open(f"media/{f.name}", "wb+") as destination:
            for chunk in f.chunks():
                await destination.write(chunk)
        return "file is uploades "
    else:
        return "file is not csv"


@sync_to_async
def db_insertion(data):
    try:
        Employee.objects.create(**data)
    except Exception as e:
        print(str(e))


def async_uploader(request):
    if request.method == "POST":
        t=time()
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

        #await db_insertion(data)
        #await handle_uploaded_file(request.FILES["myfile"])
        asyncio.run(handle_uploaded_file(data,request.FILES["myfile"]))

        return HttpResponse("file uploaded in time of : {}".format(time()-t))

    return render(request, "async_file_upload.html")
