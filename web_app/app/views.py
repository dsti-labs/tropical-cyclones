import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from logger import logging
from app.models import Cyclone
from app.methods import classify, check_form_submit, populate_database

if not Cyclone.objects.exists():
    logging.debug("The database is empty")
    populate_database()


def index(request):

    return render(request, "index.html")


@csrf_exempt
def make_prediction(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)

            check_form_submit(data)

            # create new entry
            logging.debug("inserting new cyclone into the database")

            new_cyclone = Cyclone.objects.create(
                cyclone_id=data["cyclone_id"],
                season=datetime.strptime(data["season"], "%Y-%m-%d %H:%M:%S"),
                basin=data["basin"],
                nature=data["nature"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                wind=data["wind"],
                dist2land=data["dist2land"],
                storm_dir=data["storm_dir"],
                storm_speed=data["storm_speed"],
            )
            logging.debug("object created")

            # get the id to be able to update the cyclone entry later
            cyclone_id = new_cyclone.id
            logging.debug(f"cyclone {cyclone_id} inserted")

            # send data to the model to make a prediction
            result = classify(data)

            # update stage of the cyclone entry
            logging.debug(f"updating stage of cyclone {cyclone_id}")

            cyclone = Cyclone.objects.filter(id=cyclone_id).update(
                stage=result
            )

            logging.debug(f"cyclone {cyclone_id} updated")

            return JsonResponse(
                {"message": "Form submitted!", "data": cyclone, "status": 200}
            )
        return JsonResponse({"error": "Invalid request"}, status=400)

    except ValueError as error:
        return JsonResponse({"error": error}, status=400)


def display_most_recent_predictions(request, nb_predictions: int):
    try:
        # Get the n most recent unique cyclone IDs
        if nb_predictions > 1:
            logging.debug(
                f"fetching the last {str(nb_predictions)} cyclones in the database"
            )
        else:
            logging.debug("fetching the last cyclone in the database")

        recent_cyclone_ids = (
            Cyclone.objects.order_by("-timestamp")
            .values_list("cyclone_id", flat=True)
            .distinct()[:nb_predictions]
        )

        # Get all entries related to these cyclone IDs
        logging.debug("fetching all occurencies of the cyclones")

        latest_cyclones = Cyclone.objects.filter(
            cyclone_id__in=recent_cyclone_ids
        ).order_by("-timestamp")

        if latest_cyclones.exists():
            data = list(latest_cyclones.values())

            return JsonResponse(
                {"message": "Form submitted!", "data": data, "status": 200}
            )
        return JsonResponse({"error": "No data found"}, status=404)

    except ValueError as error:
        return JsonResponse({"error": error}, status=404)


def get_cyclone_by_id(request, value: str):

    logging.debug(f"fetching the cyclone with ID {value}")

    cyclones = Cyclone.objects.filter(cyclone_id=value)

    if cyclones.exists():
        data = list(cyclones.values())

        return JsonResponse(
            {"message": "Form submitted!", "data": data, "status": 200}
        )
    return JsonResponse({"error": "No data found"}, status=404)
