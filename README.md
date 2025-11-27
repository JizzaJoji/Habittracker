Habittracker – README
■ Project Overview
Habittracker is a Django-based habit tracking application designed to help users build better routines, stay consistent, and analyse personal progress.
---
 ■ Features
 ✔ Core Features - Create habits with:
-	Name
-	Frequency (daily / weekly)
-	Category (health, work, learning, personal)
-	Start date
-	Track progress with check-ins or notes- View analytics including:
-	Streaks
-	Success rate
-	Best day of the week
-	Weekly summary
-	Categorize habits for better organization
■ UI / Frontend Features
-	Responsive Bootstrap layout
-	Dashboard with filters & search
-	Habit detail pages
-	Modern card-based interface
■■ Setup Steps
1 ■■ Clone the Repository
```
git clone https://github.com/JizzaJoji/Habittracker.git cd habits-tracker
```
2 ■■ Create and Activate Virtual Environment
```
python -m venv env env\Scripts\activate 
```
3 ■■ Apply Database Migrations
```
python manage.py makemigrations python manage.py migrate
```
4■■ Start the Development Server
```
python manage.py runserver
```	
Now open the browser at: http://127.0.0.1:8000/
---

