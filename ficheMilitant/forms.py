from django import forms
from .models import FicheMilitant, EnquetePolitique

class FicheMilitantForm(forms.ModelForm):
    class Meta:
        model = FicheMilitant
        exclude = ['enqueteur']  # Exclure le champ enqueteur du formulaire
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'sexe': forms.Select(),
            'inscription_electorale': forms.RadioSelect(),

            # Checkboxes pour les documents
            'a_cni': forms.CheckboxInput(),
            'a_attestation': forms.CheckboxInput(),
            'a_certificat': forms.CheckboxInput(),
            'a_extrait': forms.CheckboxInput(),
            'a_recepisse': forms.CheckboxInput(),
            'aucune_piece': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Champs obligatoires selon le PDF (marqués avec *)
        required_fields = [
            'region', 'departement_administratif', 'departement', 'zone',
            'section', 'comite_base', 'lieu_vote',
            'prenoms', 'nom', 'date_naissance', 'contacts', 'sexe', 'profession'
        ]

        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                self.fields[field_name].widget.attrs['required'] = True

        # Personnalisation des labels
        self.fields['prenoms'].widget.attrs['placeholder'] = 'Ex: Jean Baptiste'
        self.fields['nom'].widget.attrs['placeholder'] = 'Ex: KOUASSI'
        self.fields['contacts'].widget.attrs['placeholder'] = 'Ex: +225 07 XX XX XX XX'
        self.fields['email'].widget.attrs['placeholder'] = 'Ex: nom@email.com'
        self.fields['numero_piece'].widget.attrs['placeholder'] = 'Numéro du document d\'identité'
        self.fields['numero_carte_electeur'].widget.attrs['placeholder'] = 'Numéro de la carte d\'électeur'
        self.fields['nni'].widget.attrs['placeholder'] = 'Numéro d\'Identification Unique'

# Garder l'ancien formulaire pour compatibilité
class EnquetePolitiqueForm(forms.ModelForm):
    class Meta:
        model = EnquetePolitique
        exclude = ['enqueteur']
        widgets = {
            "commune": forms.Select(),
            "attentes": forms.Textarea(attrs={"rows": 4}),
            "age": forms.NumberInput(attrs={"min": 18}),
            "sexe": forms.Select(),
            "niveau_etudes": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['prenom', 'nom', 'age', 'sexe', 'contact', 'profession',
                           'region', 'commune', 'lieu_vote', 'parti', 'candidat']

        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                self.fields[field_name].widget.attrs['required'] = True