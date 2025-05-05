## 1. Create and InSert Database PostgreSQL
```
create database name:  spotify
insert data
```
## 2. Setup and Run
### Step 1:
```python
py -m venv venv
```
### Step 2:
```python
source venv/Scripts/activate
```
### Step 3:
```python
pip install -r requirements.txt
```
### Step 4:
```python
python manage.py runserver
```
## 3. Migrate
### Make Migrate:
```python
python manage.py makemigrations
```
### Migrate:
```python
python manage.py migrate
```
