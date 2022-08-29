from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'test/index.html')

def room(request, room_name):
    return render(request, 'test/room.html', {
        'room_name': room_name
    })

def enter(request):
    return render(request,'test/enter.html')

def file_room(request,room_name,user_name):
    return render(request, 'test/room.html', {
        'room_name': room_name,
        'user_name':user_name
    })

