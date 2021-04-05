import multiprocessing as mp
import os

import typing as t

RESULT = []


def search_recommendations(sku: str, recommendation_min: float) -> t.List[str]:
    pool = mp.Pool(12)
    jobs = []

    # create jobs
    for chunk_start, chunk_size in chunk_splitting("recommends.csv"):
        jobs.append(pool.apply_async(process_wrapper, (chunk_start, chunk_size, sku, recommendation_min)))

    result = []
    for job in jobs:
        result.extend(job.get())

    pool.close()

    return list(set(result))


def process_wrapper(chunk_start: int, chunk_size: int, sku: str, recommendation_min: float) -> t.List[str]:
    with open("recommends.csv") as file:
        file.seek(chunk_start)
        lines = file.read(chunk_size).splitlines()
        for line in lines:
            process(line, sku, recommendation_min)

    return RESULT


def chunk_splitting(filename: str, size=1024 * 1024):
    file_end = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        chunk_end = file.tell()
        while True:
            chunk_start = chunk_end
            file.seek(size, 1)
            file.readline()
            chunk_end = file.tell()
            yield chunk_start, chunk_end - chunk_start
            if chunk_end > file_end:
                break


def process(line: str, sku: str, recommendation_min: float) -> None:
    data = line.split(',')
    if data[0] == sku and float(data[2]) >= recommendation_min:
        RESULT.append(data[1])
