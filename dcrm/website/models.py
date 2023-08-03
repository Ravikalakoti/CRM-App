from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_image')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    job_profile = models.CharField(max_length=200, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    followings = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='education')
    is_higher_education = models.BooleanField(default=True)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    def __str__(self):
        return self.degree


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title