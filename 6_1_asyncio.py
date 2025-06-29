import requests
from time import time

url = 'https://loremflickr.com/320/240'

def get_file(url):
    response = requests.get(url, allow_redirects=True)
    return response

def write_file(response, time):
    #https://loremflickr.com/cache/resized/defaultImage.small_320_240_nofilter.jpg
    filename = str(time) + response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)

def main():
    t0 = time()
    url = 'https://loremflickr.com/320/240'
    for i in range (10):
        write_file(get_file(url), time())
    print(time() - t0)

if __name__ == '__main__':
    main()



