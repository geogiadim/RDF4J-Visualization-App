from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "healthProblems/index.html", context)


def ChartRenderView(request):
    # get the url params from axios request
    print("dsfsdfgdgsfdgdfsgfdsgfdsgfdsgdsfgfdsg")
    # context
    context = {'data': False, 'model': request.GET.get('model')}
    if request.GET.get('model') == 'sleep-problems':
        context['model_name'] = 'Sleep Problems'
        print(context['model'])
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)