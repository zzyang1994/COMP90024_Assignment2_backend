import pandas as pd
import datetime
import random
import couchdb
import json
import shapely.wkt

with open(
        '/Users/messifr/Desktop/Messi/MasterY1S1/CCC/django/COMP90024_Assignment2_backend/djangoProject/app1/data/config.json',
        'r') as f:
    configs = json.load(f)
    URL_Traffic = configs['url_traffic_live']
    URL_Healthy = configs['url_healthy_live']
    Traffic_database_name = configs['traffic_db_name_live']
    Healthy_database_name = configs['healthy_db_name_live']

    URL_Traffic_H = configs['url_traffic_live']
    URL_Healthy_H = configs['url_healthy_live']
    Traffic_database_name_H = configs['traffic_db_name_historical']
    Healthy_database_name_H = configs['healthy_db_name_historical']

db_traffic = couchdb.Server(URL_Traffic)[Traffic_database_name]
db_healthy = couchdb.Server(URL_Healthy)[Healthy_database_name]


def suburbs():
    """
    get the suburb names in Melbourne
    """

    return [suburb.key for suburb in db_traffic.view('suburbs/get_city', group=True)]
    # return traffic_df['lga_name11'].to_list()


def get_pie_chart_traffic(indicator):
    """
    get the tweet count for every suburb dividing by indicator of traffic
    """
    query_by = "q1"
    if indicator == "congestion":
        query_by = "q1"
    elif indicator == "crash_rate":
        query_by = "q2"
    elif indicator == "accessible_station":
        query_by = "q3"

    PIE_DATA = []

    for row in db_traffic.view('tweet_count_by_indicator/indicator', group_level=2):
        key = row.key
        if key[1] == query_by:
            PIE_DATA.append([row.value, row.key[0]])

    return sorted(PIE_DATA, key=lambda item: item[0], reverse=True)[:10]


# exit(0)


def get_pie_chart_healthy(indicator):
    """
    get the tweet count for every suburb dividing by indicator of healthy
    """
    query_by = "q1"
    if indicator == "smoking":
        query_by = "q1"
    elif indicator == "obesity":
        query_by = "q2"
    elif indicator == "exercise":
        query_by = "q3"
    elif indicator == "disease":
        query_by = "q4"

    PIE_DATA = []

    for row in db_healthy.view('tweet_count_by_indicator/indicator', group_level=2):
        key = row.key
        if key[1] == query_by:
            PIE_DATA.append([row.value, row.key[0]])

    return sorted(PIE_DATA, key=lambda item: item[0], reverse=True)[:10]


def get_date(year, month, day):
    '''
    get the datetime type variable from year(string), month(abbr string), day(string)
    '''
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = datetime_object.month
    return datetime.datetime(day=int(day), month=month_number, year=int(year))


def suburb_line_data(suburbs_list, time='Live'):
    """
    get the daily tweet counts of suburbs
    """

    if time == 'Historical':
        print(URL_Traffic_H, URL_Healthy_H, Traffic_database_name_H, Healthy_database_name_H)
        db_traffic_H = couchdb.Server(URL_Traffic_H)[Traffic_database_name_H]
        db_healthy_H = couchdb.Server(URL_Healthy_H)[Healthy_database_name_H]

        try:
            view_result_tr = db_traffic_H.view('daily_count/daily', group=True)
        except:
            view_result_tr = []
            print("traffic error")
        try:
            view_result_he = db_healthy_H.view('daily_count/daily', group=True)
        except:
            view_result_he = []
            print("healthy error")
    else:
        view_result_tr = db_traffic.view('daily_count/daily', group=True)
        view_result_he = db_healthy.view('daily_count/daily', group=True)

    date_list_timeStamp = []
    result = {}

    # print(view_result_he, view_result_tr)

    for row in view_result_tr:
        sub = row.key[0]
        if sub in suburbs_list:
            year = row.key[1]
            month = row.key[2]
            day = row.key[3]
            date = get_date(year, month, day)

            if sub in suburbs_list:
                if sub in result:
                    result[sub].append([date, row.value])
                else:
                    result[sub] = []

    for row in view_result_he:
        # print(row)
        sub = row.key[0]
        if sub in suburbs_list:
            year = row.key[1]
            month = row.key[2]
            day = row.key[3]
            date = get_date(year, month, day)

            if sub in suburbs_list:
                for i in range(len(result[sub])):
                    if date == result[sub][i][0]:
                        result[sub][i][1] += row.value

    for sub in result:
        data = result[sub]
        sorted_data = sorted(data, key=lambda item: item[0])
        result[sub] = sorted_data

        if date_list_timeStamp == []:
            date_list_timeStamp = [i[0].strftime("%Y-%m-%d") for i in sorted_data]

        result[sub] = [i[1] for i in sorted_data]

    return result, date_list_timeStamp


