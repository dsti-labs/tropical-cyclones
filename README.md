# Tropical Cyclones

Tropical Cyclones Severity Prediction.

## Install

```pyenv install 3.13.1```

```pyenv global 3.13.1```

```pip install --upgrade pip```

- cd to the project's folder.

```python -m venv .venv```

```source /bin/activate/.venv (for Windows)```

```source .venv/bin/activate (for macOS)```

```pip install -r requirements.txt```

If the requirements install fails for any reason, install the packages manually:

```pip install jupyterlab numpy pandas plotly pyarrow scikit-learn django```

To create a .env file at the root of the project to store Django's secret key:

```echo "DJANGO_SECRET_KEY=value" > .env```

To replace the word value with the proper secret key, please contact Vincent for approval.

## Start the backend (Django)

If there are migrations necessary:

```python manage.py makemigrations```

```python manage.py migrate```

Use this command to start the server:

```python manage.py runserver```

## Resources

### Dataset

- IBTrACS [dataset](https://www.ncei.noaa.gov/products/international-best-track-archive) from the National Centers for Environmental Information [(NOAA)](https://www.ncei.noaa.gov/)
