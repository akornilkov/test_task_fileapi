from fileapi.api.serializers.serializer import ma


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('_id', 'name', 'description', 'price', 'qty')
