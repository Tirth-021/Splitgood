from userprofile.models import Profile


def profile(request):
    if request.user.is_authenticated:
        usprofile = Profile.objects.filter(user=request.user)[0]
        return {'profile': usprofile}
    else:
        return {}
