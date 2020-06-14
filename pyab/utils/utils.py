"""Utility Functions for Frequentist & Bayesian A/B Testing methods."""


def check_valid_input(numerator, denominator):
    """
    Utility function to check input data consistency.

    Parameters
    ----------
    numerator : int
        number of successful clicks or successful events.
    numerator : int
        number of impressions or events.
    """
    if numerator < 0:
        raise ValueError("Found input successful clicks less than 0") 
    elif denominator <= 0:
        raise ValueError("Found input trials less than or equal to 0")
    elif not isinstance(numerator, int) or not isinstance(denominator, int):
        raise ValueError("Expected input success and trials not type int")
    elif numerator > denominator:
        raise ValueError("Found input successful clicks %s greater than trials %s" % (
            numerator, denominator))

def check_valid_parameter(parameter):
    """
    Utility function to check input parameter consistency.

    Parameters
    ----------
    parameter : float
        Type-I or Type-II error rate.
    """
    if parameter < 0 or parameter > 1:
        raise ValueError("Found input parameter less than 0 or greater than 1")

def check_t_test(trials_a, trials_b):
    """
    Utility function to check if t test or not.

    Parameters
    ----------
    trials_a : int
        number of successful clicks or successful events.
    trials_b : int
        number of impressions or events.

    Return
    ------
    flag : bool
        True if t test or False    
    """
    return True if trials_a + trials_b < 30 else False