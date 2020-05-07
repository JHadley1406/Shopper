import graphene
from .List import schema

# This is only needed if we need to register multiple apps in the project.
# For now, we're doing everything from List.schema
class Query(schema.Query, graphene.ObjectType):
    pass


class Mutation(schema.Mutation, graphene.ObjectType):
    pass


#schema = graphene.Schema(query=Query, mutation=Mutation)
