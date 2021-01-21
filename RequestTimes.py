import requests
import time

trials = 50

urls = {"https://opensnp.org/snps/json/annotation/rs4988235.json":0,
        "https://opensnp.org/snps/json/annotation/rs548049170.json":0,
        "https://opensnp.org/snps/rs4988235":0,
        "https://opensnp.org/snps/rs548049170":0,
        "https://www.snpedia.com/index.php/Rs4988235":0,
        "https://www.snpedia.com/index.php/rs548049170":0,
        "https://bots.snpedia.com/index.php/Rs4988235":0,
        "https://bots.snpedia.com/index.php/rs548049170":0}

for i in range(trials):
    print("--- Trial ", i, " ---")
    for url in urls:
        print("Downloading from ", url, ": ")
        tic = time.perf_counter()
        response = requests.get(url)
        toc = time.perf_counter()
        urls[url] = urls[url] + (toc - tic)
        # print(f"Downloaded the data in {toc - tic:0.4f} seconds")

print("Average request time by url over ", trials, "trials :")
for url in urls:
    urls[url] = urls[url] / trials
    print("URL: ", url, f" - Time: {urls[url]:0.4f} seconds")
