from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^showdata/', views.signup),
    url(r'^signup/', views.signup),
    url(r'^investor_view/', views.investor),
    url(r'^home/', views.investor, name='home'),
    url(r'^company_page/', views.company_page, name='company_page'),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^edit/', views.edit_company, name='edit_company'),
    url(r'^edit-investor/', views.edit_investor, name='edit_investor'),
    url(r'^messages_home/', views.messages_home, name='messages_home'),
    url(r'^messages_from/', views.messages_from, name='messages_from'),
    url(r'^compose_message/', views.compose_message, name='compose_message'),
    url(r'^add_project/', views.add_project, name='add_project'),
    url(r'^advanced_search/', views.advanced_search, name='advanced_search'),
    url(r'^groups_home/', views.groups_home, name='groups_home'),
    url(r'^create_site_admin/', views.create_site_admin, name='create_site_admin'),

]

# url(r'^investor_view/', TemplateView.as_view(template_name='investor_view.html'), name='investor_view'),
