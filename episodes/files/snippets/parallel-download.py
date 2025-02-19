from concurrent.futures import ThreadPoolExecutor, as_completed
from timeit import timeit
import requests  # install with `pip install requests`


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

downloaded_files = []

def sequentialDownload():
    for mass in range(10, 20):
        url = f"https://github.com/SNEWS2/snewpy-models-ccsn/raw/refs/heads/main/models/Warren_2020/stir_a1.23/stir_multimessenger_a1.23_m{mass}.0.h5"
        f = download_file(url, f"seq_{mass}.h5")
        downloaded_files.append(f)

def parallelDownload():
    pool = ThreadPoolExecutor(max_workers=6)
    jobs = []
    for mass in range(10, 20):
        url = f"https://github.com/SNEWS2/snewpy-models-ccsn/raw/refs/heads/main/models/Warren_2020/stir_a1.23/stir_multimessenger_a1.23_m{mass}.0.h5"
        local_filename = f"par_{mass}.h5"
        jobs.append(pool.submit(download_file, url, local_filename))

    for result in as_completed(jobs):        
        if result.exception() is None:
            # handle return values of the parallelised function
            f = result.result()
            downloaded_files.append(f)
        else:
            # handle errors
            print(result.exception())

    pool.shutdown(wait=False)


print(f"sequentialDownload: {timeit(sequentialDownload, globals=globals(), number=1):.3f} s")
print(downloaded_files)
downloaded_files = []
print(f"parallelDownload: {timeit(parallelDownload, globals=globals(), number=1):.3f} s")
print(downloaded_files)