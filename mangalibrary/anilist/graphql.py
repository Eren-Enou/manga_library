from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

class AniListAPI:
    BASE_URL = 'https://graphql.anilist.co'

    def __init__(self):
        self.transport = AIOHTTPTransport(url=self.BASE_URL)
        self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

    async def fetch_manga_details(self, manga_id):
        """Fetch details for a single manga by its ID using GraphQL."""
        query = gql("""
        query ($id: Int) {
            Media(id: $id, type: MANGA) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                coverImage {
                    large
                }
                genres
                status
            }
        }
        """)

        params = {"id": manga_id}
        response = await self.client.execute_async(query, variable_values=params)
        return response
