"""Locust translation of the theatre/movie/showtime JMeter scenario."""

import os

from locust import HttpUser, constant, task

API_HOST = os.getenv("netflix_API_HOST", "https://apis.netflix.com")
REQUEST_DELAY_SECONDS = 0.1


def _required_environment_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Set the required environment variable before starting Locust: {name}")
    return value


class TheatreMovieShowtimeUser(HttpUser):
    host = API_HOST
    wait_time = constant(REQUEST_DELAY_SECONDS)
    film_id: str
    showtime_date: str

    def on_start(self) -> None:
        self.film_id = _required_environment_variable("netflix_FILM_ID")
        session_token = _required_environment_variable("netflix_SESSION_TOKEN")
        subscription_key = _required_environment_variable("netflix_SUBSCRIPTION_KEY")
        self.showtime_date = os.getenv("netflix_SHOWTIME_DATE", "2022-03-02")
        self.client.headers.update(
            {
                "Content-Type": "application/json",
                "User-Session-Token": session_token,
                "Ocp-Apim-Subscription-Key": subscription_key,
            }
        )

    def _get_json(self, path: str, *, name: str, params: dict[str, str]) -> dict | None:
        with self.client.get(path, name=name, params=params, catch_response=True) as response:
            if not response.ok:
                response.failure(f"HTTP {response.status_code}")
                return None
            try:
                payload = response.json()
            except ValueError:
                response.failure("Response is not valid JSON")
                return None
            if not isinstance(payload, dict):
                response.failure("Response JSON is not an object")
                return None
            response.success()
            return payload

    def _get(self, path: str, *, name: str, params: dict[str, str] | None = None) -> None:
        self.client.get(path, name=name, params=params)

    @task
    def browse_showtimes(self) -> None:
        self._get("/uat/cpx/theatrical/api/v1/theatres", name="theatres")
        self.wait()
        self._get(
            "/uat/cpx/theatrical/api/v1/movies",
            name="movies - en",
            params={"language": "en"},
        )
        self.wait()

        payload = self._get_json(
            "/uat/cpx/theatrical/api/v1/showtimes/theatres",
            name="showtimes - threatres - film",
            params={"filmId": self.film_id},
        )
        if payload is None:
            return

        nearby_theatres = payload.get("nearbyTheatres", [])
        if not isinstance(nearby_theatres, list):
            return

        for theatre in nearby_theatres:
            if not isinstance(theatre, dict):
                continue
            theatre_id = theatre.get("theatreId")
            if theatre_id is None:
                continue
            self.wait()
            self._get(
                "/uat/cpx/theatrical/api/v1/showtimes",
                name="showtimes - location & date",
                params={
                    "locationId": str(theatre_id),
                    "date": self.showtime_date,
                },
            )
