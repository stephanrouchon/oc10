from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .permissions import IsProjectContributor, IsAuthor
import project.serializers
from .models import Project, Issue, Comment, Contributor


class ProjectViewset(ModelViewSet):

    serializer_class = project.serializers.ProjectListSerializer
    detail_serializer_class = project.serializers.ProjectDetailSerializer
  

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):

        if self.action == "retrieve":
            return self.detail_serializer_class
        return self.serializer_class

    def get_permissions(self):

        if self.action in ['list','create']:
            permission_classes = [IsAuthenticated]
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsProjectContributor]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthor]
        else : 
            permission_classes == [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(
            project=project,
            user=self.request.user
        )


class ProjectIssueViewset(ModelViewSet):

    serializer_class = project.serializers.IssueSerializer
    detail_serializer_class = project.serializers.IssueDetailSerializer

    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        serializer.save(project_id=project_id, author=self.request.user)

    def get_object(self):
        project_id = self.kwargs.get('project_pk')
        issue_id = self.kwargs.get('issue_pk')
        try:
            return Issue.objects.get(project_id=project_id, id=issue_id)
        except Issue.DoesNotExist:
            raise ("Cette issue n'existe pas pour ce projet")

    def get_permissions(self):
        if self.action in ["list",'create']:
            permission_classes = [IsProjectContributor]
        elif self.action == "retrieve":
            permission_classes = [ IsProjectContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthor]
        else:
            permission_classes = [IsProjectContributor]

        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Récupère l'id du projet dans l'url
        project_id = self.kwargs.get('project_pk')
        data = request.data.copy()
        data['project'] = project_id

        serializer = self.get_serializer(
            instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewset(ModelViewSet):

    serializer_class = project.serializers.CommentSerializer
    detail_serializer_class = project.serializers.CommentDetailSerializer

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_pk')
        return Comment.objects.filter(issue_id=issue_id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        issue_id = self.kwargs.get('issue_pk')
        serializer.save(issue_id=issue_id, author=self.request.user)
        return super().perform_create(serializer)

    def get_permissions(self):
        if self.action in ["list",'create']:
            permission_classes = [IsProjectContributor]
        elif self.action == "retrieve":
            permission_classes = [IsProjectContributor]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthor]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorViewset(ModelViewSet):

    serializer_class = project.serializers.ContributorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()
    

class UserProjectsAndIssuesView(APIView):

    permission_classes = [IsAuthenticated, IsProjectContributor]

    def get(self, request, *args, **kwargs):
        #récupere les projets ou l'utilisateur est contributeur
        user_projects = Project.objects.filter(contributors__user=request.user).distinct()
        project_serializer = project.serializers.ProjectListSerializer(user_projects, many = True)

        #Recupère les issues associés à ces projets
        user_issues = Issue.objects.filter(project__in=user_projects).distinct()
        issue_serializer = project.serializers.IssueSerializer(user_issues, many=True)

        return Response({
            "projects": project_serializer.data,
            "issues": issue_serializer.data
        })

class UserAssignedIssuesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Récupère les issues assignées à l'utilisateur
        user_assigned_issues = Issue.objects.filter(assignee=request.user).distinct()
        issue_serializer = project.serializers.IssueSerializer(user_assigned_issues, many=True)

        return Response({
            "assigned_issues": issue_serializer.data
        })
