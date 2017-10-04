from .models import ApiKey
import twitter

api = None

api_url = 'https://api.twitter.com/1.1'

last_api = 0

endpoints = {
    'user': '%s/users/show.json' % api_url,
    'tweets': '%s/search/tweets.json' % api_url,
    'timelines': '%s/user_timeline.json' % api_url,
    'retweets': '%s/user_timeline.json' % api_url,
    'lookup': '%s/statuses/lookup.json' % api_url
}


def get_active_api(set_api=0, endpoint=None):
    objects = ApiKey.objects.all()
    global api
    if not api and not endpoint:
        set_active_api(objects[set_api])
        return api
    if endpoint:
        global last_api
        for index, obj in list(enumerate(objects[last_api:])):
            if set_active_api(
                    obj,
                    check_endpoint=True,
                    endpoint=endpoints[endpoint] if endpoints.get(endpoint) else endpoint
            ):
                last_api = index
                return api
        last_api = 0
        get_active_api(set_api=set_api, endpoint=endpoint)


def set_active_api(obj, check_endpoint=False, endpoint=None):
    global api
    api = twitter.Api(
        obj.consumer_key,
        obj.consumer_secret,
        obj.api_key,
        obj.api_secret,
        sleep_on_rate_limit=True
    )
    if check_endpoint:
        try:
            api.CheckRateLimit(endpoint)
        except:
            return False
        else:
            return True


def statuses_lookup(
        ids,
        include_entities=True,
        trim_user=True,
        param_map=True,
        include_ext_alt_entities=True,
        set_api=None
):
    if not set_api:
        global api
    else:
        api = set_api
    if not api:
        return False
    url = '%s/statuses/lookup.json' % api.base_url

    parameters = {
        'id': ids,
        'include_entities': include_entities,
        'trim_user': trim_user,
        'map': param_map,
        'include_ext_alt_text': include_ext_alt_entities
    }

    resp = api._RequestUrl(url, 'GET', data=parameters)
    data = api._ParseAndCheckTwitter(resp.content.decode('utf-8'))

    return [twitter.Status.NewFromJsonDict(s) for s in data]