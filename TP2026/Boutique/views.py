from django.shortcuts import render
from .models import Client, Produit, Commande, Detail
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .forms  import ClientForm, ProduitForm , CommandeForm, DetailForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required,permission_required


@login_required(login_url='/boutique/login/')
def liste_clients(request):
    data_clients = Client.objects.all()
    return render(request,'Boutique/clients.html',{'clients':data_clients})

@login_required(login_url='/boutique/login/')
def liste_produits(request):
    
    data_produits = Produit.objects.all()
    return render(request, 'Boutique/produits.html', {'produits': data_produits})

@login_required(login_url='/boutique/login/')
def liste_commandes(request):
    
    data_commandes = Commande.objects.select_related('client').all()
    return render(request, 'Boutique/commandes.html', {'commandes': data_commandes})

@login_required(login_url='/boutique/login/')
def liste_details(request):

    data_details = Detail.objects.select_related('commande','produit').all()
    return render(request,'Boutique/details.html',{'details':data_details})








# ... (garder les fonctions existantes) ...

def client_commandes(request,id_client):
    client = get_object_or_404(Client,ncli=id_client)
    commandes = Commande.objects.filter(client=client).prefetch_related('lignes__produit')
    return render(request,'Boutique/client_commandes.html',{'client':client,'commandes':commandes})








# ... (garder toutes les fonctions existantes) ...

# --- CRUD Clients ---

def ajouter_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            Client.objects.create(**form.cleaned_data)
            return redirect('clients')
    else:
        form = ClientForm()
    return render(request, 'Boutique/forms.html',{'form':form, 'titre':"Ajouter un Client"})

@permission_required('Boutique.change_client',login_url='/boutique/login/')

def modifier_client(request,pk):
  client = get_object_or_404(Client, ncli=pk)
  if request.method == "POST":
     form = ClientForm(request.POST)
     if form.is_valid():
        # Mise à jour manuelle pour un Form standard
        Client.objects. filter(ncli=pk). update(**form.cleaned_data)
        return redirect('clients')
  else:
    # On pré-remplit le formulaire avec les données actuelles
    form = ClientForm(initial={
      'ncli': client.ncli, 'nom': client.nom, 'adresse': client.adresse,
      'localite': client.localite, 'cat': client.cat, 'compte': client.compte})
  return render(request, 'Boutique/forms.html', {'form': form, 'titre': "Modifier Client"})

@permission_required('Boutique.delete_client',login_url='/boutique/login/')

def supprimer_client(request,pk):
    client = get_object_or_404(Client, ncli=pk)
    if request.method== "POST":
       client.delete()
       return redirect ('clients')
    return render(request, 'Boutique/delete_confirm.html', {'objet': client, 'type': "le client"})

# --- CRUD Produits ---

def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produits')
    else:
        form = ProduitForm()
    return render(request, 'Boutique/forms.html',
                  {'form': form, 'titre': 'Ajouter un Produit'})

@permission_required('Boutique.change_client',login_url='/boutique/login/')

def modifier_produit(request, pk):
   produit = get_object_or_404(Produit, npro=pk)
   if request.method== "POST":
      # Pour un ModelForm, on passe l'instance à modifier
      form = ProduitForm(request.POST, instance=produit)
      if form.is_valid():
          form.save()
          return redirect ('produits')
   else:
     form = ProduitForm(instance=produit)
   return render(request, 'Boutique/forms.html',{'form': form, 'titre': "Modifier Produit"})


@permission_required('Boutique.delete_produit',login_url='/boutique/login/')

def supprimer_produit(request, pk):
    produit = get_object_or_404(Produit, npro=pk)
    if request.method == "POST":
       produit.delete()
       return redirect('produits')
    return render(request, 'Boutique/delete_confirm.html', {'objet': produit, 'type': "le produit"})
   
    


def ajouter_detail(request):
    if request.method == "POST":
        form = DetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('details')
    else:
            form = DetailForm()
    return render(request,'Boutique/forms.html',{'form':form, 'titre':"Ajouter un Detail"})


@permission_required('Boutique.change_detail',login_url='/boutique/login/')   
  
def modifier_detail(request, ncom, npro):
  #1. On récupère le détail spécifique en utilisant les deux clés étrangères
  detail = get_object_or_404(Detail, commande_id=ncom, produit_id=npro)
  if request.method == "POST":
     form = DetailForm(request.POST, instance=detail)
     if form.is_valid():
        form.save()
        return redirect ('details')
  else:
    form = DetailForm(instance=detail)
  return render(request, 'Boutique/forms.html', {
    'form': form,
    'titre': f"Modifier Ligne (Com: {ncom}, Prod: {npro})"
})

@permission_required('Boutique.delete_detail',login_url='/boutique/login/')
def supprimer_detail(request, ncom, npro):
  # 1. On récupère la ligne de détail
  detail = get_object_or_404(Detail, commande_id=ncom, produit_id=npro)
  if request.method == "POST":
     detail.delete()
     return redirect('details')
  return render(request, 'Boutique/delete_confirm.html', { 
    'objet': detail,
    'type': "cette ligne de commande"
  })


def ajouter_commande(request):
    if request.method == "POST":
        form = CommandeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('commandes')
    else:
        form = CommandeForm()
    return render(request,'Boutique/forms.html',{'form':form, 'titre':"Ajouter un Commande"})

@permission_required('Boutique.change_commande',login_url='/boutique/login/')

def modifier_commande(request, pk):
    # 1. Récupérer la commande existante via sa clé primaire
    commande = get_object_or_404(Commande, ncom=int(pk))
    if request.method == "POST":
        # 2. Lier le formulaire aux données envoyées ET à l'instance existante
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('commandes')
    else:
        # 3. Afficher le formulaire pré-rempli
        form = CommandeForm(instance=commande)
    return render(request, 'Boutique/forms.html', {
        'form': form,
        'titre': f"Modifier la Commande n°{pk}"
    })

@permission_required('Boutique.delete_commande',login_url='/boutique/login/')

def supprimer_commande(request, pk):
    # 1. Récupérer la commande
    commande = get_object_or_404(Commande, ncom=int(pk))
    if request.method == "POST":
        # 2. Supprimer l'objet après confirmation 
        commande.delete()
        return redirect('commandes')
    # 3. Afficher la page de confirmation (réutilisation du template delete_confirm.html)
    return render(request, 'Boutique/delete_confirm.html', {
        'objet': commande,
        'type': "la commande"
    })




#Vue d authentification 

def register(request):
    if request.method == 'POST' :
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('clients')
    else:
        form = RegisterForm()
    return render(request, 'Boutique/auth/register.html',{'form':form})


def connexion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('clients')
    else : 
        form = AuthenticationForm()
    return render(request,'Boutique/auth/login.html',{'form':form})

def deconnexion(request):
    logout(request)
    return redirect('connexion')


 