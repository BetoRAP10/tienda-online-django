from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'is_active')
        # fields = '__all__'

    # Al crear o actualizar se recibe el id de la categoria,
    # pero al mostrar el producto se devuelve su nombre
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = str(instance.category)
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