def suburb_wordcloud_data(suburb_list):
    result = {}

    for row in db_traffic.view('text/textDetail', group=True):
        # print(row)
        if row.key[0] in suburb_list:
            if row.key[1] in result:
                result[row.key[1]] += row.value
            else:
                result[row.key[1]] = row.value

    # for key in words.keys():
    #     tmp = {"value": key, "count": words[key]}
    #     result.append(tmp)
    #     sum_ += 1
    #     if sum_ > 60:
    #         break
    # print(result)
    sorted_result = sorted([{"value": i, "count": result[i]} for i in result], key=lambda item: item["count"],
                           reverse=True)
    # print(len(sorted_result))
    return sorted_result[:200]


def get_fields(aspect):
    # return traffic_df['lga_name11'].to_list()
    if aspect == "traffic":
        return ['congestion', 'crash_rate', 'accessible_station']

    if aspect == "healthy":
        return ['smoking', 'obesity', 'exercise', 'disease']


def get_bar_chart_traffic():
    BAR_DATA = {"congestion": [], "crash_rate": [], "accessible_station": []}
    query = ['q1', 'q2', 'q3']
    data = {}

    for row in db_traffic.view('tweet_count_by_indicator/indicator', group_level=2):
        key = row.key
        if key[0] == "Melbourne":
            continue

        if key[0] not in data:
            data[key[0]] = {'q1': 0, 'q2': 0, 'q3': 0}

        data[key[0]][key[1]] += row.value

    for sub in data:
        for i in query:
            if i == 'q1':
                BAR_DATA['congestion'].append(data[sub][i])
            elif i == 'q2':
                BAR_DATA['crash_rate'].append(data[sub][i])
            elif i == 'q3':
                BAR_DATA['accessible_station'].append(data[sub][i])

    suburbs = [i for i in data.keys()]
    return suburbs, [{i: BAR_DATA[i]} for i in BAR_DATA]


def get_bar_chart_healthy():
    BAR_DATA = {"smoking": [], "obesity": [], "exercise": [], "disease": []}
    query = ['q1', 'q2', 'q3', 'q4']
    data = {}

    for row in db_healthy.view('tweet_count_by_indicator/indicator', group_level=2):
        key = row.key
        if key[0] == "Melbourne":
            continue
        if key[0] not in data:
            data[key[0]] = {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0}

        data[key[0]][key[1]] += row.value

    for sub in data:
        for i in query:
            if i == 'q1':
                BAR_DATA['smoking'].append(data[sub][i])
            elif i == 'q2':
                BAR_DATA['obesity'].append(data[sub][i])
            elif i == 'q3':
                BAR_DATA['exercise'].append(data[sub][i])
            elif i == 'q4':
                BAR_DATA['disease'].append(data[sub][i])

    suburbs = [i for i in data.keys()]
    return suburbs, [{i: BAR_DATA[i]} for i in BAR_DATA]


def get_map_data():
    data = {
        "fields": [
            {"name": "time", "format": "yyyy-MM-dd", "type": "timestamp"},
            {"name": "lat", "format": "", "type": "real"},
            {"name": "long", "format": "", "type": "real"},
            {"name": "importance", "format": "", "type": "real"},
            {"name": "sentiment", "format": "", "type": "real"},
        ],
        "rows": []
    }

    for row in db_healthy.view('tweets/info'):
        longitude, latitude = row.key
        importance, sentiment, year, month, day = row.value

        date = get_date(year, month, day).strftime("%Y-%m-%d")

        tmp = [date, latitude, longitude, importance, sentiment]

        data['rows'].append(tmp)

    return data


def get_map_geoData():
    df = pd.read_csv("/Users/messifr/Desktop/Messi/MasterY1S1/CCC/django/COMP90024_Assignment2_backend/djangoProject/app1/data/suburbs_geometry.csv")

    data = {
        "fields": [
            {"name": "name", "format": "", "type": "string"},
            {"name": "geometry", "format": "", "type": "geometry"},
            {"name": "count", "format": "", "type": "real"},
            {"name": "importance", "format": "", "type": "real"},
            {"name": "sentiment", "format": "", "type": "real"},
        ],
        "rows": []
    }

    for row in db_healthy.view('tweets_geo/info', group=True):

        count, importance, sentiment = row.value

        geometry = df.loc[df['lga_name11'] == row.key]['geometry'].to_list()[0]

        tmp = [row.key, geometry, count, importance, sentiment]

        data['rows'].append(tmp)

    return data
