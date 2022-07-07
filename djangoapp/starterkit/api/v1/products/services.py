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
    class Meta:
        model = Product
        fields = ('category',)

    def __init__(self, *args, **kwargs):
        super(ProductFilterset, self).__init__(*args, **kwargs)
        self.filters['category'].field_class = TreeNodeChoiceField(queryset=Category.objects.all())  # fk
