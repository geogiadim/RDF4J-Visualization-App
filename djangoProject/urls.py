from django.contrib import admin
from django.urls import path
from healthProblems import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('index/render', views.ChartRenderView, name="chart-render"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
