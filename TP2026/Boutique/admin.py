from django.contrib import admin
from .models import Client, Produit, Commande, Detail


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('ncli', 'nom', 'localite', 'cat', 'compte')
    search_fields = ('ncli', 'nom', 'localite')
    list_filter = ('cat', 'localite')


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('npro', 'libelle', 'prix', 'qstock')
    search_fields = ('npro', 'libelle')


class DetailInline(admin.TabularInline):
    """Lignes d'articles saisies directement dans la commande."""
    model  = Detail
    extra  = 1   # Affiche 1 ligne vide par defaut


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('ncom', 'client', 'datecom')
    list_filter  = ('datecom',)
    search_fields= ('ncom', 'client__nom')
    inlines      = [DetailInline]  # <-- La magie : Detail integre dans Commande