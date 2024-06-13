from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class user(models.Model):

    id=models.AutoField(primary_key=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    name=models.CharField(max_length=50)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class FriendRequest(models.Model):
    id=models.AutoField(primary_key=True)
    from_user = models.ForeignKey(user,related_name='send_request',on_delete=models.CASCADE)
    to_user = models.ForeignKey(user,related_name='received_request',on_delete=models.CASCADE)
    status = models.CharField(choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')),max_length=50)
    created_at = models.DateField(auto_now_add=True)