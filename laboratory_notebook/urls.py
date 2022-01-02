from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from notebook import views
from notebook.authentification import signup_user, login_user, logout_user


urlpatterns = [
    path('admin/', admin.site.urls),

    # authentification
    path('signup/', signup_user, name="signup_user"),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),

    # notebook app
    path('', views.LaboratoryView.as_view(), name="home"),
    path('lab/<int:laboratory>/', views.LaboratoryDepartmentView.as_view(), name="lab_dep_view"),
    path('analyst_form/', views.get_analyst_form, name="get_analyst_form"),

    path('analyst/<int:analyst_pk>', views.superior_overview, name="superior_overview"),

    path('create/', views.create_task, name='create_task'),
    path('current/', views.view_current_tasks, name='view_current_tasks'),
    path('completed/', views.view_completed_tasks, name='view_completed_tasks'),

    path('task/<int:task_pk>', views.view_task, name='view_task'),
    path('task/<int:task_pk>/complete', views.complete_task, name='complete_task'),
    path('task/<int:task_pk>/delete', views.delete_task, name='delete_task'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
