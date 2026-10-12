
import os
import requests
import pandas as pd
from dotenv import load_dotenv


class Genius:
    """A class for getting artist information from the Genius API."""

    def __init__(self, access_token=None):
        # Load the API access token from the .env file.
        load_dotenv()

        # Store the API access token and base URL.
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        self.base_url = "https://api.genius.com"

        if not self.access_token:
            raise ValueError("ACCESS_TOKEN is missing from the environment.")

    def get_artist(self, search_term):
        # Set up the API authorization.
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Search for the artist.
        search_url = f"{self.base_url}/search"

        response = requests.get(
            search_url,
            headers=headers,
            params={"q": search_term},
            timeout=30
        )

        response.raise_for_status()

        # Get the first search result.
        json_data = response.json()
        hits = json_data["response"]["hits"]

        # Check if any results were found.
        if not hits:
            raise ValueError(
                f"No results found for {search_term}"
            )

        # Extract the primary artist ID from the first hit.
        artist_id = hits[0]["result"]["primary_artist"]["id"]

        # Get detailed information about the artist.
        artist_url = f"{self.base_url}/artists/{artist_id}"

        response = requests.get(
            artist_url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        # Return the complete JSON response.
        return response.json()

    def get_artists(self, search_terms):
        # Store information for multiple artists.
        artists = []

        for search_term in search_terms:
            # Get information for each artist.
            artist_data = self.get_artist(search_term)
            artist = artist_data["response"]["artist"]

            artists.append({
                "search_term": search_term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count")
            })

        # Convert the results into a DataFrame.
        return pd.DataFrame(
            artists,
            columns=[
                "search_term",
                "artist_name",
                "artist_id",
                "followers_count"
            ]
        )
