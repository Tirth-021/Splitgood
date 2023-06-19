from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from group.models import Group
from userprofile.models import Profile


class UserView(View):
    template_name = 'userprofile.html'

    def get_context_data(self):
        user = self.request.user
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        email = user.email
        profile = Profile.objects.filter(user=user).first()
        message = ""
        return {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'profile': profile,
            'message': message,
        }

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        picture = request.FILES.get('profile-picture', False)
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        old_password = request.POST.get('old-password')
        new_password = request.POST.get('new-password')
        mobile = request.POST.get('mobile')

        if 'rmphoto' in request.POST:
            picture = ''

        if old_password is None or old_password == '':
            profile = Profile.objects.get(user=request.user)
            user = User.objects.get(id=request.user.id)
            if picture:
                profile.avatar = picture
            profile.mobile_number = mobile
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            profile.save()
            user.save()

        elif not request.user.check_password(old_password):
            message = 'Password Wrong'
            context = self.get_context_data()
            context['message'] = message
            return render(request, self.template_name, context)

        else:
            profile = Profile.objects.get(user=request.user)
            user = User.objects.get(id=request.user.id)
            username = user.username
            if picture:
                profile.avatar = picture
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            profile.mobile_number = mobile
            user.set_password(new_password)
            profile.save()
            user.save()
            new_user = authenticate(request, username=username, password=new_password)
            login(request, new_user)
        groups = Group.objects.filter(users=request.user.id)
        paginator = Paginator(groups, 6)  # Create a Paginator instance with 6 items per page
        page_number = request.GET.get('page', 1)  # Get the current page number from the request's query parameters
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, 'dashboard.html', context)
