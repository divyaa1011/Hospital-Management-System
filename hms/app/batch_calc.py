"""Batch average-age using ThreadPoolExecutor."""

from concurrent.futures import ThreadPoolExecutor
from typing import List
import math
import logging
from .models import Patient

logger = logging.getLogger(__name__)

def _avg(batch: List[Patient]) -> float:
    if not batch:
        return 0.0
    return sum(p.age for p in batch) / len(batch)
"""
    Calculate the average age of patients in a given batch.

    Args:
        batch (List[Patient]): A list of Patient objects.

    Returns:
        float: The average age of the patients in the batch.
               Returns 0.0 if the batch is empty.

    Example:
        >>> _avg([Patient(age=20), Patient(age=30)])
        25.0
    """

def average_age_threaded(patients: List[Patient], batch_size: int = 10) -> float:
    if not patients:
        return 0.0
    batches = [patients[i:i + batch_size] for i in range(0, len(patients), batch_size)]
    with ThreadPoolExecutor() as ex:
        results = list(ex.map(_avg, batches))
    # overall average: average of batch averages weighted by batch sizes
    total_people = sum(len(b) for b in batches)
    weighted_sum = sum((results[i] * len(batches[i])) for i in range(len(batches)))
    overall = weighted_sum / total_people if total_people else 0.0
    """
    Compute the weighted sum of batch averages based on batch sizes.

    Each batch has an average (from `results`) and a corresponding number
    of patients (`len(batches[i])`). The weighted sum multiplies each
    batch's average by its size, ensuring that larger batches have a
    proportionally higher impact on the overall average.

    Args:
        results (List[float]): A list of average ages for each batch.
        batches (List[List[Patient]]): A list of patient batches corresponding to the averages.

    Returns:
        float: The weighted sum of all batch averages.

    Example:
        >>> results = [25.0, 35.0]
        >>> batches = [[1, 2, 3, 4], [5, 6]]
        >>> _weighted_sum(results, batches)
        25.0*4 + 35.0*2 = 150.0
    """
    logger.info("average_age_threaded computed", extra={"average": overall})
    return overall
