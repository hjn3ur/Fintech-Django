from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# importing loading from django template
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Investor, Company, Message, Picture, Project
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import PictureForm
from django.template import defaultfilters
from datetime import datetime
from django.utils import formats


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # val = type of user - 1 is investor, 2 company
        val = request.POST.get('type')
        if val == "1":

            if create_investor(request):
                # user successfully created
                return HttpResponseRedirect("/lokahi/")
            else:
                # bad username, go back to signup page
                return go_to_signup()
        else:
            if create_company(request):
                # company successfully created
                return HttpResponseRedirect("/lokahi/")
            else:
                # bad username, go back to signup
                return go_to_signup()
    else:
        # before form is submitted
        return go_to_signup()


def create_investor(request):
    username = request.POST.get('username')
    firstname = request.POST.get('firstName')
    lastname = request.POST.get('lastName')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if not User.objects.filter(username=username).exists():
        # Django hashes password automatically
        user = User.objects.create_user(username=username, email=email, password=password)
        # group = Group.objects.get(name='Investors')
        # user.groups.add(group)
        investor = Investor.objects.create(username=username, first_name=firstname, last_name=lastname,
                                           email=email,
                                           password=password)
        return True
    else:
        return False


def go_to_signup():
    template = loader.get_template("sign_up.html")
    return HttpResponse(template.render())


def create_company(request):
    company_time = datetime.now()
    company_update = datetime.now()
    company_name = request.POST.get('Companyname')
    company_username = request.POST.get('username')
    company_password = request.POST.get('password1')
    company_ceo = request.POST.get('CEO')
    company_email = request.POST.get('email')
    company_state = request.POST.get('state')
    company_country = request.POST.get('country')
    company_phone = request.POST.get('Phone')
    company_sector = request.POST.get('sector')
    company_industry = request.POST.get('industry')
    if not User.objects.filter(username=company_username).exists():
        user = User.objects.create_user(username=company_username, email=company_email, password=company_password)
        company = Company.objects.create(company_time=company_time, company_name=company_name,
                                         company_username=company_username,
                                         company_password=company_password, company_ceo=company_ceo,
                                         company_email=company_email, company_state=company_state,
                                         company_country=company_country, company_phone=company_phone,
                                         company_sector=company_sector, company_industry=company_industry)
        return True
    else:
        return False


@csrf_exempt
def investor(request):
    if request.user.is_authenticated():
        if is_investor(request):
            template = loader.get_template("investor_view.html")
            users = Company.objects.all()
            context = {
                'users': users,
            }
        elif is_site_manager(request):
            template = loader.get_template("investor_view.html")
            users = Company.objects.all()
            context = {
                'users': users,
            }
        else:
            company = Company.objects.get(company_username=request.user.username)
            if request.method == 'POST':

                form = PictureForm(request.POST, request.FILES)
                newpic = Picture(picfile=request.FILES['picfile'], owner=company.company_username,
                                 timestamp=datetime.now(), investor='')
                newpic.save()

            else:
                form = PictureForm()

            pictures = Picture.objects.filter(owner=company.company_username)
            return render_to_response('company_home.html', {'pictures': pictures, 'form': form, 'company': company},
                                      context_instance=RequestContext(request))



    else:
        return go_to_login()


def is_investor(request):
    return Investor.objects.filter(username=request.user.username).exists()


def is_site_manager(request):
    return request.user.groups.filter(name='site_manager').exists()


