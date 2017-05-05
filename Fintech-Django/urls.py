from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
                  url(r'^lokahi/', include('Lokahi.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', RedirectView.as_view(url='/lokahi/', permanent=True)),
                  url(r'^', include(router.urls)),
                  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

