# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models


# Users Manager
class UserManager(models.Manager):
    def get_or_retrieve(self, uid):
        # Busca un usuario en la base, y si no lo tenemos lo trae de Twitter
        # Habitualmente los tweets vienen con el objecto usuario - Este metodo es para cargar alternativas
        exists = self.filter(id=uid).exists()
        if exists:
            user = self.objects.filter(id=uid).get()
        elif not exists:
            user = User()
            from corecontrol.api import get_active_api
            from datetime import datetime
            api = get_active_api(endpoint='user')
            for k, v in list(api.GetUser(user_id=uid).AsDict().items()):
                if k == 'created_at':
                    user.created_at = datetime.strptime(v, '%a %b %d %H:%M:%S +0000 %Y')
                elif hasattr(user, k):
                    user.u_k = v
            user.save()
        return user


# Status Manager
class StatusManager(models.Manager):
    def get_or_retrieve(self, sid):
    # Busca un status en la base y si no lo tenemos lo trae de twitter
    # Util para los "quoted_status_id" y "in_reply_to_status_id"
        exists = self.filter(id=sid).exists()
        if exists:
            status = self.objects.filter(id=sid).get()
        else:
            status = Status()

            from corecontrol.api import get_active_api

            api = get_active_api(endpoint='tweets')
            obj = api.GetStatus(status_id=sid).AsDict()
            status.parse(obj)

        return status


# Users Model
class User(models.Model):
    objects = UserManager()

    contributors_enabled = models.BooleanField(blank=True, default=False)
    created_at = models.DateTimeField()
    default_profile = models.BooleanField(blank=True, default=False)
    default_profile_image = models.BooleanField(blank=True, default=False)
    description = models.TextField(null=True)
    entities = JSONField(null=True, blank=True, default=None)
    favourites_count = models.BigIntegerField(blank=True, default=0)
    followers_count = models.BigIntegerField(blank=True, default=0)
    friends_count = models.BigIntegerField(blank=True, default=0)
    geo_enabled = models.BooleanField(blank=True, default=False)
    id = models.BigIntegerField(primary_key=True)
    id_str = models.CharField(max_length=64)
    is_translator = models.BooleanField(blank=True, default=False)
    lang = models.CharField(max_length=10, default='none')
    listed_count = models.BigIntegerField(null=True, default=0)
    location = models.CharField(max_length=100, null=True, blank=True, default=None)
    name = models.CharField(max_length=100)
    profile_background_color = models.CharField(max_length=8, null=True, blank=True, default=None)
    profile_background_image_url = models.CharField(max_length=250, null=True, blank=True, default=None)
    profile_background_image_url_https = models.CharField(max_length=250, null=True, blank=True, default=None)
    profile_background_tile = models.BooleanField(blank=True, default=False)
    profile_banner_url = models.CharField(max_length=250, null=True, blank=True, default=None)
    profile_banner_image_url = models.CharField(max_length=250, null=True, blank=True, default=None)
    profile_banner_image_url_https = models.CharField(max_length=250, null=True, blank=True, default=None)
    profile_link_color = models.CharField(max_length=8, null=True, blank=True, default=None)
    profile_sidebar_border_color = models.CharField(max_length=8, null=True, blank=True, default=None)
    profile_sidebar_fill_color = models.CharField(max_length=8, null=True, blank=True, default=None)
    profile_text_color = models.CharField(max_length=8, null=True, blank=True, default=None)
    profile_use_background_image = models.BooleanField(blank=True, default=False)
    protected = models.BooleanField(blank=True, default=False)
    screen_name = models.CharField(max_length=25)
    statuses_count = models.IntegerField(blank=True, default=0)
    time_zone = models.CharField(max_length=50, null=True, blank=True, default=None)
    url = models.CharField(max_length=200, null=True, blank=True, default=None)
    utc_offset = models.IntegerField(null=True, blank=True, default=None)
    verified = models.BooleanField(blank=True, default=False)
    withheld_in_countries = models.CharField(max_length=50, null=True, blank=True, default=None)
    withheld_scope = models.CharField(max_length=20, null=True, blank=True, default=None)

    def parse_dict(self, obj, *args, **kwargs):
        from dateutil.parser import parse

        for k, v in list(obj.items()):
            if k == 'created_at':
                self.created_at = parse(v)
            elif hasattr(self, k):
                setattr(self, k, v)

        self.save()

        return self

    class Meta:
        app_label = 'twistreapy'


