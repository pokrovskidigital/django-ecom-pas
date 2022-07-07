from mptt.forms import TreeNodeChoiceField
import django_filters

from .models import Product, Category


class TreeNodeChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = TreeNodeChoiceField

    def filter(self, qs, value):
        if value != self.null_value:
            print(value)
            return self.get_method(qs)(**{f'{self.field_name}__in': value.get_descendants(include_self=True)})

        return qs.distinct() if self.distinct else qs


class ProductFilterset(django_filters.FilterSet):
    category = TreeNodeChoiceFilter(queryset=Category.objects.all(), field_name='category__title')

    class Meta:
        model = Product
        fields = ('category',)
