# twisearchnotify

- Python 3.9

## Easy usage

```shell
mkdir -p ./config ./data

touch .env
echo "CONSUMER_KEY=..." >> .env
echo "CONSUMER_SECRET=..." >> .env

docker run --rm --env-file=$(pwd)/.env -v=$(pwd)/config:/config -v=$(pwd)/data:/data aoirint/twisearchnotify:latest gosu user python3 authenticate.py

echo "OAUTH_TOKEN=..." >> .env
echo "OAUTH_SECRET=..." >> .env

echo <<EOF > config/nhk_penguin.yml
query: 'from:nhk_news ペンギン'
inpage_count: 10
discord_webhook_url: https://discord.com/api/webhooks/...
EOF

docker run --rm --env-file=$(pwd)/.env -v=$(pwd)/config:/config -v=$(pwd)/data:/data aoirint/twisearchnotify:latest
```

For scheduled run, use external tools like cron.

## build docker image

```shell
make build
```

## create .env

- Copy `template.env` to `.env` and set values

## create twitter app

- <https://developer.twitter.com/en/portal/projects-and-apps>

Enable OAuth 1.0a and copy CONSUMER_KEY and CONSUMER_SECRET to your .env.

## run authenticate

```shell
make authenticate ARGS="--env-file=$(pwd)/.env"
```

Open printed URL in your browser and authorize your app.

Paste outputs (OAUTH_TOKEN, OAUTH_SECRET) to your .env.

## create ./config/nhk_penguin.yml

```yaml
query: 'from:nhk_news ペンギン'
inpage_count: 10
discord_webhook_url: https://discord.com/api/webhooks/...
```

## create ./data dir

## run crawl

```shell
make run ARGS="--env-file=$(pwd)/.env -v=$(pwd)/config:/config -v=$(pwd)/data:/data"
```

## Update requirements

```shell
pip3 install pip-tools
pip-compile requirements.in
```
