from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from note_app.forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from note_app.models import Note
from note_app.forms import FormNote

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('agenda')
    else:
        return redirect('login') 

def signup(request):

    if request.user.is_authenticated:
        return redirect('agenda')
    else:
        register_form = RegisterForm()

        if request.method == 'POST':
            register_form = RegisterForm(request.POST)

            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Te has registrado correctamente...!!')

                return redirect('/agenda')
        
        return render(request, 'template_user_signup.html', {
            'register_form': register_form
        })

@login_required(login_url="login")
def agenda(request):
    try:
        notes = Note.objects.filter(owner_id=request.session['_auth_user_id'])
    except:
        notes = []
    
    return render(request, 'template_agenda.html', {
        'notes': [[notes[j] for j in range(i, min(i+5, len(notes)))] for i in range(0, len(notes), 5)]
    })    

def login_page(request):
    if request.user.is_authenticated:
        return redirect('agenda')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user:
                login(request, user)
                return redirect('/agenda')
            else:
                messages.warning(request, 'No se ha podido acceder, verifica los datos e intentalo de nuevo...!!')   
        
        return render(request, 'template_login.html') 

@login_required(login_url="index")
def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url="index")
def create_note(request):
    if request.method == 'POST':
        form = FormNote(request.POST)
        form.instance.owner_id = request.session['_auth_user_id']
        
        if form.is_valid():
            form.save()
            return redirect('agenda')
    else:
        form = FormNote()

    return render(request, 'template_create_note.html', {'form': form})           

@login_required(login_url="index")
def note(request, id):
    notes = Note.objects.all()
    note = Note.objects.get(pk=id)

    return render(request, 'template_note.html', {
        'notes': notes,
        'note': note       
    })    

@login_required(login_url="index")
def edit_note(request, id):
    if request.method == 'GET':
        try:
            note = Note.objects.get(pk = id, owner_id=request.session['_auth_user_id'])
        except:
            return HttpResponse("La nota no existe")    

        return render(request, 'template_edit_note.html', {
            'notes': [],
            'note': note,
            'id' : id       
        }) 
    
    if request.method == 'POST':
        note = Note.objects.get(pk = id)
        note.title = request.POST['title']
        note.content = request.POST['content']

        note.save()
        
    return redirect('agenda')   

@login_required(login_url="index")
def notes(request):
    notes = Note.objects.all()

    return render(request, 'template_notes.html', {
        'notes': notes
    })

@login_required(login_url="index")
def delete_note(request, id):
    note = Note.objects.get(pk=id)
    note.delete()

    return redirect('agenda')