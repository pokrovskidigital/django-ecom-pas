from mptt.forms import TreeNodeChoiceField
import django_filters

from models import Product


class TreeNodeChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = TreeNodeChoiceField

    def filter(self, qs, value):
        if value != self.null_value:
            return self.get_method(qs)(**{f'{self.field_name}__in': value.get_descendants(include_self=True)})

        return qs.distinct() if self.distinct else qs


class ProductFilterset(django_filters.FilterSet):
    category = TreeNodeChoiceFilter()

    class Meta:
        model = Product
        fields = ('category',)
