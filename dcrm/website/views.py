from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, BlogPostForm, ExcelImportForm, HigherEducationForm
from django.contrib.auth.models import User
from .models import Record, BlogPost, UserProfile, Message, Education
import pandas as pd


def home(request):
	records = Record.objects.all()
	if request.user.is_authenticated:
		user_profile = UserProfile.objects.filter(user=request.user).last()
		followers_count = user_profile.followers.count()
		following_count = user_profile.followings.count()
		received_messages_count = Message.objects.filter(recipient=request.user).count()
		send_messages_count = Message.objects.filter(sender=request.user).count()
		blogs_count = BlogPost.objects.filter(author=request.user).count()
		total_records = Record.objects.filter().count()
		users_to_follow = User.objects.exclude(id=request.user.id)

		context = {
			'user_profile': user_profile,
			'followers_count': followers_count,
			'following_count': following_count,
			'received_messages_count': received_messages_count,
			'send_messages_count': send_messages_count,
			'blogs_count': blogs_count,
			'total_records': total_records,
			'users_to_follow': users_to_follow,
			'active_users': User.objects.filter(is_active=True).count()
		}
	else:
		context = {
			'records': records
		}

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', context)


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(email=username, password=password)
			UserProfile.objects.get_or_create(user=user)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
	if request.user.is_authenticated:
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')


def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def blog_post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_post_list.html', {'posts': posts})


def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_post_detail.html', {'post': post})


def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'add_blog_post.html', {'form': form})


def author_profile(request, author_id):
    author = get_object_or_404(User, id=author_id)

    blogs_count = BlogPost.objects.filter(author=author).count()
    profile_instance = UserProfile.objects.filter(user=author)
    education_details = author.education.all()

    if profile_instance:
    	image_url = profile_instance.last().profile_image.url if profile_instance.last().profile_image else None
    	user_profile = profile_instance.last()
    else:
    	image_url = 'https://images.unsplash.com/photo-1608231857279-40bea0778f5f?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=100&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY5MDk1NTQ1NQ&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=100'
    return render(request, 'author_profile.html', {
    	'author': author,
    	'image_url': image_url,
    	'user_profile': user_profile,
    	'blogs': blogs_count,
    	'education_details': education_details
    })


def edit_profile(request):
    return render(request, 'edit_profile.html')


def import_records(request):
	if request.method == 'POST':
		form = ExcelImportForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			if file.name.endswith('.xlsx'): #If it's not an .xlsx file, pandas will handle it as a CSV file pd.read_csv(file)
				df = pd.read_excel(file, engine='openpyxl')
				records = []
				for _, row in df.iterrows():
				    record = Record(
				        first_name=row['First Name'],
				        last_name=row['Last Name'],
				        email=row['Email'],
				        phone=row['Phone'],
				        address=row['Address'],
				        city=row['City'],
				        state=row['State'],
				        zipcode=row['Zipcode'],
				    )
				    records.append(record)
				Record.objects.bulk_create(records)
				return redirect('home')
	else:
	    form = ExcelImportForm()
	return render(request, 'import_records.html', {'form': form})


def follow_user(request, author_id):
    author = get_object_or_404(User, id=author_id)
    author_profile, created = UserProfile.objects.get_or_create(user=author)
    user_profile = UserProfile.objects.get(user=request.user)
    author_profile.followers.add(request.user)
    user_profile.followings.add(author)
    return redirect('author_profile', author_id=author_id)


def unfollow_user(request, author_id):
    author = get_object_or_404(User, id=author_id)
    author_profile = UserProfile.objects.get(user=author)
    user_profile = UserProfile.objects.get(user=request.user)
    author_profile.followers.remove(request.user)
    user_profile.followings.remove(author)
    return redirect('author_profile', author_id=author_id)


def send_message(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user

        message = Message.objects.create(sender=sender, recipient=recipient, content=content)

        messages.success(request, 'Message sent successfully.')
        return redirect('author_profile', author_id=recipient_id)

    return render(request, 'send_message.html', {'recipient': recipient})


def inbox(request):
    user = request.user
    received_messages = Message.objects.filter(recipient=user).order_by('-timestamp')
    return render(request, 'inbox.html', {'received_messages': received_messages})


def mark_message_as_read(request, message_id):
    message = Message.objects.get(id=message_id)
    if request.user == message.recipient:
        message.is_read = True
        message.save()
    return redirect('inbox')

def reply_to_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user

        # Create a new reply message
        reply_message = Message.objects.create(sender=sender, recipient=message.sender, content=content)
        
        return render(request, 'reply_success.html', {'reply_message': reply_message})
    
    return render(request, 'reply_message.html', {'message': message})


def add_higher_education(request):
    if request.method == 'POST':
        form = HigherEducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.is_higher_education = True
            education.save()
            return redirect('author_profile', author_id=request.user.id)

    return render(request, 'add_higher_education.html', {'form': HigherEducationForm()})