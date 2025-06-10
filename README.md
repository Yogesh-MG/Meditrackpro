# MediTrackPros 
## Empowering health management with seamless tracking and organization.
### MediTrackPros is a web application designed to simplify medical record tracking, appointment scheduling, and medication management for patients and healthcare providers. Built with modern web technologies, it offers an intuitive interface and reliable performance, hosted on Netlify for fast and secure access.
Live Demo: <a href="https://meditrackpros.netlify.app">meditrackpros.netlify.app</a>

#### Run localy using below steps

Step 1
```bash
git clone https://github.com/Yogesh-MG/Meditrackpro
```
Step 2
```bash
cd Meditrackpro
```
Step 3
```bash
docker-compose build
```
Step 4
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```
Step 5
```bash
http://localhost
```
<p>Visit the step5 url in your browser</p>
