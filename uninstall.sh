if docker stop taxi_analytics_service 2> /dev/null && docker rm taxi_analytics_service 2> /dev/null;
then
    echo "stopped and removed taxi analytics service"
else
    sudo docker stop taxi_analytics_service && sudo docker rm taxi_analytics_service
    fi
