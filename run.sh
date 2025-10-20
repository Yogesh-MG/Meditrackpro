
echo "Running medical2 application..."


echo "Select an option:/n 1. web/n 2. mobile/n 3. Docker application"
read option
if [ "$option" = "1" ]; then
  echo "Starting web application..."
  ./web.sh
elif [ "$option" = "2" ]; then
  echo "Starting mobile application..."
  ./app.sh
elif [ "$option" = "3" ]; then
  echo "Starting Docker application..."
  docker build -t Dockerfile.Mtorch
  docker-compose build
  docker-compose up
  docker-compose exec backend python manage.py migrate
  docker-compose exec backend python manage.py createsuperuser
else
  echo "Invalid option. Please select either 1 or 2."
fi


