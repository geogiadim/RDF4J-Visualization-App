from django.shortcuts import render
import pandas as pd


def index(request):
    context = {}
    return render(request, "healthProblems/index.html", context)


def ChartRenderView(request):
    # get the url params from axios request
    patient = request.GET.get('userVal')
    selected_problems = request.GET.get('probVal')
    start_date_range = request.GET.get('startDate')
    end_date_range = request.GET.get('endDate')

    patient_problems = request.GET.get('problems')
    rates = request.GET.get('rates')
    pts = request.GET.get('patients')
    dates = request.GET.get('dates')

    list_patient_problems = list(patient_problems.split(","))
    list_rates = list(rates.split(","))
    list_pts = list(pts.split(","))
    list_dates = list(dates.split(","))

    # print(patient)
    # print(selected_problems)
    # print(start_date_range)
    # print(end_date_range)
    # print(list_patient_problems)
    # print(list_rates)
    # print(list_pts)
    # print(list_dates)

    df = pd.DataFrame()
    df['patient'] = list_pts
    df['problem'] = list_patient_problems
    df['rates'] = list_rates
    df['dates'] = list_dates
    new_df = df[df.patient == patient]
    new_df = new_df[new_df.dates >= start_date_range]
    new_df = new_df[new_df.dates <= end_date_range]
    print()
    print(new_df)
    print()
    # context
    context = {'data': False, 'model': request.GET.get('model')}
    if request.GET.get('model') == 'sleep-problems':
        context['model_name'] = 'Sleep Problems'
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
    if request.GET.get('model') == 'heartRate-problems':
        context['model_name'] = 'Heart Rate Problems'
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
    if request.GET.get('model') == 'movement-problems':
        context['model_name'] = 'Movement Problems'
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
