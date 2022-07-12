from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, parse_obj_as
load_dotenv()

import os
from pathlib import Path
DATA_ROOT = Path(os.environ['DATA_ROOT'])
CONFIG_ROOT = Path(os.environ['CONFIG_ROOT'])
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_SECRET = os.environ['OAUTH_SECRET']

import json
from urllib.parse import urlencode, urlparse
from urllib.request import urlopen
import tempfile
import time
from datetime import datetime, timezone
import requests
import yaml

from twitter import Twitter, OAuth, oauth_dance

class ConfigItem(BaseModel):
  query: str
  inpage_count: int
  discord_webhook_url: str

class DataItem(BaseModel):
  last_tweet_id: Optional[int] = None
  last_crawled_at: Optional[datetime] = None

config_paths = list(CONFIG_ROOT.glob('*.yml'))

for config_path in config_paths:
  config_obj = yaml.load(config_path.read_text(encoding='utf-8'), Loader=yaml.SafeLoader)
  config = parse_obj_as(ConfigItem, config_obj)

  config_name = config_path.stem
  print(f'[{config_name}]')

  data_path = DATA_ROOT / f'{config_name}.json'
  data_path.parent.mkdir(parents=True, exist_ok=True)

  data = DataItem()
  if data_path.exists():
    data = parse_obj_as(DataItem, json.loads(data_path.read_text(encoding='utf-8')))

  twitter = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

  data.last_crawled_at = datetime.now(timezone.utc)

  result = twitter.search.tweets(
    q=config.query,
    since_id=data.last_tweet_id,
    count=config.inpage_count,
    result_type='recent',
  )
  tweets = result['statuses']
  tweets_asc = sorted(tweets, key=lambda tweet: int(tweet['id']))

  for tweet in tweets_asc:
    tweet_id = str(tweet['id'])
    user_id = str(tweet['user']['id'])
    screen_name = tweet['user']['screen_name']

    tweet_url = f'https://twitter.com/{screen_name}/status/{tweet_id}'

    requests.post(config.discord_webhook_url, json={
      'content': f'{tweet_url}',
    })

  last_tweet = next(iter(sorted(tweets, key=lambda tweet: int(tweet['id']), reverse=True)), None)
  data.last_tweet_id = int(last_tweet['id']) if last_tweet is not None else None

  data_path.write_text(data.json(ensure_ascii=False), encoding='utf-8')
