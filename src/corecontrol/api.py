from .models import ApiKey
import twitter

api = None

api_url = 'https://api.twitter.com/1.1'

endpoints = {
    'user': '%s/users/show.json' % api_url,
    'tweets': '%s/search/tweets.json' % api_url,
    'timelines': '%s/user_timeline.json' % api_url,
    'retweets': '%s/user_timeline.json' % api_url
}


def get_active_api(set_api=0, endpoint=None):
    objects = ApiKey.objects.all()
    global api
    if not api:
        set_active_api(objects[set_api])
    if endpoint:
        for obj in objects:
            if set_active_api(
                    obj,
                    check_endpoint=True,
                    endpoint=endpoints[endpoint] if endpoints.get(endpoint) else endpoint
            ):
                return api
        return False
    return api


def set_active_api(obj, check_endpoint=False, endpoint=None):
    global api
    api = twitter.Api(
        obj.consumer_key,
        obj.consumer_secret,
        obj.api_key,
        obj.api_secret,
        sleep_on_rate_limit=False
    )
    if check_endpoint:
        if api.CheckRateLimit(endpoint) <= 1:
            return False
        return True
