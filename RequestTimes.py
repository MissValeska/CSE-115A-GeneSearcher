import requests
import time

trials = 10
print("--- Average Request Time for Various Sources Test ---")
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
        # print("Downloading from ", url, ": ")
        tic = time.perf_counter()
        response = requests.get(url)
        toc = time.perf_counter()
        urls[url] = urls[url] + (toc - tic)
        # print(f"Downloaded the data in {toc - tic:0.4f} seconds")

print("Average request time by url over ", trials, "trials :")
for url in urls:
    urls[url] = urls[url] / trials
    print("URL: ", url, f" - Time: {urls[url]:0.4f} seconds")


print("\n--- Average Request Time Session vs Non-Session Test --- ")
print("--- NON-SESSION ---")
urls = {"https://opensnp.org/snps/json/annotation/rs548049170.json":0,
        "https://opensnp.org/snps/json/annotation/rs4988235.json":0,
        "https://opensnp.org/snps/json/annotation/rs9283150.json":0,
        "https://opensnp.org/snps/json/annotation/rs116587930.json":0,
        "https://opensnp.org/snps/json/annotation/rs3131972.json":0,
        "https://opensnp.org/snps/json/annotation/rs12184325.json":0,
        "https://opensnp.org/snps/json/annotation/rs12567639.json":0,
        "https://opensnp.org/snps/json/annotation/rs114525117.json":0,
        "https://opensnp.org/snps/json/annotation/rs12124819.json":0,
        "https://opensnp.org/snps/json/annotation/rs4988235.json":0,
        "https://opensnp.org/snps/json/annotation/rs548049170.json":0}

for i in range(trials):
    print("--- Trial ", i, " ---")
    for url in urls:
        # print("Downloading from ", url, ": ")
        tic = time.perf_counter()
        response = requests.get(url)
        toc = time.perf_counter()
        urls[url] = urls[url] + (toc - tic)
        # print(f"Downloaded the data in {toc - tic:0.4f} seconds")

print("Average request time by url over ", trials, "trials :")
for url in urls:
    urls[url] = urls[url] / trials
    print("URL: ", url, f" - Time: {urls[url]:0.4f} seconds")

print("--- Session ---")
session = requests.Session()

for i in range(trials):
    print("--- Trial ", i, " ---")
    for url in urls:
        # print("Downloading from ", url, ": ")
        tic = time.perf_counter()
        response = session.get(url)
        toc = time.perf_counter()
        urls[url] = urls[url] + (toc - tic)
        # print(f"Downloaded the data in {toc - tic:0.4f} seconds")

print("Average request time by url over ", trials, "trials :")
for url in urls:
    urls[url] = urls[url] / trials
    print("URL: ", url, f" - Time: {urls[url]:0.4f} seconds")