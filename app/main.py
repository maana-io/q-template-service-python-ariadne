import os
import logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "info").upper())

from ariadne import ObjectType, QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from asgi_lifespan import LifespanManager
from graphqlclient import GraphQLClient
from starlette.applications import Starlette

# .env
from dotenv import load_dotenv

from app.qclient import QClient

# Load environment variables
load_dotenv()


def getClient():
    qClient = None
    qEndpoint = os.getenv('MAANA_ENDPOINT_URL')

    if not qEndpoint:
        logging.info('Maana Q endpoint is not set')
        return None
    else:
        # Build as closure to keep scope clean.
        def buildClient(client=qClient):
            # Cached in regular use cases.
            if (client is None):
                logging.info('Building graphql client...')
                client = QClient(os.getenv('MAANA_ENDPOINT_URL'))
            return client
        return buildClient()


# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql("""
    type Query {
        people: [Person!]!
    }

    type Person {
        firstName: String
        lastName: String
        age: Int
        fullName: String
    }
""")

# Map resolver functions to Query fields using QueryType
query = QueryType()

# Resolvers are simple python functions


@query.field("people")
def resolve_people(_, info):

    # # A resolver can access the graphql client via the context.
    # client = info.context["client"]

    # # Query all maana services.
    # result = client.execute('''
    # {
    #     allServices {
    #         id
    #         name
    #     }
    # }
    # ''')

    # print(result)

    return [
        {"firstName": "Marie", "lastName": "Curie", "age": 21},
        {"firstName": "Rubab", "lastName": "Nedzo", "age": 24},
    ]


# Map resolver functions to custom type fields using ObjectType
person = ObjectType("Person")


@person.field("fullName")
def resolve_person_fullname(person, *_):
    return "%s %s" % (person["firstName"], person["lastName"])


# Create executable GraphQL schema
schema = make_executable_schema(type_defs, [query, person])

# --- ASGI app


async def startup():
    logging.info("Starting up...")
    logging.info("... done!")


async def shutdown():
    logging.info("Shutting down...")
    logging.info("... done!")

# Create an ASGI app using the schema, running in debug mode
# Set context with authenticated graphql client.
app = Starlette(debug=True, on_startup=[startup], on_shutdown=[shutdown])
app.mount('/', GraphQL(schema, debug=True,
                       context_value={'client': getClient()}))
