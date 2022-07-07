from mptt.forms import TreeNodeChoiceField
import django_filters

from .models import Product, Category, Color, Leftover


class TreeNodeChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = TreeNodeChoiceField

    def filter(self, qs, value):
        if value != self.null_value:
            print(value)
            return self.get_method(qs)(**{f'{self.field_name}__in': value.get_descendants(include_self=True)})

        return qs.distinct() if self.distinct else qs


class ProductFilterset(django_filters.FilterSet):
    # category = TreeNodeChoiceFilter(queryset=Category.objects.all(), field_name='category__title')
    price = django_filters.RangeFilter(field_name='price')
    brand = django_filters.CharFilter(field_name="brand__slug", lookup_expr="icontains")
    color = django_filters.ModelMultipleChoiceFilter(field_name="color__code_1c", to_field_name="code_1c",
                                                     queryset=Color.objects.all())
    size = django_filters.ModelMultipleChoiceFilter(field_name="leftovers__parent_size__slug",
                                                    to_field_name='parent_size__slug',
                                                    queryset=Leftover.objects.all())

    class Meta:
        model = Product
        fields = ('price', 'brand', 'color', 'size')
