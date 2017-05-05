from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# importing loading from django template
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Person, Investor, Company, Message, Picture, Project, Report
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import PictureForm
from django.template import defaultfilters
from datetime import datetime
from itertools import chain
from django.utils import formats

# encryption
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
from base64 import b64decode, b64encode
random_generator= Random.new().read

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


def new_messages(request):
    return "(" + str(Message.objects.filter(receiver=request.user.username, read=False).count()) + ")"


@csrf_exempt
def investor(request):
    if request.user.is_authenticated():
        if is_site_manager(request):
            template = loader.get_template("admin_view.html")
            users = Report.objects.all()
            context = {
                'users': users,
                'new_messages': new_messages(request),
            }
        elif is_investor(request):
            investor = Investor.objects.get(username=request.user.username)
            if investor.banned:
                return go_to_banned()
            template = loader.get_template("investor_view.html")

            users = load_all_viewable_reports(request)
            context = {
                'users': users,
                'new_messages': new_messages(request),
            }
        else:
            company = Company.objects.get(company_username=request.user.username)
            if company.banned:
                return go_to_banned()
            if request.method == 'POST' and request.FILES.__len__() != 0:

                form = PictureForm(request.POST, request.FILES)
                newpic = Picture(picfile=request.FILES['picfile'], owner=company.company_username,
                                 timestamp=datetime.now(), investor='')
                newpic.save()

            else:
                form = PictureForm()

            pictures = Picture.objects.filter(owner=company.company_username, files_id="")
            projects = Project.objects.filter(owner=company.company_name, project_id="")
            return render_to_response('company_home.html',
                                      {'pictures': pictures, 'form': form, 'company': company, 'projects': projects,
                                       'new_messages': new_messages(request), },
                                      context_instance=RequestContext(request))

        return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


def load_all_viewable_reports(request):
    public_set = Report.objects.filter(public="public")
    groups_set = get_group_reports(request)
    users = unique_reports(public_set, groups_set)
    return users


def get_group_reports(request):
    reports = Report.objects.all()
    list = []
    for report in reports:
        groups = report.company_groups.split(",")
        for group in groups:
            if request.user.groups.filter(name=group).exists():
                list.append(report)
    return list


def unique_reports(query1, query2):
    dict = {}
    for query in query1:
        dict[query] = 1
    for query in query2:
        dict[query] = 1
    return dict


def is_investor(request):
    return Investor.objects.filter(username=request.user.username).exists()


def is_site_manager(request):
    return request.user.groups.filter(name='site_manager').exists()


