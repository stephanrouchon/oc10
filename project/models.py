from django.db import models
from django.conf import settings
import uuid

class TypeChoices(models.TextChoices):
    BACKEND = 'Back-end','Back-end'
    FRONTEND = 'Front-end','Front-end'
    IOS = 'iOS','iOS'
    ANDROID = 'Android','Android'

class IssuePriorityChoices(models.TextChoices):
    LOW = "LO","LOW"
    MEDIUM = "ME","MEDIUM"
    HIGH = "HI","HIGH"

class BaliseChoices(models.TextChoices):
    BUG="BUG","BUG"
    FEATURE ="FEATURE","FEATURE"
    COMPLETED = "COMPLETED","COMPLETED"

class IssueStatusChoices(models.TextChoices):
    TODO = "To_do","To Do"
    IN_PROGRESS = 'In_progress','In progress'
    FINISH = 'Finished', 'Finished'

class Project(models.Model):

    name= models.CharField(max_length=128)
    description =models.CharField(max_length=8000, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_type =  models.CharField(max_length=20, choices=TypeChoices.choices)


class Issue(models.Model):

    name=models.CharField(max_length=128)
    description =models.CharField(max_length=8000, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="issues")
    priority = models.CharField(max_length=20, choices=IssuePriorityChoices.choices, blank=True, null=True)
    balise = models.CharField(max_length=20, choices=BaliseChoices.choices, blank=True, null=True)
    status = models.CharField(max_length=20, choices=IssueStatusChoices.choices, default=IssueStatusChoices.TODO)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="issues")
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="assigned_issues")

    def save(self, *args, **kwargs):
        """Affecte l'auteur du projet par défaut si `assignee` n'est pas défini"""
        if not self.assignee:
            self.assignee = self.project.author
        super().save(*args, **kwargs)
    

class Comment(models.Model):

    description=models.CharField(max_length=8000)
    created_time = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='comments')
    

class Contributor(models.Model):

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions')
    
    class Meta:
        unique_together = ('project','user')