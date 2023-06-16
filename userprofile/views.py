from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from group.models import Group
from userprofile.models import Profile


@method_decorator(login_required(login_url='/login/'), name='dispatch')
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
            if picture:
                profile.avatar = picture
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            profile.mobile_number = mobile
            user.set_password(new_password)
            profile.save()
            user.save()

        groups = Group.objects.filter(users=request.user.id)
        profile = Profile.objects.filter(user=request.user).first()
        context = {'groups': groups, 'profile': profile}
        return render(request, 'dashboard.html', context)
