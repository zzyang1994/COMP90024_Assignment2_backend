import pandas as pd
import datetime
import couchdb
import json

with open('./app1/data/config.json', 'r') as f:
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


def create_map_reduce(db, map_fun, reduce_fun, design_name, index_name):
    """
    create the map reduce to assigned couchdb
    """
    design = {'views': {
        f"{index_name}": {
            'map': map_fun,
            'reduce': reduce_fun
        }
    }}

    try:
        db[f"_design/{design_name}"] = design

    except:
        print('already exist')


def suburbs(time="Live"):
    """
    get the suburb names in Melbourne
    """
    map_fun = '''function(doc) {
        if (doc.city.match('Melbourne')) {
            emit(doc.suburb, 1);
        }
    }
    '''
    reduce_fun = "_count"
    design_name = "suburbs"
    index_name = "get_city"
    print("get suburbs from : ", time)
    if time == "historical":
        db_traffic_H = couchdb.Server(URL_Traffic_H)[Traffic_database_name_H]
        create_map_reduce(db_traffic_H, map_fun, reduce_fun, design_name, index_name)
        return [suburb.key for suburb in db_traffic_H.view('suburbs/get_city', group=True)]

    else:
        create_map_reduce(db_traffic, map_fun, reduce_fun, design_name, index_name)
        return [suburb.key for suburb in db_traffic.view('suburbs/get_city', group=True)]


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

    map_fun = '''function(doc) {
        if (doc.city.match('Melbourne') && doc['Related to']) {
            emit([doc.suburb, doc['Related to']], 1);
        }
    }
    '''
    reduce_fun = "_count"
    design_name = "tweet_count_by_indicator"
    index_name = "indicator"

    create_map_reduce(db_traffic, map_fun, reduce_fun, design_name, index_name)
    for row in db_traffic.view(f'{design_name}/{index_name}', group_level=2):
        key = row.key
        if key[1] == query_by:
            PIE_DATA.append([row.value, row.key[0]])

    return sorted(PIE_DATA, key=lambda item: item[0], reverse=True)[:10]


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

    map_fun = '''function(doc) {
        if (doc.city.match('Melbourne') && doc['Related to']) {
            emit([doc.suburb, doc['Related to']], 1);
        }
    }
    '''
    reduce_fun = "_count"
    design_name = "tweet_count_by_indicator"
    index_name = "indicator"

    create_map_reduce(db_healthy, map_fun, reduce_fun, design_name, index_name)
    for row in db_healthy.view(f'{design_name}/{index_name}', group_level=2):
        key = row.key
        if key[1] == query_by:
            PIE_DATA.append([row.value, row.key[0]])

    return sorted(PIE_DATA, key=lambda item: item[0], reverse=True)[:10]


def get_date(year, month, day):
    """
    get the datetime type variable from year(string), month(abbr string), day(string)
    """
    datetime_object = datetime.datetime.strptime(month, "%b")
    month_number = datetime_object.month
    return datetime.datetime(day=int(day), month=month_number, year=int(year))


def suburb_line_data(suburbs_list, time='Live'):
    """
    get the daily tweet counts of suburbs
    """

    map_fun = '''function(doc) {
        emit([doc.suburb, doc.created_at_year, doc.created_at_month, doc.created_at_day], doc.importance);
    }
    '''
    reduce_fun = "_sum"
    design_name = "daily_count"
    index_name = "daily"

    if time == 'Historical':
        db_traffic_H = couchdb.Server(URL_Traffic_H)[Traffic_database_name_H]
        db_healthy_H = couchdb.Server(URL_Healthy_H)[Healthy_database_name_H]
        try:

            create_map_reduce(db_traffic_H, map_fun, reduce_fun, design_name, index_name)
            view_result_tr = db_traffic_H.view(f'{design_name}/{index_name}', group=True)
        except:
            view_result_tr = []
            print("get view from traffic historical error")
        try:
            create_map_reduce(db_healthy_H, map_fun, reduce_fun, design_name, index_name)
            view_result_he = db_healthy_H.view(f'{design_name}/{index_name}', group=True)
        except:
            view_result_he = []
            print("get view from healthy historical error")
    else:
        print("from live data")
        create_map_reduce(db_traffic, map_fun, reduce_fun, design_name, index_name)
        create_map_reduce(db_healthy, map_fun, reduce_fun, design_name, index_name)
        view_result_tr = db_traffic.view(f'{design_name}/{index_name}', group=True)
        view_result_he = db_healthy.view(f'{design_name}/{index_name}', group=True)

    date_list_timeStamp = []
    result = {}

    for row in view_result_tr:
        sub = row.key[0]

        if sub in suburbs_list:
            year = row.key[1]
            month = row.key[2]
            day = row.key[3]
            date = get_date(year, month, day)

            if sub in result:
                result[sub].append([date, row.value])
            else:
                result[sub] = [[date, row.value]]

    for row in view_result_he:
        sub = row.key[0]
        if sub in suburbs_list:
            year = row.key[1]
            month = row.key[2]
            day = row.key[3]
            date = get_date(year, month, day)

            for i in range(len(result[sub])):
                if date == result[sub][i][0]:
                    result[sub][i][1] += row.value

    for sub in result:
        data = result[sub]
        sorted_data = sorted(data, key=lambda item: item[0])
        result[sub] = sorted_data

        if not date_list_timeStamp:
            date_list_timeStamp = [i[0].strftime("%Y-%m-%d") for i in sorted_data]

        result[sub] = [i[1] for i in sorted_data]

    return result, date_list_timeStamp


