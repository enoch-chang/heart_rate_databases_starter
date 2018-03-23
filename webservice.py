""" A web app for heart rate data storage.

Users can create user profiles, add heart rate readings, retrieve information
from the database and obtain either the global or a specified interval average.
"""

from flask import Flask, jsonify, request
import pymodm
from pymodm import connect
from datetime import datetime
import main
import numpy as np
import logging

app = Flask(__name__)
connect("mongodb://localhost:27017/bme590")  # connect to database


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    """ Stores heart rate measurement for the user with the specified email

    :return:
    """

    set_up_logging()

    r = request.get_json()
    valid = check_input(r)

    if valid is True:
        try:
            main.add_heart_rate(r["user_email"],
                                r["heart_rate"], datetime.now())
            logging.info("Heart rate added to existing user.")
        except pymodm.errors.DoesNotExist:
            main.create_user(r["user_email"], r["user_age"], r["heart_rate"])
            logging.info("Heart rate added to new user.")

        user = {
                "message": "Heart rate successfully recorded.",
                "user_email": r["user_email"],
                "user_age": r["user_age"],
                "heart_rate": r["heart_rate"]
        }
    else:
        msg = "Invalid input."
        return msg, 400

    return jsonify(user), 201


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def rate_email(user_email):
    """ Returns all heart rate measurements for user with specified email

    :param user_email:
    :return:
    """

    set_up_logging()

    try:
        all_hr = main.print_user(user_email)

        result = {
            "user_email": user_email,
            "heart_rate": all_hr
        }
        logging.info("Data for requested user_email successfully retrieved!")
    except pymodm.errors.DoesNotExist:
        msg = "No data associated with the inputted user_email. "
        logging.error(msg)
        print(msg)
        return msg, 400

    return jsonify(result), 200


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def average_email(user_email):
    """ Returns average of all heart rate measurements for user with specified
    email

    :param user_email:
    :return:
    """

    set_up_logging()

    try:
        [hr, times] = main.return_all_hr(user_email)

        average_hr = calculate_average(hr)

        result = {
                "user_email": user_email,
                "average_hr": average_hr
        }

        logging.info("Data for requested user_email successfully retrieved!")

    except pymodm.errors.DoesNotExist:
        msg = "No data associated with the inputted user_email. "
        logging.error(msg)
        return msg, 400

    return jsonify(result), 200


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    """ Calculates and returns average heart rate for the user since time
    specified

    :return:
    """

    set_up_logging()

    r = request.get_json()
    email = r["user_email"]

    try:
        time = datetime.strptime(r["heart_rate_average_since"],
                                 "%Y-%m-%d %H:%M:%S.%f")
        logging.info("%s%s", "Time requested is valid: ", time)
    except ValueError:
        msg = "Time specified is of an invalid format. "
        logging.error(msg)
        print(msg)
        return msg, 400

    try:
        [hr, times] = main.return_all_hr(email)
        logging.info("Data for requested user_email successfully retrieved!")
    except pymodm.errors.DoesNotExist:
        msg = "No data associated with the inputted user_email. "
        logging.error(msg)
        print(msg)
        return msg, 400

    hr_since = []

    for n, t in enumerate(times):
        if t > time:
            hr_since.append(hr[n])

    average = calculate_average(hr_since)

    result = {
            "user_email": email,
            "Condition": diagnosis(average),
            "average_hr": average
    }

    return jsonify(result), 201


def check_input(r):
    """ Validates input heart rate data and returns information about input

    :return:
    """

    msg = "Data input is OK. "

    set_up_logging()

    try:
        if type(r["user_email"]) is not str:
            msg = "Invalid input. 'user_email' input must be a string. "
            print(msg)
            logging.error(msg)
            return False
    except KeyError:
        msg = "Invalid input. No input provided for 'user_email'. "
        print(msg)
        logging.error(msg)
        return False

    try:
        float(r["user_age"])
        if r["user_age"] > 120:
            logging.warning("Warning: Your age inputted is >120")
    except KeyError:
        msg = "Invalid input. No input provided for 'user_age'."
        print(msg)
        logging.error(msg)
        return False
    except ValueError:
        msg = "Invalid input. 'user_age' input must be a float. "
        print(msg)
        logging.error(msg)
        return False

    try:
        float(r["heart_rate"])
        if r["heart_rate"] > 200:
            logging.warning("Warning: Your heart rate input is >200")
    except KeyError:
        msg = "Invalid input. No input provided for 'heart_rate'."
        print(msg)
        logging.error(msg)
        return False
    except ValueError:
        msg = "Invalid input. 'heart_rate' input must be a float. "
        logging.error(msg)
        print(msg)
        return False

    print(msg)
    logging.info(msg)

    return True


def calculate_average(hr):
    """ Returns the average heart rate calculated from an input list

    :param hr: list of heart rates
    :return: average heart rate
    """

    if len(hr) is 1:
        logging.warning("Average is calculated for only one heart rate!")

    average = np.mean(hr)
    logging.info("Average heart rate calculated successfully.")
    return average


def diagnosis(hr):
    """ Returns a diagnosis based on the input heart rate - normal, tachycardic
    or bradycardic

    :param hr: heart rate
    :return: String with the condition
    """
    condition = "Normal"
    if hr > 100:
        condition = "Tachycardia"
        logging.warning("Patient has tachycardia.")
    if hr < 60:
        condition = "Bradycardia"
        logging.warning("Patient has bradycardia.")
    return condition


def set_up_logging():
    logging.basicConfig(filename='webservice.txt',
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)
    return


if __name__ == "__main__":
    app.run(host="127.0.0.1")
