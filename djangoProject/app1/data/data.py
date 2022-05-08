import pandas as pd
import datetime
import random

traffic_df = pd.read_csv(
    './app1/data/traffic.csv')
healthy_df = pd.read_csv(
    './app1/data/healthy.csv')


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
    for n in suburbs:
        result[n] = [random.random() for _ in range(len(date_list))]

    return result, date_list


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
