from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from group.models import Group
from userprofile.models import Profile


@login_required(login_url='login/')
def user_profile(request):
    user = request.user
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    email = user.email
    profile = Profile.objects.filter(user=user)[0]
    message = ""
    context = {'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email,
               'profile': profile, 'message': message}
    return render(request, 'userprofile.html', context)


@login_required(login_url='login/')
def updateuser(request):
    picture = request.FILES.get('profile-picture')
    first_name = request.POST.get('first-name')
    last_name = request.POST.get('last-name')
    email = request.POST.get('email')
    old_password = request.POST.get('old-password')
    new_password = request.POST.get('new-password')
    mobile = request.POST.get('mobile')
    if ('rmphoto' in request.POST):
        picture = ''
    if old_password is None or old_password == '':
        profile = Profile.objects.get(user=request.user)
        user = User.objects.get(id=request.user.id)
        profile.avatar = picture
        profile.mobile_number = mobile
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.save()
        user.save()


    elif not request.user.check_password(old_password):
        message = 'Password Wrong'
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        email = user.email
        profile = Profile.objects.filter(user=user)[0]
        context = {'first_name': first_name, 'last_name': last_name, 'username': username, 'email': email,
                   'profile': profile, 'message': message}
        return render(request, 'userprofile.html', context)
    else:
        profile = Profile.objects.get(user=request.user)
        user = User.objects.get(id=request.user.id)
        profile.avatar = picture
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.mobile_number = mobile
        user.set_password(new_password)
        profile.save()
        user.save()
    groups = Group.objects.filter(users=request.user.id)
    profile = Profile.objects.filter(user=request.user)[0]
    context = {'groups': groups, 'profile': profile}
    return render(request, 'dashboard.html', context)
