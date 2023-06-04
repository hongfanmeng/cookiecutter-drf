from django_filters import rest_framework as filters


class FilterNotMixin:
    @classmethod
    def filter_for_field(cls, field, field_name, lookup_expr=None):
        exclude = False
        if lookup_expr and lookup_expr.startswith("not_"):
            lookup_expr = lookup_expr.replace("not_", "")
            exclude = True
        filter = super().filter_for_field(field, field_name, lookup_expr)
        filter.exclude = exclude
        return filter


class FilterSet(FilterNotMixin, filters.FilterSet):
    pass


class FilterBackend(filters.DjangoFilterBackend):
    filterset_base = FilterSet
