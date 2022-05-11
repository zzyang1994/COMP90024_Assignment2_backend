import pandas as pd
import datetime
import random
from .wordCloudData import words

traffic_df = pd.read_csv(
    './app1/data/traffic.csv')
healthy_df = pd.read_csv(
    './app1/data/healthy.csv')

line_mock_data = [["2000-06-05", 116], ["2000-06-06", 129], ["2000-06-07", 135], ["2000-06-08", 86], ["2000-06-09", 73], ["2000-06-10", 85], ["2000-06-11", 73], ["2000-06-12", 68], ["2000-06-13", 92], ["2000-06-14", 130], ["2000-06-15", 245], ["2000-06-16", 139], ["2000-06-17", 115], ["2000-06-18", 111], ["2000-06-19", 309], ["2000-06-20", 206], ["2000-06-21", 137], ["2000-06-22", 128], ["2000-06-23", 85], ["2000-06-24", 94], ["2000-06-25", 71], ["2000-06-26", 106], ["2000-06-27", 84], ["2000-06-28", 93], ["2000-06-29", 85], ["2000-06-30", 73], ["2000-07-01", 83], ["2000-07-02", 125], ["2000-07-03", 107], ["2000-07-04", 82], ["2000-07-05", 44], ["2000-07-06", 72], ["2000-07-07", 106], ["2000-07-08", 107], ["2000-07-09", 66], ["2000-07-10", 91], ["2000-07-11", 92], ["2000-07-12", 113], ["2000-07-13", 107], ["2000-07-14", 131], ["2000-07-15", 111], ["2000-07-16", 64], ["2000-07-17", 69], ["2000-07-18", 88], ["2000-07-19", 77], ["2000-07-20", 83], ["2000-07-21", 111], ["2000-07-22", 57], ["2000-07-23", 55], ["2000-07-24", 60]];

def suburbs():
    return traffic_df['lga_name11'].to_list()


def get_pie_chart_traffic(indicator):
    tmp = traffic_df.sort_values(indicator, ascending=False).head(10)
    PIE_DATA = []
    for i in tmp.index:
        PIE_DATA.append([tmp.loc[i, indicator], tmp.loc[i, 'lga_name11']])

    return PIE_DATA


def get_pie_chart_healthy(indicator):
    tmp = healthy_df.sort_values(indicator, ascending=False).head(10)
    PIE_DATA = []
    for i in tmp.index:
        PIE_DATA.append([tmp.loc[i, indicator], tmp.loc[i, 'lga_name11']])

    return PIE_DATA

def suburb_line_data(suburbs):
    def date_range(beginDate, endDate):
        dates = []
        dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
        date = beginDate[:]
        while date <= endDate:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime("%Y-%m-%d")
        return dates

    date_list = date_range("2021-09-01", "2022-04-15")
    result = {}

    def get_mock_value(x):
        return x - random.randint(-20, 20)

    for n in suburbs:
        res = []
        j = 0
        for i in range(len(date_list)):
            if i % len(line_mock_data) == 0:
                j = 0
            res.append(get_mock_value(line_mock_data[j][1]))
            j += 1

        result[n] = res

    return result, date_list

def suburb_wordcloud_data(suburbs):

    result = []
    sum_ = 0
    for key in words.keys():
        tmp = {"value": key, "count": words[key]}
        result.append(tmp)
        sum_ += 1
        if sum_ > 60:
            break

    return result


def get_fields(aspect):
    # return traffic_df['lga_name11'].to_list()
    if (aspect == "traffic"):
        return ['congestion', 'crash_rate', 'accessible_station']

    if (aspect == "healthy"):
        return ['smoking', 'obesity', 'exercise', 'disease']


def get_bar_chart_traffic():
    fields = get_fields("traffic")
    BAR_DATA = []

    df = traffic_df.head(6)

    for field in fields:
        tmp = {field: df[field].to_list()}
        BAR_DATA.append((tmp))

    return df['lga_name11'].to_list(), BAR_DATA


def get_bar_chart_healthy():
    fields = get_fields("healthy")
    BAR_DATA = []

    df = healthy_df.head(6)

    for field in fields:
        tmp = {field: df[field].to_list()}
        BAR_DATA.append((tmp))

    return df['lga_name11'].to_list(), BAR_DATA


RADAR_DATA = [
    {
        "value": [4200, 3000, 20000, 35000, 50000, 18000],
        "name": 'Allocated Budget'
    },
    {
        "value": [5000, 14000, 28000, 26000, 42000, 21000],
        "name": 'Actual Spending'
    }
]

RADAR_INDICATOR = [
    {"name": 'Sales', "max": 6500},
    {"name": 'Administration', "max": 16000},
    {"name": 'Information Technology', "max": 30000},
    {"name": 'Customer Support', "max": 38000},
    {"name": 'Development', "max": 52000},
    {"name": 'Marketing', "max": 25000}
]

SUNBURST_DATA = [
    {
        "name": 'Grandpa',
        "children": [
            {
                "name": 'Uncle Leo',
                "value": 15,
                "children": [
                    {
                        "name": 'Cousin Jack',
                        "value": 2
                    },
                    {
                        "name": 'Cousin Mary',
                        "value": 5,
                        "children": [
                            {
                                "name": 'Jackson',
                                "value": 2
                            }
                        ]
                    },
                    {
                        "name": 'Cousin Ben',
                        "value": 4
                    }
                ]
            },
            {
                "name": 'Father',
                "value": 10,
                "children": [
                    {
                        "name": 'Me',
                        "value": 5
                    },
                    {
                        "name": 'Brother Peter',
                        "value": 1
                    }
                ]
            }
        ]
    }
]

MAP_DATA = {
    "fields": [
        {
            "name": "index",
            "format": "",
            "type": "real",
        },
        {
            "name": "time",
            "format": "yyyy-MM-dd HH:mm:ss",
            "type": "timestamp",
        },
        {
            "name": "friends_count",
            "format": "",
            "type": "real",
        },
        {
            "name": "lat",
            "format": "",
            "type": "real",
        },
        {
            "name": "long",
            "format": "",
            "type": "real",
        },
    ],
    "rows": [
        [
            0,
            "2014-07-28 16:58:48",
            148,
            -37.97935827,
            145.05330569,
        ],
        [
            1,
            "2014-07-28 16:59:43",
            112,
            -37.83740582,
            144.99653022,
        ],
    ],
}

