from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied
from .models import Cliente, Fornitore
from .serializers import ClienteSerializer, FornitoreSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FornitoreFilterFE, ClienteFilterFE
from rest_framework.permissions import IsAuthenticated


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ClienteFilterFE
    search_fields = ["ragionesociale"]
    ordering_fields = ["ragionesociale"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to only show clienti belonging to the current user's company
        """
        if not hasattr(self.request.user, 'profile') or not self.request.user.profile.company:
            raise PermissionDenied("User must belong to a company to access this resource")

        company = self.request.user.profile.company
        return Cliente.objects.filter(company=company).order_by("ragionesociale")

    def perform_create(self, serializer):
        """
        Automatically assign the current user's company when creating a cliente
        """
        if not hasattr(self.request.user, 'profile') or not self.request.user.profile.company:
            raise PermissionDenied("User must belong to a company to create a cliente")

        serializer.save(
            created_by=self.request.user,
            company=self.request.user.profile.company
        )

    def perform_update(self, serializer):
        serializer.save()


class FornitoreViewSet(viewsets.ModelViewSet):
    serializer_class = FornitoreSerializer
    filterset_class = FornitoreFilterFE
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter queryset to only show fornitori belonging to the current user's company
        """
        if not hasattr(self.request.user, 'profile') or not self.request.user.profile.company:
            raise PermissionDenied("User must belong to a company to access this resource")

        company = self.request.user.profile.company
        return Fornitore.objects.filter(company=company).order_by("ragionesociale")

    def perform_create(self, serializer):
        """
        Automatically assign the current user's company when creating a fornitore
        """
        if not hasattr(self.request.user, 'profile') or not self.request.user.profile.company:
            raise PermissionDenied("User must belong to a company to create a fornitore")

        serializer.save(
            created_by=self.request.user,
            company=self.request.user.profile.company
        )

    def perform_update(self, serializer):
        serializer.save()
