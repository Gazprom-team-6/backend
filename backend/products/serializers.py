from rest_framework import serializers

from products.models import Product
from users.serializers import EmployeeShortGetSerializer


class ProductBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для продуктов."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(ProductBaseSerializer):
    """Сериализатор для добавления и изменения продукта."""

    class Meta:
        model = Product
        fields = "__all__"

    def validate_parent_product(self, value):
        """
        Проверяем, что родителем продукта не назначен сам продукт.
        """
        if self.instance and value == self.instance:
            raise serializers.ValidationError(
                "Нельзя назначить родительским "
                "продуктом сам продукт."
            )
        return value


class ProductReadSerializer(ProductBaseSerializer):
    """Сериализатор для получения информации о продукте."""

    product_manager = EmployeeShortGetSerializer()
    parent_product = ProductBaseSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class ProductChildrenReadSerializer(ProductBaseSerializer):
    """Сериализатор для получения дочерних продуктов."""

    product_manager = EmployeeShortGetSerializer()

    class Meta:
        model = Product
        fields = ["id", "product_name", "product_manager",
                  "product_description"]
