from django.db import models

class Tasks(models.Model):
    username = models.CharField(max_length=50,null=False)
    desc = models.CharField(max_length=300,null=False,default="No description")
    task = models.CharField(max_length=200,null=False)
    due_date = models.DateTimeField(null=False)
    priority = models.CharField(max_length=10,default="High")
    completed = models.CharField(max_length=10,null=False,default="Not completed")
    assigned_to = models.CharField(max_length=50,default="self")
    assigned_mail = models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return f"{self.username} {self.task}"
    