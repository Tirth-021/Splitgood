from django.shortcuts import render

from activites.models import Activities
from group.models import Group


# Create your views here.
def show_activity(request):
    groups = Group.objects.filter(users=request.user)
    activity = Activities.objects.filter(group__in=groups).values("activity", "amount", "expense__expense_name",
                                                                  "group__group_name", "user__username", "date")
    context = {"activity": activity}
    return render(request, 'activities.html', context)
