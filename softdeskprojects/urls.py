"""
URL configuration for softdeskprojects project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import UserViewset
from project.views import ProjectViewset, ProjectIssueViewset,CommentViewset, ContributorViewset, UserAssignedIssuesView, UserProjectsAndIssuesView


router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')
router.register('project', ProjectViewset, basename = 'project' )
router.register('contributor', ContributorViewset, basename='contributor')


urlpatterns = [
    path('admin', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/project/<int:project_pk>/issues',
         ProjectIssueViewset.as_view({'get': 'list', 'post':'create'}),
         name='project-issues'),
    path('api/project/<int:project_pk>/issues/<int:issue_pk>',
         ProjectIssueViewset.as_view({'get':'retrieve',
                                      'put': 'update',
                                      'delete':'destroy'}),
         name='project-issue-detail' ),
    path('api/project/<int:project_pk>/issues/<int:issue_pk>/comments/', 
         CommentViewset.as_view({'get': 'list', 'post':'create'}),
         name='project-issue-comments'),
    path('api/user/<int:user_pk>/project-issues/', UserProjectsAndIssuesView.as_view(), name='user-projects-issues'),
    path('api/user/<int:user_pk>/assigned-issues/', UserAssignedIssuesView.as_view(), name='user-assigned-issues'),
]  