def company_page(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        value2 = request.GET.get('value2', '2')
        report = Report.objects.get(report_id=value2)
        company = Company.objects.get(company_name=value)

        if not is_site_manager(request):
            investor = Investor.objects.get(username=request.user.username)
            investor_username = investor.username
        else:
            investor_username = 'site_manager'

        if request.method == 'POST' and request.FILES.__len__() != 0:

            form = PictureForm(request.POST, request.FILES)
            encrypted_option = request.POST.get("encrypted")
            if encrypted_option == "Yes":
                encrypted = True
            else:
                encrypted = False
            newpic = Picture(picfile=request.FILES['picfile'], owner=company.company_username, timestamp=datetime.now(),
                             investor=investor_username, files_id=value2, encrypted=encrypted)
            newpic.save()
        else:
            form = PictureForm()

        pictures = Picture.objects.filter(owner=company.company_username, files_id=value2)
        projects = Project.objects.filter(owner=company.company_name, project_id=value2)
        return render_to_response('company_page.html',
                                  {'report': report, 'pictures': pictures, 'form': form, 'company': company,
                                   'projects': projects,
                                   'authenticated': is_site_manager(request)},
                                  context_instance=RequestContext(request))

    else:
        return go_to_login()


def list(request):
    return HttpResponseRedirect('/lokahi/')


@csrf_exempt
def edit_company(request):
    if request.user.is_authenticated():
        if is_site_manager(request):
            value = request.GET.get('value', '1')
            value2 = request.GET.get('value2', '2')
            company = Company.objects.get(company_name=value)
        else:
            company = Company.objects.get(company_username=request.user.username)

        if request.method == 'POST':
            return edit_company_submit(request, company)
        else:
            return load_company_edit(request, company)
    else:
        return go_to_login()


@csrf_exempt
def edit_report(request):
    if request.user.is_authenticated():
        value1 = request.GET.get('value', '1')
        value2 = request.GET.get('value2', '2')
        report = Report.objects.get(report_id=value2)
        project = Project.objects.filter(owner=value1, project_id=value2)
        if request.method == 'POST':
            value1 = request.GET.get('value', '1')
            value2 = request.GET.get('value2', '2')
            project = Project.objects.filter(owner=value1, project_id=value2)
            report.company_update = datetime.now()
            report.company_ceo = request.POST.get('CEO')
            report.company_email = request.POST.get('email')
            report.company_state = request.POST.get('state')
            report.company_country = request.POST.get('country')
            report.company_phone = request.POST.get('Phone')
            report.company_sector = request.POST.get('sector')
            report.company_industry = request.POST.get('industry')
            for project in project:
                idnum = project.id
                project.project = request.POST.get(str(idnum))
                project.save(update_fields=['project'])
            report.save(
                update_fields=['company_update', 'company_ceo', 'company_email', 'company_state',
                               'company_country',
                               'company_phone',
                               'company_sector', 'company_industry'])
            return HttpResponseRedirect("/lokahi/company_page/?value2=" + value2 + "&value=" + value1)
        else:
            template = loader.get_template('company_edit.html')
            return render_to_response('company_edit.html',
                                      {'company': report, 'project': project},
                                      context_instance=RequestContext(request))

    else:
        return go_to_login()


@csrf_exempt
def delete_report(request):
    if request.user.is_authenticated():
        value2 = request.GET.get('value2', '2')
        report = Report.objects.get(report_id=value2).delete();

    return HttpResponseRedirect("/lokahi/home")


def edit_report_submit(request, report):
    report.company_update = datetime.now()
    report.company_ceo = request.POST.get('CEO')
    report.company_email = request.POST.get('email')
    report.company_state = request.POST.get('state')
    report.company_country = request.POST.get('country')
    report.company_phone = request.POST.get('Phone')
    report.company_sector = request.POST.get('sector')
    report.company_industry = request.POST.get('industry')
    report.save(
        update_fields=['company_update', 'company_ceo', 'company_email', 'company_state',
                       'company_country',
                       'company_phone',
                       'company_sector', 'company_industry'])
    return HttpResponseRedirect("/lokahi/home")


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
        update_fields=['company_update', 'company_ceo', 'company_email', 'company_state',
                       'company_country',
                       'company_phone',
                       'company_sector', 'company_industry'])
    return HttpResponseRedirect("/lokahi/home")


def load_company_edit(request, report):
    return render_to_response('company_editonly.html',
                              {'company': report, },
                              context_instance=RequestContext(request))


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


def go_to_banned():
    template = loader.get_template("banned.html")
    return HttpResponse(template.render())


@csrf_exempt
def go_to_edit():
    template = loader.get_template("company_edit.html")
    return HttpResponse(template.render())


