from pytube import YouTube
from pytube import Search
import os

def process_link(link):
    yt = YouTube(link)
    start_download(yt)

def process_search(search):
    yt_search = Search(search)
    yt = yt_search.results[0]
    start_download(yt)

def start_download(asset: YouTube):
    audios = asset.streams.filter(only_audio=True)
    audios[0].download(output_path="downloads")

# Get the current working directory
current_directory = os.getcwd()

# Define the path for the "downloads" directory
downloads_directory = os.path.join(current_directory, 'downloads')

# Check if the "downloads" directory exists
if not os.path.exists(downloads_directory):
    # Create the "downloads" directory
    os.makedirs(downloads_directory)
    print("The 'downloads' directory has been created.")
else:
    print("The 'downloads' directory already exists.")

search_or_link = input("Type in the name or link of the video (name does not need to be exact):\n")
link = False
if (".com" in search_or_link) or ("youtu.be" in search_or_link) or ("youtube" in search_or_link):
    link = True

process_link(search_or_link) if link is True else process_search(search_or_link)