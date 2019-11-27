from ariadne import ObjectType, QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from asgi_lifespan import Lifespan, LifespanMiddleware

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
def resolve_people(*_):
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

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema, debug=True)

# 'Lifespan' is a standalone ASGI app.
# It implements the lifespan protocol,
# and allows registering lifespan event handlers.
lifespan = Lifespan()


@lifespan.on_event("startup")
async def startup():
    print("Starting up...")
    print("... done!")


@lifespan.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    print("... done!")

# 'LifespanMiddleware' returns an ASGI app.
# It forwards lifespan requests to 'lifespan',
# and anything else goes to 'app'.
app = LifespanMiddleware(app, lifespan=lifespan)
