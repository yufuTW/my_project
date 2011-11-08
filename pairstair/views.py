from django.http import HttpResponse
from pairstair.models import Pair, Programmer
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

def _populate_pairs():
    programmer_list = Programmer.objects.all().order_by("id")
    for mainIndex in range(len(programmer_list)):
        for secondIndex in range(mainIndex+1, len(programmer_list)):
            pair = Pair(programmer_one = programmer_list[mainIndex].name, programmer_two = programmer_list[secondIndex])
            pair.save()


def view_stair(request):
    programmers = Programmer.objects.all().order_by('id')
    reversed_list = programmers.reverse()[1:]
    pairs = Pair.objects.all()
    return render_to_response('pair_stair.html', RequestContext(request, {'programmers_for_columns':programmers,
             'programmers_for_rows': reversed_list, 'pairs':pairs}))


class FewerThanTwoProgrammersSubmitted(Exception):
    def __init__(self, message, data=None):
        assert data is None or type(data) is tuple
        self.message = message
        self.data = data

    def __str__(self):
        return self.message


def create_programmers_for_pair_stair(names):
    if len(names) < 2:
        raise FewerThanTwoProgrammersSubmitted(u"There should be two or more programmers for pair stair.")
    Programmer.objects.all().delete()
    for new_name in names:
        Programmer(name=new_name).save()

    _populate_pairs()


def create_pairs(request):
    if request.method == 'POST':
        names = request.POST['programmer_names'].split(',')
        try:
         create_programmers_for_pair_stair(names)
        except FewerThanTwoProgrammersSubmitted as ex:
            return render_to_response('create_pairs.html', RequestContext(request, {'error_message': ex.message}))
        return redirect(view_stair)
    return render_to_response('create_pairs.html', RequestContext(request))

def increase_times(request, first_programmer_name, second_programmer_name):
    pair = Pair.objects.filter(programmer_one = first_programmer_name, programmer_two = second_programmer_name)

    if len(pair) > 0:
        pair[0].times += 1
        pair[0].save()

    return view_stair(request)

