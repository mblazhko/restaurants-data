import httpx
import json


class JustEatClient:
    @staticmethod
    def by_postcode(postcode: str):
        url = f"https://uk.api.just-eat.io/restaurants/bypostcode/{postcode}"

        with httpx.Client() as client:
            response = client.get(url)

            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                return f"HTTP error occurred: {exc}"

            restaurants = []

            restaurant_data = response.json().get("Restaurants")

            for place in restaurant_data:
                if postcode in place.get('Postcode'):
                    restaurant = {
                        "Name": place.get("Name"),
                        "Rating": place.get("RatingAverage"),
                        "Cuisines": [
                            name["Name"] for name in place.get("Cuisines")
                        ],
                    }
                    restaurants.append(restaurant)

            if len(restaurants) != 0:
                return json.dumps(restaurants)
            return "There is no restaurants for your request"