@csrf_exempt
def groups_home(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            group_created = create_group(request)
        else:
            group_created = False

        return load_groups_home(request, group_created)
    else:
        return go_to_login()


def load_groups_home(request, group_created):
    template = loader.get_template('groups_home.html')
    groups = get_user_groups(request)
    authenticated = is_site_manager(request)
    investor = is_investor(request) or authenticated
    context = {
        'groups': groups,
        'group_created': group_created,
        'investor': investor,
        'authenticated': authenticated,
        'new_messages': new_messages(request),
    }
    return HttpResponse(template.render(context, request))


def create_group(request):
    group_name = request.POST.get('group')
    Group.objects.get_or_create(name=group_name)
    user = User.objects.get(username=request.user.username)
    group = Group.objects.get(name=group_name)
    groups = request.user.groups.all()
    user.groups.add(group)
    for x in groups:

        if x == group:
            return False

    return True


def get_user_groups(request):
    if is_site_manager(request):
        return Group.objects.all()
    else:
        return request.user.groups.all()


@csrf_exempt
def selected_group(request):
    if request.user.is_authenticated():
        group = request.GET.get('value', '1')
        if request.method == 'POST':
            if request.POST.get("add_user"):
                user_to_add = request.POST.get('person')
                add_user_to_group(request, user_to_add, group)
            if request.POST.get("remove_user"):
                user_to_remove = request.POST.get('person')
                remove_from_group(request, user_to_remove, group)
        return load_selected_group(request, group)
    else:
        return go_to_login()


def load_selected_group(request, group):
    template = loader.get_template('selected_group.html')
    members = User.objects.filter(groups__name=group)
    addable = User.objects.exclude(username__in=members.values('username'))
    removable = User.objects.filter(username__in=members.values('username'))
    investorss = Investor.objects.exclude(username__in=members.values('username'))
    authenticated = is_site_manager(request)
    investor = is_investor(request) or authenticated
    users = User.objects.all()
    authenticated = is_site_manager(request)
    context = {
        'group': group,
        'members': members,
        'users': users,
        'authenticated': authenticated,
        'removable': removable,
        'addable': addable,
        'investor': investor,
        'investorss': investorss,
        'new_messages': new_messages(request)
    }
    return HttpResponse(template.render(context, request))


def remove_self_from_group(request):
    if request.user.is_authenticated():
        group = request.GET.get('value', '1')
        user = User.objects.get(username=request.user.username)
        g = Group.objects.get(name=group)
        g.user_set.remove(user)
        return HttpResponseRedirect("/lokahi/groups_home/")
    else:
        return go_to_login()


def add_user_to_group(request, user_to_add, group):
    user = User.objects.get(username=user_to_add)
    group = Group.objects.get(name=group)
    user.groups.add(group)


def remove_from_group(request, user_to_remove, group):
    user = User.objects.get(username=user_to_remove)
    g = Group.objects.get(name=group)
    g.user_set.remove(user)


@csrf_exempt
def messages_home(request):
    if request.user.is_authenticated():

        if request.method == "POST":
            create_message(request)
            return HttpResponseRedirect("/lokahi/messages_home/")

        receivedmessages = Message.objects.filter(receiver=request.user.username)
        sentMessages = Message.objects.filter(sender=request.user.username)
        conversations = unique_companies(receivedmessages, sentMessages)

        recipients = User.objects.exclude(username=request.user.username)
        authenticated = is_site_manager(request)
        users = User.objects.all()
        context = {
            'conversations': conversations,
            'messages': sentMessages,
            'investor': is_investor(request) or is_site_manager(request),
            'users': users,
            'authenticated': authenticated,
            'recipients': recipients,
            'new_messages': new_messages(request),
        }
        template = loader.get_template('messages_home.html')
        return HttpResponse(template.render(context, request))

    else:
        return go_to_login()


def unique_companies(query_set, query_set2):
    dict = {}
    for query in query_set:
        dict[query.sender] = 1
    for query in query_set2:
        dict[query.receiver] = 1
    return dict


@csrf_exempt
def messages_from(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        if request.method == "POST":
            respond_message(request, value)

        message_received = Message.objects.filter(sender=value, receiver=request.user.username)
        mark_read(message_received)
        message_sent = Message.objects.filter(sender=request.user.username, receiver=value)
        sort_messages(message_received, message_sent)
        sorted_messages = sort_messages(message_received, message_sent)

        # for message in sorted_messages:
        #     if message.encrypted:
        #         decrypt_message(message.message, message.RSA_key)

        context = {
            'sender': value,
            'messages': sorted_messages,
            'investor': is_investor(request) or is_site_manager(request),
            'new_messages': new_messages(request),
            'authenticated': is_site_manager(request),
        }
        template = loader.get_template("messages_from.html")
        return HttpResponse(template.render(context, request))

    else:
        return go_to_login()


def sort_messages(message_received, message_sent):
    messages = sorted(
        chain(message_received, message_sent),
        key=lambda instance: instance.timestamp)
    return messages


def mark_read(message_received):
    for message in message_received:
        message.read = True
        message.save()


def create_message(request):
    timestamp = datetime.now()
    receiver = request.POST.get('receiver')
    message = request.POST.get('message')
    encrypted = request.POST.get('encryptMessage')
    RSA_key = ""
    encrypted_message = str.encode("")
    if encrypted:
        encryption_output = encrypt_message(message)
        message = ""
        encrypted_message = encryption_output[0][0]
        RSA_key = encryption_output[1]
    hash_id = SHA256.new(str.encode(str(timestamp))).hexdigest()[:24]
    sender = request.user.username
    Message.objects.create(message_timestamp=timestamp, sender=sender, receiver=receiver, message=message,
                           encrypted=encrypted, RSA_key=RSA_key, hash_id=hash_id, encrypted_message=encrypted_message)


def respond_message(request, receiver):
    timestamp = datetime.now()
    message = request.POST.get('message')
    sender = request.user.username
    encrypted = request.POST.get('encryptMessage')
    RSA_key = ""
    encrypted_message = str.encode("")
    if encrypted:
        encryption_output = encrypt_message(message)
        message = ""
        print(encryption_output[0])
        encrypted_message = encryption_output[0]
        RSA_key = encryption_output[1]
    hash_id = SHA256.new(str.encode(str(timestamp))).hexdigest()[:24]
    Message.objects.create(message_timestamp=timestamp, sender=sender, receiver=receiver, message=message,
                           encrypted=encrypted, RSA_key=RSA_key, hash_id=hash_id, encrypted_message=encrypted_message)


def decrypted_message(request):
    if request.user.is_authenticated() and request.user.username in [request.GET.get('sender', '1'), request.GET.get('receiver', '2')]:
        # Need to be authenticated and also be either the sender or receiver of the message to view the decrypted
        # version -- so that copying then sending the url to another user won't work
        sender = request.GET.get('sender', '1')
        receiver = request.GET.get('receiver', '2')
        id = request.GET.get('id', '3')

        encrypted_message = Message.objects.get(sender=sender, receiver=receiver, hash_id=id)
        print(encrypted_message.encrypted_message)
        original_message = decrypt_message((encrypted_message.encrypted_message,), encrypted_message.RSA_key).decode("utf-8")

        context = {
            'original_message': original_message
        }
        template = loader.get_template("decrypted_message.html")
        return HttpResponse(template.render(context, request))
    else:
        go_to_login()


def encrypt_message(message_text):
    key = RSA.generate(1024, random_generator)
    #encrypted_message = key.publickey().encrypt(str.encode(message_text), 32)
    #private_key = key.exportKey().decode("utf-8")

    encrypted_message=key.publickey().encrypt(message_text.encode(), 32)
    enc_message=b64encode(encrypted_message[0])
    private_key=key.exportKey()
    print(str(enc_message))
    return [enc_message, private_key]


def decrypt_message(encrypted_message, private_key):
    key = RSA.importKey(private_key)
    decrypted_message = key.decrypt(b64decode(encrypted_message[0]))
    return decrypted_message


@csrf_exempt
def add_project(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            timestamp = datetime.now()
            projects = request.POST.get('project')
            owner = Company.objects.get(company_username=request.user.username)
            project = Project.objects.create(timestamp=timestamp, project=projects, owner=owner)
            return HttpResponseRedirect("/lokahi/home")
        else:
            company = Company.objects.get(company_username=request.user.username)
            context = {
                'company': company,
                'new_messages': new_messages(request),
            }
            template = loader.get_template('add_projects.html')
            return HttpResponse(template.render(context, request))
    else:
        return go_to_login()


def remove_project(request):
    value1 = request.GET.get('value', '1')
    value2 = request.GET.get('value2', '2')
    report = Project.objects.get(project_id=value1, project=value2).delete();

    return HttpResponseRedirect("/lokahi/home")


def remove_project1(request):
    if request.user.is_authenticated():
        value1 = request.GET.get('value', '1')
        value2 = request.GET.get('value2', '2')
        value3 = request.GET.get('value3', '3')
        report = Project.objects.get(project_id=value1, project=value2).delete();
        return HttpResponseRedirect("/lokahi/company_page/?value2=" + value1 + "&value=" + value3)


def remove_file(request):
    if request.user.is_authenticated():
        value1 = request.GET.get('value', '1')
        value2 = request.GET.get('value2', '2')
        value3 = request.GET.get('value3', '3')
        report = Picture.objects.get(files_id=value1, picfile=value2).delete();
        return HttpResponseRedirect("/lokahi/company_page/?value2=" + value1 + "&value=" + value3)


def remove_file1(request):
    value1 = request.GET.get('value', '1')
    value2 = request.GET.get('value2', '2')
    report = Picture.objects.get(files_id=value1, picfile=value2).delete();
    return HttpResponseRedirect("/lokahi/home")


@csrf_exempt
def advanced_search(request):
    if request.user.is_authenticated():
        authenticated = is_site_manager(request)
        investor = is_investor(request)
        if request.method == 'POST':
            CEO = request.POST.get('CEO')
            phone = request.POST.get('Phone')
            Companyname = request.POST.get('Companyname')
            sector = request.POST.get('sector')
            industry = request.POST.get('industry')
            email = request.POST.get('email')
            state = request.POST.get('state')
            country = request.POST.get('country')
            projects = request.POST.get('projects')
            reportDate = request.POST.get('reportDate')
            if request.POST.get('andOr') == "allFields":
                search_type = 'Match all fields'
            else:
                search_type = 'Match at least one field'

            users = load_all_viewable_reports(request)
            users2 = Report.objects.all()
            if authenticated:
                context = {
                    'CEO': CEO,
                    'phone': phone,
                    'Companyname': Companyname,
                    'sector': sector,
                    'industry': industry,
                    'email': email,
                    'state': state,
                    'country': country,
                    'projects': projects,
                    'reportDate': reportDate,
                    'search_type': search_type,
                    'users': users2,
                    'investor': investor,
                    'authenticated': authenticated
                }

                template = loader.get_template('search_results.html')
                return HttpResponse(template.render(context, request))
            else:
                context = {
                    'CEO': CEO,
                    'phone': phone,
                    'Companyname': Companyname,
                    'sector': sector,
                    'industry': industry,
                    'email': email,
                    'state': state,
                    'country': country,
                    'projects': projects,
                    'reportDate': reportDate,
                    'search_type': search_type,
                    'users': users,
                    'investor': investor,
                    'authenticated': authenticated
                }

                template = loader.get_template('search_results.html')
                return HttpResponse(template.render(context, request))
        else:
            context = {
                'new_messages': new_messages(request),
                'investor': investor,
                'authenticated': authenticated
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


def create_form(request):
    company = Company.objects.get(company_username=request.user.username)
    projects = Project.objects.filter(owner=company.company_name, project_id="")
    pictures = Picture.objects.filter(owner=company.company_username, files_id="")
    if projects:
        return render_to_response('create_report.html',
                                  {'company': company, 'projects': projects, 'pictures': pictures},
                                  context_instance=RequestContext(request))
    else:
        if request.method == 'POST':

            form = PictureForm(request.POST, request.FILES)
            newpic = Picture(picfile=request.FILES['picfile'], owner=company.company_username,
                             timestamp=datetime.now(), investor='')
            newpic.save()

        else:
            form = PictureForm()
        message = 'You need to add a project to create a report.'
        return render_to_response('company_home.html',
                                  {'company': company, 'projects': projects, 'pictures': pictures, 'message': message,
                                   'form': form},
                                  context_instance=RequestContext(request))


def report(request):
    company = Company.objects.get(company_username=request.user.username)
    projects = Project.objects.filter(owner=company.company_name)
    pictures = Picture.objects.filter(owner=company.company_username)
    report_time = datetime.now()
    report_public = request.POST.get('public')
    report_private = request.POST.get('private')
    report_update = datetime.now()
    report_name = company.company_name
    report_ceo = company.company_ceo
    report_email = company.company_email
    report_state = company.company_state
    report_country = company.company_country
    report_phone = company.company_phone
    report_sector = company.company_sector
    report_industry = company.company_industry
    if report_public == None:
        report_public = ''
    if report_private == None:
        report_private = ''
    for project in projects:
        report_project = project.project
    report_file = ""
    for x in pictures:
        report_file += str(x.picfile) + '\n'

    if Project.objects.filter(project_id="").exists() or Picture.objects.filter(files_id="").exists():
        report = Report.objects.create(public=report_public, private=report_private, company_time=report_time,
                                       company_update=report_update, company_name=report_name,
                                       company_ceo=report_ceo, company_email=report_email,
                                       company_state=report_state, company_country=report_country,
                                       company_phone=report_phone,
                                       company_sector=report_sector, company_industry=report_industry,
                                       company_project=report_project, company_file=report_file)
        for project in projects:
            if project.project_id == '':
                project.project_id = report.report_id
                project.save(update_fields=['project_id'])
        for x in pictures:
            if x.files_id == '':
                x.files_id = report.report_id
                x.save(update_fields=['files_id'])

    return HttpResponseRedirect('/lokahi/home/')


def view_reports(request):
    if request.user.is_authenticated():
        company = Company.objects.get(company_username=request.user.username)
        report = Report.objects.filter(company_name=company.company_name)
        return render_to_response('reports.html',
                                  {'report': report, 'new_messages': new_messages(request), },
                                  context_instance=RequestContext(request))


def list_of_users(request):
    if request.user.is_authenticated():
        companys = Company.objects.all()
        investors = Investor.objects.all()
        return render_to_response('list_of_users.html',
                                  {'companys': companys, 'investors': investors},
                                  context_instance=RequestContext(request))


def selected_user(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        companys = Company.objects.all()
        investors = Investor.objects.all()
        company = ''
        investor = ''
        for x in companys:
            if x.company_name == value:
                company = Company.objects.get(company_name=value)
                return render_to_response('selected_user.html',
                                          {'company': company},
                                          context_instance=RequestContext(request))
        split = value.split()
        for x in investors:
            if x.username == split[0]:
                investor = Investor.objects.get(username=split[0])
                return render_to_response('selected_user2.html',
                                          {'investor': investor},
                                          context_instance=RequestContext(request))


def ban_user(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        companys = Company.objects.all()
        investors = Investor.objects.all()
        for x in companys:
            if x.company_name == value:
                company = Company.objects.get(company_name=value)
                ban = company.banned
                if ban == False:
                    company.banned = True
                    company.save(update_fields=['banned'])
                else:
                    company.banned = False
                    company.save(update_fields=['banned'])
                return render_to_response('list_of_users.html',
                                          {'companys': companys, 'investors': investors},
                                          context_instance=RequestContext(request))
        split = value.split()
        for x in investors:
            if x.username == split[0]:
                investor = Investor.objects.get(username=split[0])
                ban = investor.banned
                if ban == False:
                    investor.banned = True
                    investor.save(update_fields=['banned'])
                else:
                    investor.banned = False
                    investor.save(update_fields=['banned'])
                return render_to_response('list_of_users.html',
                                          {'companys': companys, 'investors': investors},
                                          context_instance=RequestContext(request))


@csrf_exempt
def report_final(request):
    if request.user.is_authenticated():
        value = request.GET.get('value', '1')
        value2 = request.GET.get('value2', '2')
        report = Report.objects.get(report_id=value2)
        company = Company.objects.get(company_name=value)
        if request.method == "POST":

            if request.POST.get('add_group'):
                add_group_to_report(request, report)
            if request.POST.get('remove_group'):
                remove_group_from_report(request, report)

        pictures = Picture.objects.filter(owner=company.company_username, files_id=value2)
        projects = Project.objects.filter(owner=company.company_name, project_id=value2)
        groups = request.user.groups.all()
        removable = report.company_groups.split(',')
        return render_to_response('listof_reports.html',
                                  {'report': report, 'pictures': pictures, 'company': company, 'projects': projects,
                                   'new_messages': new_messages(request), 'groups': groups, 'removable': removable},
                                  context_instance=RequestContext(request))

    else:
        return go_to_login()


def add_group_to_report(request, report):
    group_to_add = request.POST.get('group_to_add')
    if report.company_groups == "":
        report.company_groups = group_to_add
    elif report.company_groups.endswith(","):
        report.company_groups += group_to_add
    else:
        report.company_groups += "," + group_to_add
    report.save(
        update_fields=['company_groups'])


def remove_group_from_report(request, report):
    group_to_remove = request.POST.get('group_to_remove')
    report.company_groups = report.company_groups.replace(group_to_remove + ",", "")
    report.company_groups = report.company_groups.replace(group_to_remove, "")
    report.save(update_fields=['company_groups'])


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .serializers import ReportSerializer, PictureSerializer


@csrf_exempt
def list_all_reports(request):
    # report = Report.objects.all()
    # report = load_all_viewable_reports(request)
    report = Report.objects.filter(public='public')
    data = JSONParser().parse(request)
    user = User.objects.get(username=data['user'])
    reports = Report.objects.all()
    list = []
    for i in reports:
        groups = i.company_groups.split(",")
        for group in groups:
            if user.groups.filter(name=group).exists():
                list.append(i)

    report = unique_reports(report, list)

    if request.method == 'POST':
        serializer = ReportSerializer(report, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def report_detail(request, pk):
    try:
        report = Report.objects.get(report_id=pk)
    except Report.DoesNotExist:
        return JsonResponse({"bad": True})
        # return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReportSerializer(report)
        return JsonResponse(serializer.data)


@csrf_exempt
def get_pictures(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        pictures = Picture.objects.filter(files_id=data['report_id'])
        serializer = PictureSerializer(pictures, many=True)
        return JsonResponse(serializer.data, safe=False)


from django.contrib.auth import authenticate


@csrf_exempt
def login_accepted(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':

        data = JSONParser().parse(request)
        # exists = User.objects.filter(username=data['username']).exists()
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            exists = True
        else:
            exists = False
        return JsonResponse({"exists": exists}, status=201)


def delete_message(request):
    value1 = request.GET.get('value', '1')
    value2 = request.GET.get('value2', '2')
    value3 = request.GET.get('value3', '3')
    message = Message.objects.get(sender=value1, hash_id=value2, receiver=value3).delete();

    return HttpResponseRedirect("/lokahi/messages_home/")
