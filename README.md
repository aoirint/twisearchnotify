# twisearchnotify

- Python 3.9

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

## run crawl

```shell
make run ARGS="--env-file=$(pwd)/.env -v=$(pwd)/config:/config -v=$(pwd)/data:/data"
```

## Update requirements

```shell
pip3 install pip-tools
pip-compile requirements.in
```
