import graphene
from graphene_django.types import DjangoObjectType
from .models import Item


class ItemType(DjangoObjectType):
    class Meta:
        model = Item


class Query(graphene.ObjectType):
    item = graphene.Field(ItemType, id=graphene.Int(), name=graphene.String(), quantity=graphene.Int())
    all_items = graphene.List(ItemType)

    def resolve_all_items(self, info, **kwargs):
        return Item.objects.all()

    def resolve_item(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None and Item.objects.filter(id=id).exists():
            return Item.objects.get(id=id)
        return None


class ItemMutation(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int(required=True)
        id = graphene.ID()

    item = graphene.Field(ItemType, id=graphene.Int(), name=graphene.String(), quantity=graphene.Int())

    def mutate(self, info, quantity, id):
        item = Item.objects.get(id=id)
        item.quantity = quantity
        item.save()
        return ItemMutation(item=item)


class Mutation(graphene.ObjectType):
    update_item = ItemMutation.Field()
