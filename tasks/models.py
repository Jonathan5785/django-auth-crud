from ast import Delete
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    
    # Usar related_name para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name='get_custom_user',  # Cambia este nombre según tu preferencia
        blank=True,
        
        
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='get_custom_user_permissions',  # Cambia este nombre según tu preferencia
        blank=True,
        
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self) -> bool:
        return self.role.name == "Admin"
    
    @property
    def is_security(self) -> bool:
        return self.role.name == "Seguridad"



class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username
    
    



