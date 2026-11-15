"""
9-апта: сүзгі (django-filter), іздеу және сұрыптау.

RecipeFilter            – ?category=  ?cuisine=  ?difficulty=  ?min_time=  ?max_time=
MultiCaseSearchFilter   – ?search=   (SQLite кириллицада регистрді ажыратпайтындай етіп түзетілген)
StableOrderingFilter    – ?ordering= (беттер арасында ретті тұрақты ету үшін соңына id қосады)
"""
import operator
from functools import reduce

from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    min_time = filters.NumberFilter(field_name="cooking_time", lookup_expr="gte",
                                    label="Дайындау уақыты, кемінде (мин)")
    max_time = filters.NumberFilter(field_name="cooking_time", lookup_expr="lte",
                                    label="Дайындау уақыты, көбі (мин)")

    class Meta:
        model = Recipe
        # category, cuisine – ForeignKey id бойынша; difficulty – easy / medium / hard
        fields = ["category", "cuisine", "difficulty"]


class MultiCaseSearchFilter(SearchFilter):
    """
    Қарапайым SearchFilter SQLite-та кириллицада регистрді ажыратады ("плов" ≠ "Плов").
    Мұнда сөздің бірнеше жазылуы (түпнұсқа, кіші, бас әріп, бірінші әріп бас) тексеріледі.
    Бірнеше сөз болса, барлығы табылуы керек (AND); бір сөз бірнеше өрістің біреуінен табылса жеткілікті (OR).
    """

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, "search_fields", None)
        terms = self.get_search_terms(request)
        if not search_fields or not terms:
            return queryset

        conditions = []
        for term in terms:
            variants = {term, term.lower(), term.upper(), term.capitalize(), term.title()}
            q = Q()
            for field in search_fields:
                for variant in variants:
                    q |= Q(**{f"{field}__icontains": variant})
            conditions.append(q)
        return queryset.filter(reduce(operator.and_, conditions))


class StableOrderingFilter(OrderingFilter):
    """Сұрыптау мәндері бірдей болса да беттер араласпауы үшін соңына id қосады."""

    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)
        current = list(queryset.query.order_by)
        return queryset.order_by(*current, "id")
