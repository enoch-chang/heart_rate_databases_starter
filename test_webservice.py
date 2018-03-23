from webservice import calculate_average, diagnosis, check_input
import pytest
import math

def test_calculate_average():

    output_1 = calculate_average([10, 20, 30])
    assert output_1 == 20

    output_2 = calculate_average([50, 76, 82, 99, 43, 46, 76, 35])
    assert output_2 == 63.375


def test_diagnosis():

    output_3 = diagnosis(120)
    assert output_3 == "Tachycardia"

    output_4 = diagnosis(100)
    assert output_4 == "Normal"

    output_5 = diagnosis(61)
    assert output_5 == "Normal"

    output_6 = diagnosis(45)
    assert output_6 == "Bradycardia"

def check_input():

    input_7 = {
                "user_email": "suyash@suyashkumar.com",
                "user_age": 50,
                "heart_rate": 100
    }

    output_7 = check_input(input_7)
    assert output_7 is True

    input_8 = {
                "user_email": "suyash@suyashkumar.com",
                "user_age": "50",
                "heart_rate": "100"
    }

    output_8 = check_input(input_8)
    assert output_8 is True


    input_9 = {
        "user_age": 50,
        "heart_rate": 100
    }

    with pytest.raises(KeyError):
        output_9 = check_input(input_9)

    assert output_9 is False

    input_10 = {
                "user_email": 45,
                "user_age": 50,
                "heart_rate": 100
    }

    output_10 = check_input(input_10)
    assert output_10 is False

    input_11 = {
                "user_email": "suyash@suyashkumar.com",
                "user_age": "fifty",
                "heart_rate": 100
    }

    with pytest.raises(ValueError):
        output_11 = check_input(input_11)
    assert output_11 is False

    input_12 = {
        "user_email": "suyash@suyashkumar.com",
        "user_age": 50,
        "heart_rate": math.sqrt(-100)
    }

    with pytest.raises(ValueError):
        output_12 = check_input(input_12)
    assert output_12 is False





