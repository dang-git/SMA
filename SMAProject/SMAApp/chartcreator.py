def timeline_linechart(chartdata):
    """
    lineChart page
    """
    extra_serie = {"tooltip": {"y_start": "", "y_end": "Volume"}}        
    chartdata = {'x': chartdata["xdata"], 'name1': 'Volume', 'y1': chartdata["ydata"], 'kwargs1': { 'color': '#ef6c00' }, 'extra1' : extra_serie}
    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%b-%d %H:%m',
            'tag_script_js': True,
            'jquery_on_ready': False
		}
    }

    return data

def polarity_donutchart(chartdata):
    """
    pieChart page
    """
    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': chartdata["xdata"], 'y1': chartdata["ydata"], 'name1':'Tweets', 'extra1': extra_serie
    }
    charttype = "pieChart"
    chartcontainer = 'polarity_piechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
    			'donut':True,
            'donutRatio':0.5,
            'chart_attr':{
                'labelType':'\"percent\"',
            }
        }
    }
    return data

def sourcePiechartConverter(chartdata):
    """
    pieChart page
    """
    # {'Web Client': 393, 'Android': 669, 'iPhone': 670, 'Others': 929}
    # xdata = ["Web Client", "Android", "iPhone", "Others"]
    # ydata = [data["webClient"], data["android"], data["iPhone"], data["others"]]
    #ydata = [393, 669, 670, 929]
    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': chartdata["xdata"], 'y1': chartdata["ydata"], 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'source_piechart_container'

    data = {
        'chartcontainer': chartcontainer,
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'donut':True,
            'donutRatio':0.5,
            'chart_attr':{
                'labelType':'\"percent\"',
            }
        }
    }
    return data

def hashtag_horizontalBarChart(chartdata):
    #nb_element = 10
    xdata = [i["hashtag"] for i in chartdata]
    ydata = [i["count"] for i in chartdata] #[i + random.randint(-10, 10) for i in range(nb_element)]
    #ydata2 = map(lambda x: x * 2, ydata)

    extra_serie = {"tooltip": {"y_start": "", "y_end": " tweets"}}
    
    chartdata = {
        'x': xdata,
        'name1': 'Tweets', 'y1': ydata, 'extra1': extra_serie
    }

    charttype = "multiBarHorizontalChart"
    chartcontainer = 'multibarhorizontalchart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
			'margin_left' : 120
        }
		
    }
    return data

def compositionPiechartConverter(chartdata):
    """
    pieChart page
    """
    
    #xdata = ["Retweet", "Original", "Reply"]
    #ydata = [1307,950,316]
    #ydata = [data["retweet"], data["original"], data["reply"]]

    extra_serie = {"tooltip": {"y_start": "", "y_end": ""}}
    chartdata = {'x': chartdata["xdata"], 'y1': chartdata["ydata"], 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'composition_piechart_container'

    data = {
        'chartcontainer': chartcontainer,
        'charttype': charttype,
        'chartdata': chartdata,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'donut':True,
            'donutRatio':0.5,
            'chart_attr':{
                'labelType':'\"percent\"',
            }
        }
    }
    return data