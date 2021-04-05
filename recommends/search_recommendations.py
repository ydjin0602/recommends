import multiprocessing as mp
import os

RESULT = []


def search_recommendations(sku, recommendation_min):
    pool = mp.Pool(12)
    jobs = []

    # create jobs
    for chunk_start, chunk_size in chunk_splitting("recommends.csv"):
        jobs.append(pool.apply_async(process_wrapper, (chunk_start, chunk_size, sku, recommendation_min)))

    result = []
    for job in jobs:
        result.extend(job.get())

    pool.close()

    return result


def process_wrapper(chunk_start, chunk_size, sku, recommendation_min):
    with open("recommends.csv") as f:
        f.seek(chunk_start)
        lines = f.read(chunk_size).splitlines()
        for line in lines:
            process(line, sku, recommendation_min)

    return RESULT


def chunk_splitting(filename, size=1024 * 1024):
    file_end = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        chunk_end = f.tell()
        while True:
            chunk_start = chunk_end
            f.seek(size, 1)
            f.readline()
            chunk_end = f.tell()
            yield chunk_start, chunk_end - chunk_start
            if chunk_end > file_end:
                break


def process(line, sku, recommendation_min):
    data = line.split(',')
    if data[0] == sku and float(data[2]) >= recommendation_min:
        RESULT.append(data[1])
