build:
	docker build -t twisearchnotify:latest .

run:
	docker run --rm $(ARGS) twisearchnotify:latest

authenticate:
	docker run --rm -it $(ARGS) twisearchnotify:latest gosu user python3 authenticate.py
