
echo "Running medical2 application..."

get_pi_ip() {
  hostname -I | awk '{print $1}'
}
PI_IP=$(get_pi_ip)
update_frontend_ip() {
  APP_API_CONFIG_PATH="app/src/utils/apiconfig.ts"
  FRONTEND_API_CONFIG_PATH="frontend/src/utils/apiconfig.ts"
  if [ -f "$APP_API_CONFIG_PATH"  ]; then
    echo "Updating API URL in $APP_API_CONFIG_PATH"
    sed -i "s|? \"https://twistar.pythonanywhere.com/\"|? \"http://$PI_IP:8000/\"|" "$CONFIG_FILE"
  fi
  if [ -f "$FRONTEND_API_CONFIG_PATH" ]; then
    echo "Updating API URL in $FRONTEND_API_CONFIG_PATH"
    sed -i "s|? \"https://twistar.pythonanywhere.com/\"|? \"http://$PI_IP/\"|" "$CONFIG_FILE"
  fi
}
update_frontend_ip
echo "Your IP address is: $(get_pi_ip)"
echo "Select an option:/n 1. web/n 2. mobile apk/n 3. Deploy application"
read option
if [ "$option" = "1" ]; then
  echo "Starting web application..."
  chmod +x web.sh
  ./web.sh
elif [ "$option" = "2" ]; then
  echo "Starting mobile application..."
  chmod +x app.sh
  ./app.sh
elif [ "$option" = "3" ]; then
  echo "Starting Docker application..."
  docker build -t mtorch:latest -f Dockerfile.Mtorch .
  docker-compose build
  docker-compose up
  docker-compose exec backend python manage.py migrate
  docker-compose exec backend python manage.py createsuperuser
else
  echo "Invalid option. Please select either 1 or 2."
fi


