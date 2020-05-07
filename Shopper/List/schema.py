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


class ItemCreation(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int(required=True)
        name = graphene.String(required=True)
        id = graphene.ID()

    item = graphene.Field(ItemType, id=graphene.Int(), name=graphene.String(), quantity=graphene.Int())

    def mutate(self, info, **kwargs):
        item = Item.objects.create(name=kwargs.get('name'), quantity=kwargs.get('quantity'))
        item.save()
        return ItemCreation(item=item)


class ItemDeletion(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    deleted = graphene.Boolean()
    id = graphene.Int()

    def mutate(self, info, **kwargs):
        ok = False
        id = kwargs.get('id')
        if Item.objects.filter(id=id).exists():
            item = Item.objects.get(id=id)
            item.delete()
            ok = True
        return ItemDeletion(id=id, deleted=ok)


class ItemMutation(graphene.Mutation):
    class Arguments:
        quantity = graphene.Int()
        name = graphene.String()
        id = graphene.ID()

    item = graphene.Field(ItemType)

    def mutate(self, info, **kwargs):
        id = kwargs.get('id')
        item = Item.objects.get(id=id)
        if 'name' in kwargs:
            name = kwargs.get('name')
            item.name = name
        if 'quantity' in kwargs:
            quantity = kwargs.get('quantity')
            item.quantity = quantity

        item.save()
        return ItemMutation(item=item)


class Mutation(graphene.ObjectType):
    update_item = ItemMutation.Field()
    create_item = ItemCreation.Field()
    delete_item = ItemDeletion.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