# Status Object (Tweets)
class Status(models.Model):
    objects = StatusManager()
    
    coordinates = JSONField(null=True)
    created_at = models.DateTimeField()
    deleted = models.BooleanField(blank=True, default=False)
    entities = JSONField(null=True)
    favorite_count = models.BigIntegerField(default=0)
    filter_level = models.CharField(max_length=50, default='none')
    hashtags = JSONField(null=True)
    id = models.BigIntegerField(primary_key=True)
    id_str = models.CharField(max_length=64)
    in_reply_to_screen_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    in_reply_to_status_id = models.BigIntegerField(null=True, blank=True, default=None)
    in_reply_to_user_id = models.BigIntegerField(null=True, blank=True, default=None)
    in_reply_to_user_id_str = models.BigIntegerField(null=True, blank=True, default=None)
    lang = models.CharField(max_length=20, null=True, blank=True, default=None)
    media = JSONField(null=True)
    place = JSONField(null=True, blank=True, default=None)
    possibly_sensitive = models.BooleanField(blank=True, default=False)
    quoted_status_id = models.BigIntegerField(blank=True, null=True, default=None)
    # = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    scopes = JSONField(null=True, blank=True, default=None)
    retweet_count = models.BigIntegerField(default=0)
    source = models.TextField(null=True, blank=True, default=None)
    text = models.TextField()
    truncated = models.BooleanField(blank=True, default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_json = JSONField(null=True)
    user_mentions = JSONField(null=True)
    urls = JSONField(null=True)
    withheld_copyright = models.BooleanField(blank=True, default=False)
    withheld_in_countries = JSONField(null=True, blank=True, default=None)
    withheld_scope = models.CharField(max_length=50, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if self.user_id:
            self.proc_user()

        super(Status, self).save(*args, **kwargs)

        self.parse_entities()

    def parse_dict(self, obj, *args, **kwargs):
        from dateutil.parser import parse

        for k, v in list(obj.items()):
            if k == 'created_at':
                self.created_at = parse(v)
            elif k == 'user':
                setattr(self, 'user_json', v)
                setattr(self, 'user_id', v.get('id'))
            elif hasattr(self, k):
                setattr(self, k, v)

        self.save()

        return self

    def proc_user(self):
        if User.objects.filter(id=self.user_id).exists():
            self.user = User.objects.filter(id=self.user_id).get()
        else:
            if self.user_json is not None:
                self.user = User().parse_dict(self.user_json)
            else:
                self.user = User.objects.get_or_retrieve(uid=self.user_id)

    def parse_entities(self):
        if self.entities is not None:
            pass
        if self.hashtags is not None:
            self.insert_hashtags()
        if self.user_mentions is not None:
            self.insert_user_mentions()
        if self.media is not None:
            self.insert_media()
        if self.urls is not None:
            self.insert_urls()

    def insert_hashtags(self):
        for ht in self.hashtags:
            Hashtag.objects.get_or_create(
                status=self,
                text=ht.get('text'),
                indices=ht.get('indices', None)
            )

    def insert_user_mentions(self):
        for um in self.user_mentions:
            UserMention.objects.get_or_create(
                status=self,
                user_id=um['id'],
                indices=um.get('indices', None),
                name=um['name'],
                screen_name=um['screen_name']
            )

    def insert_urls(self):
        for ur in self.urls:
            URL.objects.get_or_create(
                status=self,
                display_url=ur.get('display_url', None),
                expanded_url=ur.get('expanded_url', None),
                indices=ur.get('indices', None),
                url=ur.get('url', None)
            )

    def insert_media(self):
        for me in self.media:
            MediaEntity.objects.get_or_create(
                status=self,
                display_url=me.get('display_url', None),
                expanded_url=me.get('expanded_url', None),
                id=me.get('id'),
                id_str=me.get('id_str'),
                indices=me.get('indices', None),
                ext_alt_text=me.get('ext_alt_text', None),
                media_url=me.get('media_url', None),
                media_url_https=me.get('media_url_https', None),
                sizes=me.get('sizes', None),
                source_status_id=me.get('source_status_id', None),
                source_status_id_str=me.get('source_status_id_str', None),
                type=me.get('type', None),
                url=me.get('url', None)
            )

    class Meta:
        app_label = 'twistreapy'


# Entities
# Hashtags
class Hashtag(models.Model):
    indices = JSONField(null=True)
    text = models.CharField(max_length=90, db_index=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        app_label = 'twistreapy'


# Media
class MediaEntity(models.Model):
    display_url = models.CharField(max_length=90, blank=True, null=True, default=None)
    expanded_url = models.CharField(max_length=250, blank=True, null=True, default=None)
    id = models.BigIntegerField(primary_key=True)
    id_str = models.CharField(max_length=64)
    indices = JSONField(null=True)
    ext_alt_text = models.CharField(max_length=250, null=True, blank=True, default=None)
    media_url = models.CharField(max_length=250, blank=True, null=True, default=None)
    media_url_https = models.CharField(max_length=250, blank=True, null=True, default=None)
    sizes = JSONField(null=True)
    source_status_id = models.BigIntegerField(blank=True, null=True, default=None)
    source_status_id_str = models.CharField(max_length=64, blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, default='none')
    url = models.CharField(max_length=90, blank=True, null=True, default=None)

    class Meta:
        app_label = 'twistreapy'


# URLS
class URL(models.Model):
    display_url = models.CharField(max_length=250, null=True, blank=True, default=None)
    expanded_url = models.CharField(max_length=250, null=True, blank=True, default=None)
    indices = JSONField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    url = models.CharField(max_length=90, null=True, blank=True, default=None)

    class Meta:
        app_label = 'twistreapy'


# User Mentions
class UserMention(models.Model):
    user_id = models.BigIntegerField(db_index=True)
    indices = JSONField(null=True)
    name = models.CharField(max_length=50)
    screen_name = models.CharField(max_length=30)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        app_label = 'twistreapy'
