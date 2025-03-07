# Tropical Cyclones

Tropical Cyclones Severity Prediction.

## Installation specifics for the backend

To create a .env file at the root of the project to store Django's secret key:

```echo "DJANGO_SECRET_KEY=value" > .env```

To replace the word value with the proper secret key, please contact Vincent for approval.

## Start the backend (Django)

Remain at the root of the project "Tropical cyclones".

If there are migrations necessary:

```python web_app/manage.py makemigrations```

```python web_app/manage.py migrate```

Use this command to start the server:

```python web_app/manage.py runserver```

## Resources

### Dataset

- IBTrACS [dataset](https://www.ncei.noaa.gov/products/international-best-track-archive) from the National Centers for Environmental Information [(NOAA)](https://www.ncei.noaa.gov/)
