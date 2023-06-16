# check-bandwidth-hls
Service that checks accordance of the given bandwith in master playlist with actual bandwidth of segments in corresponding variant playlist

To use the service you need to build image and start the container. Here are examples of the commands:

```docker build -t check-bandwidth .```

```docker run -d -p 5000:5000 --name check-bandwidth-service check-bandwidth```

Service will be ready to use at http://localhost:5000
You can set one or more URLs of hls video that you want to check.
Then press 'Submit', now service started to compare given bandwith from master playlist with actual bandwith of all chunks in corresponding variant playlist. You will see all incongruities in results form When it's done you'll see 'Done!' in the bottom of results. If there are no incongruities, you'll see only 'Done!' in results field.
