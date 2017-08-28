from .models import ApiKey
import twitter

api = None

api_url = 'https://api.twitter.com/1.1'

last_api = 0

endpoints = {
    'user': '%s/users/show.json' % api_url,
    'tweets': '%s/search/tweets.json' % api_url,
    'timelines': '%s/user_timeline.json' % api_url,
    'retweets': '%s/user_timeline.json' % api_url
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
        if api.CheckRateLimit(endpoint) <= 1:
            return False
        return True