def suburb_wordcloud_data(indicator):
    result = {}
    map_fun = '''function(doc) {
      var list = doc.text_cleaned.split(" ");
      list.map(v => {
        var n = v.replace(/[`:_.~!@#$%^&*() \+ =<>?"{}|, \/ ;'1234567890\\ [ \] ·~！@#￥%……&*（）—— \+ ={}|《》？：“”【】、；‘’，。、]/g,'');
        if (n.length > 4) {
          emit(n, 1); 
        }
      })
    }
    '''

    reduce_fun = "_count"
    design_name = "text"
    index_name = "textDetail"

    if indicator == "traffic":
        db_ = db_traffic
    else:
        db_ = db_healthy
    create_map_reduce(db_, map_fun, reduce_fun, design_name, index_name)

    for row in db_.view(f'{design_name}/{index_name}', group=True):

        if row.key in result:
            result[row.key] += row.value
        else:
            if row.key not in ['rt', 'pt', 'gun', 'nigga'] \
                    and (len(row.key) > 3):
                result[row.key] = row.value

    sorted_result = sorted([{"value": i, "count": result[i]} for i in result], key=lambda item: item["count"],
                           reverse=True)

    return sorted_result[:200]


def get_fields(aspect):
    if aspect == "traffic":
        return ['congestion', 'crash_rate', 'accessible_station']

    if aspect == "healthy":
        return ['smoking', 'obesity', 'exercise', 'disease']


def get_bar_chart_traffic():
    BAR_DATA = {"congestion": [], "crash_rate": [], "accessible_station": []}
    query = ['q1', 'q2', 'q3']
    data = {}

    map_fun = '''function(doc) {
        if (doc.city.match('Melbourne') && doc['Related to']) {
            emit([doc.suburb, doc['Related to']], 1);
        }
    }
    '''
    reduce_fun = "_count"
    design_name = "tweet_count_by_indicator"
    index_name = "indicator"

    create_map_reduce(db_traffic, map_fun, reduce_fun, design_name, index_name)
    for row in db_traffic.view(f'{design_name}/{index_name}', group_level=2):
        key = row.key
        if key[0] == "Melbourne":
            continue

        if key[0] not in data:
            data[key[0]] = {'q1': 0, 'q2': 0, 'q3': 0}

        if key[1] in ['q1', 'q2', 'q3']:
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
    query = ['q1', 'q2', 'q3', 'q4', 'q5']
    data = {}

    map_fun = '''function(doc) {
            if (doc.city.match('Melbourne') && doc['Related to']) {
                emit([doc.suburb, doc['Related to']], 1);
            }
        }
        '''
    reduce_fun = "_count"
    design_name = "tweet_count_by_indicator"
    index_name = "indicator"

    create_map_reduce(db_traffic, map_fun, reduce_fun, design_name, index_name)
    for row in db_healthy.view(f'{design_name}/{index_name}', group_level=2):
        key = row.key
        if key[0] == "Melbourne":
            continue
        if key[0] not in data:
            data[key[0]] = {'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0, 'q5': 0}

        if key[1] in ['q1', 'q2', 'q3', 'q4', 'q5']:
            data[key[0]][key[1]] += row.value

    for sub in data:
        for i in query:
            if i == 'q1':
                BAR_DATA['smoking'].append(data[sub][i])
            elif i == 'q2' or i == 'q3':
                BAR_DATA['obesity'].append(data[sub][i])
            elif i == 'q4':
                BAR_DATA['exercise'].append(data[sub][i])
            elif i == 'q5':
                BAR_DATA['disease'].append(data[sub][i])

    suburbs = [i for i in data.keys()]
    return suburbs, [{i: BAR_DATA[i]} for i in BAR_DATA]


def get_map_data():
    data = {
        "fields": [
            {"name": "lat", "format": "", "type": "real"},
            {"name": "long", "format": "", "type": "real"},
            {"name": "importance", "format": "", "type": "real"},
            {"name": "sentiment", "format": "", "type": "real"},
        ],
        "rows": []
    }

    map_fun = '''function(doc) {
        if (doc.longitude && doc.latitude) {
            emit([doc.longitude, doc.latitude], [doc.importance, doc.sentiments]);
        }
    }
    '''
    reduce_fun = "_sum"
    design_name = "tweets"
    index_name = "info"

    create_map_reduce(db_healthy, map_fun, reduce_fun, design_name, index_name)
    for row in db_healthy.view(f'{design_name}/{index_name}', group=True):

        try:
            longitude = row.key[0]
            latitude = row.key[1]

            importance = row.value[0]
            sentiment = row.value[1]

            tmp = [latitude, longitude, importance, sentiment]

            data['rows'].append(tmp)
            print(data)
        except:
            continue

    return data


def get_map_geoData():
    df = pd.read_csv("./app1/data/suburbs_geometry.csv")

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

    map_fun = '''function(doc) {
        emit(doc.suburb, [1, doc.importance, doc.sentiments]);
    }
    '''
    reduce_fun = "_sum"
    design_name = "tweets_geo"
    index_name = "info"

    create_map_reduce(db_healthy, map_fun, reduce_fun, design_name, index_name)
    for row in db_healthy.view(f'{design_name}/{index_name}', group=True):
        try:
            count, importance, sentiment = row.value
            print(row)

            geometry = df.loc[df['lga_name11'] == row.key]['geometry'].to_list()[0]

            tmp = [row.key, geometry, count, importance, sentiment]

            data['rows'].append(tmp)
        except:
            continue

    return data
