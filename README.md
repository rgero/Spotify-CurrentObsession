# Spotify - Current Obsessions

This project is a simple script that exercises that Spotify REST API to generate a playlist of your most listened to songs over the course of a given time frame. It was the inspiration for a React website that I am currently working on, but for the time being can be ran on its own should one choose.

### What is needed to run

The first thing you would need to do is create a developer application through Spotify. You can do this here - [https://developer.spotify.com/dashboard/login](https://developer.spotify.com/dashboard/login). This will give you access to the Spotify APIs.

Once completed, you would need to manually define a file named `credentials.py`. This file should contain a simple dictionary with the following keys

* SPOTIFY_API_KEY
* SPOTIFY_API_SECRET
* SPOTIFY_URI

The first two are given to you from Spotify after you create your application and the third is one that you define in the application settings. Typically you can use something like `http://localhost:8080`

Here is an example `credentials.py` file.

```
credentials={
  "SPOTIFY_API_KEY" : "NotARealKeyJustAnExample",
  "SPOTIFY_API_SECRET" : "NotASecretJustAnExample",
  "SPOTIFY_URI" : "http://localhost:8080",
}
```

Ideally if this were to be deployed to a server or something of that nature, you'd define these in a more secure method, however for the purpose of this script I chose to do it this way while making certain I do not accidentally check in it into source control.

Once you have this all set up, you can follow the builder pattern defined in the SpotifyObsession class.
