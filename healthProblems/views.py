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

    sleep_df1 = clean_df[clean_df.problem == 'TooMuchSleepProblem']
    sleep_df2 = clean_df[clean_df.problem == 'LackOfSleepProblem']
    sleep_df3 = clean_df[clean_df.problem == 'LowSleepQualityProblem']
    sleep_df3['rates'] = pd.to_numeric(sleep_df3['rates'], downcast="float") * 100
    sleep_df1 = sleep_df1.sort_values('dates')
    sleep_df2 = sleep_df2.sort_values('dates')
    sleep_df3 = sleep_df3.sort_values('dates')

    hr_df = clean_df[clean_df.problem == 'LowHeartRateProblem']
    movement_df = clean_df[clean_df.problem == 'LackOfMovementProblem']

    # context
    context = {'data': False, 'model': request.GET.get('model'), 'unique_dates': list_unique_dates}
    if request.GET.get('model') == 'sleep-problems':
        context['model_name'] = 'Sleep Problems'
        context['too_much_sleep'], has_data1 = set_prob_list(sleep_df1, list_unique_dates)
        context['lack_of_sleep'], has_data2 = set_prob_list(sleep_df2, list_unique_dates)
        context['low_quality'], has_data3 = set_prob_list(sleep_df3, list_unique_dates)
        if has_data1 or has_data2 or has_data3:
            context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
    if request.GET.get('model') == 'heartRate-problems':
        context['model_name'] = 'Heart Rate Problems'
        context['lowHR'], has_data = set_prob_list(hr_df, list_unique_dates)
        if has_data:
            context['data'] = True
        return render(request, "healthProblems/_chart.html", context)
    if request.GET.get('model') == 'movement-problems':
        context['model_name'] = 'Movement Problems'
        context['lackOfMovement'], has_data = set_prob_list(movement_df, list_unique_dates)
        print(len(context['lackOfMovement']))
        if has_data:
            context['data'] = True

        return render(request, "healthProblems/_chart.html", context)


def set_prob_list(df, unique_dates):
    problem = []
    has_data = False
    for i, date in enumerate(unique_dates):
        flag = True
        for df_date in df['dates']:
            if df_date == date:
                flag = False
                has_data = True
                temp = df.loc[df['dates'] == df_date, 'rates'].iloc[0]
                problem.append(temp)
        if flag:
            problem.append(0)
    return problem, has_data
