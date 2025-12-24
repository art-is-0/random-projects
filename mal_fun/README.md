# Compare anime- or manga lists from MyAnimeList

This is a short code that uses the malpy module to query the anime lists of users and compare them to each other. You can get two dictionaries which hold the anime that only one person has watched and another dictionary that contains the anime two or more people have watched with the people that have watched and the mean score. (Does not count if they have rated it 0)

## Requirements
Python 3.10.12
```sh
pip install -r requirements.txt
```

## API-key
You can get an API key for MAL officially from their website on your account. When you have it, add it to a `.env` file as MAL_TOKEN for the script to work.