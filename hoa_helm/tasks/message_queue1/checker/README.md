# How to maintain this checker
* Python is required for local testing
  * PyCharm is recommended
* Run `docker build -t vovchello/checker-message_queue1 .` to update the image
* Run `kind load docker-image vovchello/checker-message_queue1:latest` for local testing in cluster
* Run `docker push vovchello/checker-message_queue1` to push image