def company_page(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        company = Company.objects.get(company_name=value)
        if not is_site_manager(request):
            investor = Investor.objects.get(username=request.user.username)
        else:
            investor = 'site_manager'
        if request.method == 'POST':

            form = PictureForm(request.POST, request.FILES)
            newpic = Picture(picfile=request.FILES['picfile'], owner=company.company_username, timestamp=datetime.now(),
                             investor=investor.username)
            newpic.save()
        else:
            form = PictureForm()

        pictures = Picture.objects.filter(owner=company.company_username)
        projects = Project.objects.filter(owner=company.company_username)
        return render_to_response('company_page.html',
                                  {'pictures': pictures, 'form': form, 'company': company, 'projects': projects,
                                   'authenticated': is_site_manager(request)},
                                  context_instance=RequestContext(request))

    else:
        return go_to_login()


@csrf_exempt
def edit_company(request):
    if request.user.is_authenticated():
        if is_site_manager(request):
            value = request.GET.get('value', '1')
            company = Company.objects.get(company_name=value)
        else:
            company = Company.objects.get(company_username=request.user.username)

        if request.method == 'POST':
            return edit_company_submit(request, company)
        else:
            return load_company_edit(request, company)
    else:
        return go_to_login()


def edit_company_submit(request, company):
    company.company_update = datetime.now()
    company.company_ceo = request.POST.get('CEO')
    company.company_email = request.POST.get('email')
    company.company_state = request.POST.get('state')
    company.company_country = request.POST.get('country')
    company.company_phone = request.POST.get('Phone')
    company.company_sector = request.POST.get('sector')
    company.company_industry = request.POST.get('industry')
    company.save(
        update_fields=['company_update', 'company_ceo', 'company_email', 'company_state', 'company_country',
                       'company_phone',
                       'company_sector', 'company_industry'])
    return HttpResponseRedirect("/lokahi/home")


def load_company_edit(request, company):
    context = {
        'company': company,
    }
    template = loader.get_template('company_edit.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def edit_investor(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            investor1 = Investor.objects.get(username=request.user.username)
            investor1.first_name = request.POST.get('firstName')
            investor1.email = request.POST.get('email')
            investor1.last_name = request.POST.get('lastName')
            investor1.save(update_fields=['first_name', 'last_name', 'email'])
            return HttpResponseRedirect("/lokahi/home")
        else:
            investor1 = Investor.objects.get(username=request.user.username)
            context = {
                'investor1': investor1,
            }
            template = loader.get_template('investor_edit.html')
            return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


def go_to_login():
    return HttpResponseRedirect("/lokahi/")


@csrf_exempt
def go_to_edit():
    template = loader.get_template("company_edit.html")
    return HttpResponse(template.render())


def groups_home(request):
    if request.user.is_authenticated():
        template = loader.get_template('groups_home.html')
        context = {

        }
        return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


def messages_home(request):
    if request.user.is_authenticated():
        messages = Message.objects.filter(receiver=request.user.username)
        companies = unique_companies(messages)
        sentMessages = Message.objects.filter(sender=request.user.username)
        context = {
            'companies': companies,
            'messages': sentMessages
        }
        template = loader.get_template('messages_home.html')
        return HttpResponse(template.render(context, request))

    else:
        return go_to_login()


def unique_companies(query_set):
    dict = {}
    for query in query_set:
        dict[query.sender] = 1
    return dict


def messages_from(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        messages = Message.objects.filter(sender=value, receiver=request.user.username)
        context = {
            'messages': messages,
        }
        template = loader.get_template("messages_from.html")
        return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


@csrf_exempt
def compose_message(request):
    if request.user.is_authenticated():
        context = {}
        if request.method == 'POST':
            create_message(request)
            return HttpResponseRedirect("/lokahi/messages_home")
        else:
            users = User.objects.all()
            context = {
                'users': users
            }
            template = loader.get_template('compose_message.html')
            return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


def create_message(request):
    receiver = request.POST.get('receiver')
    message = request.POST.get('message')
    sender = request.user.username
    Message.objects.create(sender=sender, receiver=receiver, message=message)


@csrf_exempt
def add_project(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            timestamp = datetime.now()
            projects = request.POST.getlist('project')
            value = request.GET.get('value', '1')
            owner=  Company.objects.get(company_username=request.user.username)
            project = Project.objects.create(timestamp= timestamp, project=projects, owner= owner)
            return HttpResponseRedirect("/lokahi/home")
        else:
            company = Company.objects.get(company_username=request.user.username)
            context = {
                'company': company,
            }
            template = loader.get_template('add_projects.html')
            return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


@csrf_exempt
def advanced_search(request):
    if request.user.is_authenticated():
        if request.method == 'POST':

            return HttpResponseRedirect("/lokahi/home")
        else:
            investor1 = Investor.objects.get(username=request.user.username)
            context = {
                'investor1': investor1,
            }
            template = loader.get_template('advanced_search.html')
            return HttpResponse(template.render(context, request))

    else:
        return go_to_login()


def create_site_admin(request):
    Group.objects.get_or_create(name='site_manager')

    user, created = User.objects.get_or_create(username='manager')
    user.set_password('abc')
    user.save()
    group = Group.objects.get(name='site_manager')

    user.groups.add(group)
    return HttpResponseRedirect('/lokahi/')
