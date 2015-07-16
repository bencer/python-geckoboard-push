import urllib.request
import json

class Gecko(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def push(self, widget_key, data):
        payload = json.dumps({'api_key' : self.api_key, 'data' : data})
        DATA = bytes(payload, 'utf-8')
        req = urllib.request.Request(
           "https://push.geckoboard.com/v1/send/{:s}".format(widget_key),
           method='POST',
           data=DATA
        )
        res = urllib.request.urlopen(req)
        if not (res.getcode() == 200 and json.loads(res.read().decode('utf-8')).get('success') == True):
            raise ValueError(res.content)

    def number(self, widget_key, number1, number2=None):
        data = {'item' : []}
        if number1: data['item'].append({'value' : number1, 'text' : ''})
        if number2: data['item'].append({'value' : number2, 'text' : ''})
        return self.push(widget_key, data)

    def rag(self, widget_key, *items):
        data = {'item' : []}
        for item in items:
            data['item'].append({'value' : item[0], 'text' : item[1]})
        return self.push(widget_key, data)

    def line(self, widget_key, values, **kwargs):
        data = {'item' : [], 'settings' :kwargs}
        for item in values:
            data['item'].append(item)
        return self.push(widget_key, data)

    def text(self, widget_key, *texts):
        data = { "item" : [] }
        for text in texts:
            if isinstance(text, dict):
                data['item'].append(dict(text))
            else:
                data['item'].append({"text" : text, "type" : 0})
        return self.push(widget_key, data)

    def heartbeat(self, widget_key, utc=True, format="%H:%M / %d %b"):
        import datetime
        dt = (datetime.datetime.utcnow if utc else datetime.datetime.now)().strftime(format)
        return self.text(widget_key, dt)

    def beater(self, *args, **kwargs):
        return lambda: self.heartbeat(*args, **kwargs)

    def funnel(self, widget_key, phases):
        data = { "item" : [] }
        if isinstance(phases, dict):
            for k, v in phases.items():
                data['item'].append({"value" : v, "label" : k})
            data['item'].sort(key=lambda v: v['value'], reverse=True)
        else:
            for phase in phases:
                data['item'].append({"value" : phase, "label" : ""})
            data['item'].sort(reverse=True)
        return self.push(widget_key, data)

