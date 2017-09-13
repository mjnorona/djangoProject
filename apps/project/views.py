import bcrypt
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Prompt, Solution, Collaboration, Like, Following
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, ListView

from .forms import ProfileImageForm
from .models import ProfileImage
from random import randint, random, choice

def gethome(request):
    #Prompt.objects.all().delete()
    #list = User.objects.all().delete()
    # for i in list:
    #     print i.email
    return render(request, 'project/gethome.html')

# Create your views here.
def index(request):
    #Prompt.objects.all().delete()
    #list = User.objects.all().delete()
    # for i in list:
    #     print i.email
    return render(request, 'project/index.html')

def index(request):
    return render(request,'project/index.html')

@login_required
def gethome(request):
    return render(request, 'project/gethome.html')

def register(request):

    if request.method == "POST":
        values = User.objects.register(request.POST)

        if values[0]:
            request.session['id'] = values[1]
            return redirect("/home")
        else:
            for error in values[1]:
                messages.error(request, error)
            return redirect("/")



def login(request):
    if request.method == "POST":
        login = User.objects.login(request.POST)
        # print login
        if login[0]:
            if login[3].email == "admin@creativespaces.com":
                request.session['id'] = login[2]
                print 'jkkop'
                print request.session['id']
                return redirect('/admin')
            else:
                request.session['id'] = login[2]
                return redirect('/home')
        else:
            messages.error(request, 'Email or password is incorrect')
            return redirect('/')

def admin(request):
    print request.session['id']
    if request.session['id']:
        print 'jijj'
        for i in Prompt.objects.all():
            print i.content, i.id
        # print(prompt[0].content)
        user = User.objects.get(id = request.session['id'])
        content = {
            'first_name': user.first_name,
            'user': user,
            'prompt': Prompt.objects.all()
        }
        return render(request, 'project/admin.html', content)
    else:
        return redirect('/')

def home(request):
    if 'id' in request.session:

        # text = "How do you improve an umbrella?"
        # text1 = "How can we lower the housing price in San Francisco?"
        # text2 = "How can we protect the trees?"
        # text3="How can we control the heat in environment?"
        # text4="How can we help earthquake victims?"
        # prompt = Prompt.objects.get(id = 8).delete()
        # prompt.id = 5
        # prompt.save()
        print Prompt.objects.count()
        # bool = True
        # while(bool):
        #     get = randint(1, Prompt.objects.count())
        #     print get
        #     if Prompt.objects.filter(id = get):
        #         prompt = Prompt.objects.filter(id = get)
        #         bool = False
        prompt = Prompt.objects.order_by('?').first()
        print prompt
        for i in Prompt.objects.all():
            print i.content, i.id
        print(prompt)
        user = User.objects.get(id = request.session['id'])
        content = {
            'first_name': user.first_name,
            'user': user,
            'prompt': prompt
        }
        return render(request, 'project/home.html', content)
    else:
        return redirect('/')

def edit(request):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        print User.objects.all()
        print "in edit"
        for i in User.objects.all():
            print i.first_name

        content = {
            'user': user
        }
        return render(request, 'project/edit.html', content)
    else:
        return redirect('/')

def edit_submit(request):
    if request.method == "POST":
        edit = User.objects.edit(request.POST, request.session['id'])
        if edit[0] == False:
            messages.error(request, edit[1])
        # if not edit:
        #     messages.error('Current password is incorrect')
        return redirect('/edit')

def submit(request, id):
    if request.method == "POST":
        print id
        Solution.objects.createSolution(request.POST, request.session['id'], id)
    return redirect('solutions', id = id)

def solutions(request, id):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        prompt = Prompt.objects.get(id = id)
        solutions = Solution.objects.filter(prompt = prompt).annotate(num_likes = Count('likes')).order_by('-num_likes')
        content = {
            'prompt': prompt,
            'solutions': solutions,
            'user': user
        }
        return render(request, 'project/solutions.html', content)
    else:
        return render('/home')

