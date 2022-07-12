from mptt.forms import TreeNodeChoiceField
import django_filters

from .models import Product, Category, Color, Leftover, Size, Sex


class TreeNodeChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = TreeNodeChoiceField

    def filter(self, qs, value):
        print(value)
        if value != self.null_value:
            print(value)
            return self.get_method(qs)(**{f'{self.field_name}__in': value.get_descendants(include_self=True)})

        return qs.distinct() if self.distinct else qs


class MultipleCharFilter(django_filters.CharFilter):
    """
    Allows multiple options in a comma separated list for Char fields.
    Example:
      - field=value       # filter by a single value
      - field=val1,val2   # Filter by val1 OR val2  (Django's 'in' lookup)
    """

    def filter(self, qs, value):
        if not value:
            return qs

        values = value.split(',')
        if len(values) > 1:
            self.lookup_expr = 'in'
        else:
            values = values[0]

        return super(MultipleCharFilter, self).filter(qs, values)


class ProductFilterSet(django_filters.FilterSet):
    category = TreeNodeChoiceFilter(queryset=Category.objects.all(), field_name='category', required=True)
    price = django_filters.RangeFilter(field_name='price')
    brand = MultipleCharFilter(field_name="brand__slug", lookup_expr="icontains")
    color = django_filters.ModelMultipleChoiceFilter(field_name="color__code_1c", to_field_name="code_1c",
                                                     queryset=Color.objects.all())
    size = django_filters.ModelMultipleChoiceFilter(field_name="leftovers__parent_size__title", to_field_name="title",
                                                    queryset=Size.objects.all())

    class Meta:
        model = Product
        fields = ('price', 'brand', 'color', 'size')


class ProductSearchFilterSet(django_filters.FilterSet):
    sex = django_filters.ModelMultipleChoiceFilter(field_name='sex__slug', to_field_name='slug',
                                                   queryset=Sex.objects.all())
    price = django_filters.RangeFilter(field_name='price')
    brand = MultipleCharFilter(field_name="brand__slug", lookup_expr="icontains")
    color = django_filters.ModelMultipleChoiceFilter(field_name="color__code_1c", to_field_name="code_1c",
                                                     queryset=Color.objects.all())
    size = django_filters.ModelMultipleChoiceFilter(field_name="leftovers__parent_size__title", to_field_name="title",
                                                    queryset=Size.objects.all())

    class Meta:
        model = Product
        fields = ('price', 'brand', 'color', 'size', 'sex')
