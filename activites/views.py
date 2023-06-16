from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from activites.models import Activities
from group.models import Group


@login_required(login_url='login/')
def show_activity(request):
    groups = Group.objects.filter(users=request.user)
    activity = Activities.objects.filter(group__in=groups).exclude(
        ~Q(user=request.user.id) & Q(activity="Paid")).values("activity", "amount", "expense__expense_name",
                                                                "group__group_name", "user__username", "date",
                                                                "paid_to__lender__username",
                                                                "added_id__username").order_by("-date")
    paginator = Paginator(activity, 7)  # Create a Paginator instance with 6 items per page
    page_number = request.GET.get('page', 1)  # Get the current page number from the request's query parameters
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, 'activities.html', context)