def collaborate(request, id):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        solution = Solution.objects.get(id = id)
        print solution.content
        # print Collaboration.objects.get(solution = solution)
        # somecollab = Collaboration.objects.get(solution = solution)
        # print somecollab.solution.content
        # collaborations = Collaboration.objects.filter(prompt = prompt)
        if(Collaboration.objects.filter(solution = solution).exists()):
            ##collaboration already existed
            collaboration = Collaboration.objects.get(solution = solution)
            collaboration.users.add(user)
            collaboration.save()
            ##add login_user to collaboration.users

        else:
            ##create collaboration
            collaboration = Collaboration.objects.create(solution = solution)
            ##add login_user
            collaboration.users.add(solution.user)
            collaboration.users.add(user)
            collaboration.save()
            ##also add solution.user (thats person who made the solution)

        write = {
            'collaboration': collaboration,
            'solution': solution,
            'login_user': user
        }
        return render(request, 'project/collaborate.html', write)
    else:
        return render('/home')

def like(request, id):
    print "solution " + id
    user = User.objects.get(id = request.session['id'])
    solution = Solution.objects.get(id = id)
    print solution.user.id
    userofsolution = User.objects.get(id = solution.user.id)
    getsolutions = Solution.objects.filter(user__id = userofsolution.id).annotate(num_likes = Count('likes')).order_by('-num_likes')[:3]
    like = Like.objects.create(user = user, solution = solution)
    count = 0
    for i in getsolutions:
        count = i.likes.count()+count
    count = count*10
    userofsolution.point = count
    userofsolution.save()
    print 'usersol'
    print 'come on' + str(userofsolution.point)
    print 'prompt ' + str(solution.prompt.id)
    return redirect('solutions', id = solution.prompt.id)

def likeonprofile(request, id):
    print "solution " + id
    user = User.objects.get(id = request.session['id'])
    solution = Solution.objects.get(id = id)
    print solution.user.id
    userofsolution = User.objects.get(id = solution.user.id)
    getsolutions = Solution.objects.filter(user__id = userofsolution.id).annotate(num_likes = Count('likes')).order_by('-num_likes')[:3]
    like = Like.objects.create(user = user, solution = solution)
    count = 0
    for i in getsolutions:
        count = i.likes.count()+count
    count = count*10
    userofsolution.point = count
    userofsolution.save()
    print 'usersol'
    print 'come on' + str(userofsolution.point)
    print 'prompt ' + str(solution.prompt.id)
    return redirect('profile', id = solution.user.id)

def logout(request):
    request.session.clear()
    return redirect('/')

def profile(request, id):
    if 'id' in request.session:
        user = User.objects.get(id = id)
        print request.session['id']
        solutions = Solution.objects.filter(user__id = user.id).annotate(num_likes = Count('likes')).order_by('-num_likes')[:3]
        getsolutionsforcount = Solution.objects.filter(user__id = user.id).annotate(num_likes = Count('likes')).order_by('-num_likes')

        count = 0
        likes = Like.objects.filter(solution__id = 1)


        for i in getsolutionsforcount:

            count = count + i.likes.count()


        count = count*10

        context = {
            "user": user,
            "solutions": solutions,
            "likes": likes,
            "points": count
        }


    return render(request, 'project/profile.html', context)


def simple_upload(request):
    context = {'uploaded_file_url':''}
    user = User.objects.get(id = request.session['id'])
    print 'sdsd'
    print user.id
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        values = User.objects.saveprofilepicture(uploaded_file_url, request.session['id'])

        return redirect('/profile/'+str(request.session['id']))
    
    somecontext = {
            #"uploaded_file_url": uploaded_file_url,
            "getuser": user,
            "somenumber": str(request.session['id'])
    }

    return render(request, 'project/profile_image_form.html', somecontext )

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
