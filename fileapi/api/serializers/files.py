from fileapi.api.serializers.serializer import ma


class FileSchema(ma.Schema):
    class Meta:
        fields = ('_id', 'name', 'description', 'price', 'qty')
