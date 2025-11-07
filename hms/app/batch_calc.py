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
    logger.info("average_age_threaded computed", extra={"average": overall})
    return overall
