import os,asyncio,aiofiles
from django.contrib import messages
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .models import Employee
from asgiref.sync import sync_to_async
from time import time
import csv
import re
import codecs

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
        file_content = myfile.read()
        decode_content = file_content.decode('utf-8-sig').splitlines()
        decode_content.pop()
        reader = csv.reader(decode_content)
        status = 200
        row_count = 1
        for row in reader:
            if len(row) != 2 :
                status = 502
                msg = f"at row {row_count} row lenght is not matching "
                break
            if not re.compile("^[0-9]{10}$").match(row[0]):
                status = 502
                msg = f" invalid msisdn at row {row_count} "
                break
            row_count = row_count+1

        if status == 200:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return HttpResponse("file is saved in :{} and in time of :{}".format(uploaded_file_url,time()-t))
        else:
            messages.error(request, "file is not saved")
            return HttpResponse(f"file is not saved in error msg :{msg} and in time of :{time() - t}")

    return render(request,'simple_file_upload.html')


async def DataValidation(data):
    decode_content = data.decode('utf-8-sig').splitlines()
    decode_content.pop()
    reader = csv.reader(decode_content)
    status = 200
    msg = 'data validation done successfully'
    row_count = 1
    for row in reader:
        if len(row) != 2:
            status = 502
            msg = f"at row {row_count} row lenght is not matching "
            break
        if not re.compile("^[0-9]{10}$").match(row[0]):
            status = 502
            msg = f" invalid msisdn at row {row_count} "
            break
        row_count = row_count + 1

    return status,msg


async def handle_uploaded_file(f):
    if str(f).split('.')[1] == 'csv':
        async with aiofiles.open(f"media/{f.name}", "wb+") as destination:
            for chunk in f.chunks():
                await destination.write(chunk)
        return "file uploaded"
    else:
        return "file is not csv"


@sync_to_async
def db_insertion(data):
    try:
        Employee.objects.create(**data)
        return "db insertion done"
    except Exception as e:
        print(str(e))
        return str(e)


async def async_uploader(request):
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

        myfile = request.FILES["myfile"]
        task1 = asyncio.create_task(db_insertion(data))
        datavalid_tasks = list()
        for chunk in myfile.chunks():
            datavalid_tasks.append(asyncio.create_task(DataValidation(chunk)))
        task2 = asyncio.create_task(handle_uploaded_file(request.FILES["myfile"]))
        done = await asyncio.gather(
            task1,
            *datavalid_tasks
        )

        res = await task2

        print(done,res)

        return HttpResponse("file uploaded in time of : {}".format(time()-t))

    return render(request, "async_file_upload.html")
