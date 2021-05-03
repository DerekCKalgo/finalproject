from django.db import models
import re
import bcrypt


class RegisterManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['first']) < 2:
            errors["first"] = "First name has to be at least 2 characters"
        if len(postData['last']) < 2:
            errors["last"] = "Last name has to be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']=("Invalid email address")
        if len(postData['password']) < 8:
            errors["password"] = "Password has to be at least 8 characters"
        if (postData['password']) != (postData['confirm']):
            errors["confirm"] = "Passwords should match"
        return errors 
    def login_validator(self, postData):
        errors = {}
        loginUser = Register.objects.filter(email=postData['loginemail'])
        if len(loginUser) > 0:
            if bcrypt.checkpw(postData['loginpassword'].encode(), loginUser[0].password.encode()):
                print("Password matches")
            else:
                errors['loginpassword']="Incorrect password"
        else:
            errors['loginemail']="email does not exist"
        return errors

class Register(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegisterManager()

class Photo(models.Model):
    imagefile = models.ImageField(upload_to='images/', null=True)
    caption = models.TextField()
    current_user = models.ForeignKey(Register, related_name="photos", on_delete=models.CASCADE)
    user_who_comment = models.ManyToManyField(Register, related_name="comment_photos")
    user_who_like = models.ManyToManyField(Register, related_name="like_photos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

