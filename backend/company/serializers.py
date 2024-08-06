from django.contrib.auth import get_user_model
from rest_framework import serializers

from company.models import Department, Product
from users.serializers import EmployeeShortGetSerializer

User = get_user_model()


class DepartmentBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для департаментов."""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner"]


class DepartmentWriteSerializer(DepartmentBaseSerializer):
    """Сериализатор для создания и изменения департаментов."""

    class Meta:
        model = Department
        fields = "__all__"

    def validate_parent_department(self, value):
        """
        Проверяем, что родителем департамента не назначен сам департамент.
        """
        if self.instance and value == self.instance:
            raise serializers.ValidationError(
                "Нельзя назначить родительским "
                "департаментом сам департамент."
            )
        return value


class DepartmentReadSerializer(DepartmentBaseSerializer):
    """Сериализатор для получения департаментов."""

    departament_owner = EmployeeShortGetSerializer()
    parent_department = DepartmentBaseSerializer()

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner",
                  "departament_description", "parent_department"]


class DepartmentChildrenReadSerializer(DepartmentBaseSerializer):
    """Сериализатор для получения дочерних департаментов."""

    departament_owner = EmployeeShortGetSerializer()

    class Meta:
        model = Department
        fields = ["id", "departament_name", "departament_owner",
                  "departament_description"]


class DepartmentAddEmployeesSerializer(serializers.Serializer):
    """Сериализатор для добавления сотрудников в департамент."""

    employee_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=0),
    )

    def validate_employee_ids(self, value):
        """Проверяем, что сотрудники с переданными ID существуют в БД."""
        existing_ids = set(
            User.objects.filter(id__in=value).values_list(
                'id',
                flat=True
            )
        )
        provided_ids = set(value)
        missing_ids = provided_ids - existing_ids
        if missing_ids:
            raise serializers.ValidationError(
                f"Следующие сотрудники не существуют: {list(missing_ids)}"
            )
        return value


class EmployeeListResponseSerializer(serializers.Serializer):
    """Сериализатор для получения списка сотрудников и их общего количества."""

    total_employees = serializers.IntegerField()
    employees = EmployeeShortGetSerializer(many=True)


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

    class Meta:
        model = Product
        fields = "__all__"

    product_manager = EmployeeShortGetSerializer()
    parent_product = ProductBaseSerializer()


class ProductChildrenReadSerializer(ProductBaseSerializer):
    """Сериализатор для получения дочерних продуктов."""

    product_manager = EmployeeShortGetSerializer()

    class Meta:
        model = Product
        fields = ["id", "product_name", "product_manager",
                  "product_description"]



