from rest_framework.permissions import BasePermission


from .models import Contributor, Project, Issue, Comment


class IsAuthor(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class IsProjectContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return Contributor.objects.filter(project=obj, user=request.user).exists()
    
