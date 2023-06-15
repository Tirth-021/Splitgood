from userprofile.models import Profile


def profile(request):
    usprofile = Profile.objects.filter(user=request.user)[0]
    return {'profile': usprofile}
