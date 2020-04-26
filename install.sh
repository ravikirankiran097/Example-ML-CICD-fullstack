google_credentials=${1:-$GOOGLE_APPLICATION_CREDENTIALS}

cp "$google_credentials" google_secrets.json

if ! (docker build -t taxi_analytics . --build-arg google_credentials=google_secrets.json 2>/dev/null); then
  echo "Sudo is required"
  exit
fi

priorcontainer=$(docker container ls -a | grep taxi_analytics_service | cut -d" " -f 1)

[ -z "$priorcontainer" ] && to_remove=false || to_remove=true

if $to_remove; then
  echo "There exists another similar container previously run, stopping"

  stopped_container=$(docker container stop "$priorcontainer" &&
    docker container rm "$priorcontainer")
  echo "Stopped and removed container $stopped_container"
fi

if docker run -d -p 8080:8080 --name taxi_analytics_service taxi_analytics; then
  echo "Success, API service is now hosted on localhost:8080"
  echo "See specs at localhost:8080/specs.html"
else
  echo "Failed to start API service on localhost: 8080"
fi
