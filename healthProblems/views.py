from django.shortcuts import render
import pandas as pd


def index(request):
    context = {}
    return render(request, "healthProblems/index.html", context)


def ChartRenderView(request):
    # get the url params from axios request
    patient = request.GET.get('userVal')
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

    df = pd.DataFrame()
    df['patient'] = list_pts
    df['problem'] = list_patient_problems
    df['rates'] = list_rates
    df['dates'] = list_dates
    clean_df = df[df.patient == patient]
    clean_df = clean_df[clean_df.dates >= start_date_range]
    clean_df = clean_df[clean_df.dates <= end_date_range]

    unique_dates = set(clean_df['dates'])
    list_unique_dates = list(unique_dates)
    list_unique_dates.sort()

    sleep_df = clean_df[clean_df.problem == 'TooMuchSleepProblem']
    sleep_df = sleep_df.append(clean_df[clean_df.problem == 'LackOfSleepProblem'])
    sleep_df = sleep_df.append(clean_df[clean_df.problem == 'LowSleepQualityProblem'])
    hr_df = clean_df[clean_df.problem == 'LowHeartRateProblem']
    movement_df = clean_df[clean_df.problem == 'LackOfMovementProblem']
    # context
    context = {'data': False, 'model': request.GET.get('model')}
    print("Unique dates: ", list_unique_dates)
    if request.GET.get('model') == 'sleep-problems':
        print(sleep_df)
        context['model_name'] = 'Sleep Problems'
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
    if request.GET.get('model') == 'heartRate-problems':
        print(hr_df)
        context['model_name'] = 'Heart Rate Problems'
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
    if request.GET.get('model') == 'movement-problems':
        print(movement_df)
        context['model_name'] = 'Movement Problems'
        context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
