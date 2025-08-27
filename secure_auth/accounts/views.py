from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import SecureLoginForm
from .models import Document
from .mixins import OwnerRequiredMixin, GroupRequiredMixin


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SecureLoginForm(request, data=request.POST)
        if form.is_valid():
            request.session.flush()

            user = form.get_user()
            login(request, user)

            return redirect('dashboard')
        else:
            messages.error(request,"Email ou mot de passe incorrect. Votre compte pourrait être temporairement verrouillé.")
    else:
        form = SecureLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'accounts/document_list.html'

    def get_queryset(self):
        """
        Filtre les documents en fonction des permissions de l'utilisateur.
        """
        # Si l'utilisateur a la permission globale, il voit tout.
        if self.request.user.has_perm('accounts.view_document'):
            return Document.objects.all()
        # Sinon, il voit les documents publics ou ceux dont il est le propriétaire.
        return Document.objects.filter(Q(is_public=True) | Q(owner=self.request.user))

class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'content', 'is_public']
    template_name = 'accounts/document_form.html'
    success_url = reverse_lazy('document_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class DocumentUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Document
    fields = ['title', 'content', 'is_public']
    template_name = 'accounts/document_form.html'
    success_url = reverse_lazy('document_list')

class DocumentDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Document
    template_name = 'accounts/document_confirm_delete.html'
    success_url = reverse_lazy('document_list')

class DocumentPublishView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Document
    fields = ['is_public']
    template_name = 'accounts/document_publish.html'
    success_url = reverse_lazy('document_list')
    groups = ['editors']