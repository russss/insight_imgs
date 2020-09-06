deploy:
	docker build . -t ghcr.io/russss/insight_imgs:latest
	docker push ghcr.io/russss/insight_imgs:latest
