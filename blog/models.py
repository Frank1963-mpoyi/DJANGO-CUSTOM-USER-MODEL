from django.db import models
from django.utils import timezone
#from django.utils.translation import gettext_lazy  its translation module of the Django project. 1st option or
from django.utils.translation import gettext_lazy as _ # second option // this text translation to the end user
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
'''
django by default has a user model 
instead of having username to login we can extend to email address


'''

class  CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
                )
        
        if other_fields.get('is_superuser')is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
                )       
        return self.create_user(email, user_name, first_name, password, **other_fields)


    def create_user(self, email, user_name, first_name, password, **other_fields):
        # validation check to perform 
        if not email:
            raise ValueError(_('You must provide an email address'))
        email =self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name = first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    

    
class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    #email = models.EmailField(gettext_lazy('email address'), unique=False) FIRST OPTION SEE IMPORT 
    user_name =models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    # the unique identify code we are going to utelize for our user model
    USERNAME_FIELD = 'email' # we change username field to email this username is when you login in your system
    REQUIRED_FIELDS =['user_name', 'first_name']# because when you login will be require to put username that why we put as also a default name
    
    objects =  CustomAccountManager() # here we tell our model to utilize this model
    
    def __str__(self):
        return self.user_name