import requests
import pandas as pd


class Genius:
    """A class for getting artist information from the Genius API."""

    def __init__(self, access_token):
        # Store the API access token and base URL.
        self.access_token = access_token
        self.base_url = "https://api.genius.com"

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
            params={"q": search_term, "per_page": 50},
            timeout=30
        )

        response.raise_for_status()

        hits = response.json()["response"]["hits"]

        # Check if any results were found.
        if not hits:
            raise ValueError(
                f"No results found for {search_term}"
            )

        # Find an artist whose name matches the search term.
        artist_id = None

        for hit in hits:
            artist = hit["result"]["primary_artist"]

            if artist["name"].lower() == search_term.lower():
                artist_id = artist["id"]
                break

        # Raise an error if the artist was not found.
        if artist_id is None:
            raise ValueError(
                f"Artist not found: {search_term}"
            )

        # Get detailed information about the artist.
        artist_url = f"{self.base_url}/artists/{artist_id}"

        response = requests.get(
            artist_url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        artist_data = response.json()["response"]["artist"]

        return artist_data

    def get_artists(self, search_terms):
        # Store information for multiple artists.
        artists = []

        for search_term in search_terms:
            # Get information for each artist.
            artist = self.get_artist(search_term)

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
    