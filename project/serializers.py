from rest_framework.serializers import ModelSerializer, SerializerMethodField

from project.models import Project, Issue, Comment, Contributor



class CommentSerializer(ModelSerializer):

    author_username = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','description','created_time','author', 'author_username']

    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username
        return None
        

class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorSerializer(ModelSerializer):

    username = SerializerMethodField()
    project_name = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['id','project', 'project_name',  'user','username']

    def get_username(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def get_project_name(self, obj):
        return obj.project.name


class IssueSerializer(ModelSerializer):

    assignee_username = SerializerMethodField()
    priority_display = SerializerMethodField()
    balise_display = SerializerMethodField()
    status_display = SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['id',
                  'name',
                  'priority_display',
                  'balise_display',
                  'status_display',
                  'assignee_username',
                  ]
        
    def get_assignee_username(self, obj):
        return obj.assignee.username
    
    def get_priority_display(self, obj):
        return obj.get_priority_display()
    
    def get_balise_display(self, obj):
        return obj.get_balise_display()
    
    def get_status_display(self, obj):
        return obj.get_status_display()

class IssueDetailSerializer(ModelSerializer):

    assignee_username = SerializerMethodField()
    priority_display = SerializerMethodField()
    balise_display = SerializerMethodField()
    status_display = SerializerMethodField()
    author_username = SerializerMethodField()

    comments = CommentSerializer(many=True)

    class Meta:
        model = Issue
        fields = ['name','description','created_time','assignee_username', 'author_username','priority_display','balise_display','status_display', 'comments']

    def get_assignee_username(self, obj):
        return obj.assignee.username
    
    def get_priority_display(self, obj):
        return obj.get_priority_display()
    
    def get_balise_display(self, obj):
        return obj.get_balise_display()
    
    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_author_username(self, obj):
        if obj.author:
            return obj.author.username
        return None

class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author','project_type']


class ProjectDetailSerializer(ModelSerializer):

    issues = IssueSerializer(many=True)
    contributors = ContributorSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

