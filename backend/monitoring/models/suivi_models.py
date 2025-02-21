from django.db import models
from dateutil.relativedelta import relativedelta
from ..models.aspect_models import SousAspectEau,IndicateurEauPollution,Indicateur
from ..models.enterprise_models import ActiviteIndustrielle,Entreprise

class EngagementAspect(models.Model):  
    FREQUENCY_CHOICES = [  
        (1, 'Mensuel (12 fois par an)'),  # 1 mois  
        (2, 'Trimestriel (4 fois par an)'),  # 3 mois  
        (3, 'Semestriel (2 fois par an)'),  # 6 mois  
        (4, 'Bisannuel (1 fois par 2 ans)'),  # 12 mois  
        (5, 'Triennal (1 fois par 3 ans)'),  # 36 mois  
    ]  

    id_engagement_aspect = models.AutoField(primary_key=True)  
    id_entreprise = models.ForeignKey('Entreprise', on_delete=models.CASCADE, related_name='engagements_aspects', null=True, blank=True)  
    id_aspect = models.ForeignKey('Aspect', on_delete=models.CASCADE, null=True, blank=True)  
    id_sous_aspect_eau = models.ForeignKey(SousAspectEau, on_delete=models.CASCADE, null=True, blank=True)  # Rempli si l'aspect est "Eau"

    lieu_prelevement = models.CharField(max_length=255)  
    methode_equipement = models.CharField(max_length=255)  
    frequence = models.IntegerField(choices=FREQUENCY_CHOICES)  # Utilisation des choix pour la fréquence  
    responsabilite = models.CharField(max_length=255)  
    date_creation = models.DateField()  
    date_prochaine_echeance = models.DateField(null=True, blank=True)  

    class Meta:  
        constraints = [  
            models.UniqueConstraint(  
            fields=['id_aspect', 'id_sous_aspect_eau'],  
            name='unique_engagement_aspect_aspect',  
            condition=models.Q(id_sous_aspect_eau__isnull=False)  # Appliquer uniquement si id_sous_aspect_eau est non nul
        )  
    ] 

    def generer_prochaine_echeance(self):  
        """Génère la prochaine échéance et crée un suivi"""  
        self.date_prochaine_echeance = self.calculer_prochaine_date()  
        self.save()  

        if self.date_prochaine_echeance:  
            Suivi.objects.create(  
                id_engagement_aspect=self,  
                date_limite=self.date_prochaine_echeance,  
                statut="en attente"  
            )  

    def calculer_prochaine_date(self):  
        """Calculer la date en fonction de la fréquence"""  
        if self.frequence:  
            # Mapping de la fréquence à des mois  
            frequence_mois = {  
                1: 1,   # Mensuel  
                2: 3,   # Trimestriel  
                3: 6,   # Semestriel  
                4: 12,  # Bisannuel  
                5: 36,  # Triennal  
            }  
            return self.date_creation + relativedelta(months=frequence_mois[self.frequence])  
        return None  
class EngagementIndicateur(models.Model):
    id_engagement_indicateur = models.AutoField(primary_key=True)
    id_indicateur = models.ForeignKey('Indicateur', on_delete=models.CASCADE)
    id_engagement_aspect = models.ForeignKey(EngagementAspect, on_delete=models.CASCADE, null=True, blank=True, related_name='engagements_indicateurs')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id_engagement_aspect', 'id_indicateur'],
                name='unique_engagement_aspect_indicateur'
            )
        ]

class Suivi(models.Model):
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('effectué', 'Effectué'),
        ('effectué_Retard', 'Effectué_Retard'),
    ]

    id_suivi = models.AutoField(primary_key=True)
    id_engagement_aspect = models.ForeignKey(EngagementAspect, on_delete=models.CASCADE, related_name='suivis')
    date_mesure = models.DateField(null=True, blank=True)
    date_limite = models.DateField(null=True, blank=True)
    justificatif_etude = models.FileField(upload_to='justificatifs/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')
    cloturer = models.BooleanField(default=False)  # Nouveau champ

    def mettre_a_jour_statut(self):
        if self.date_mesure:
            if self.date_mesure <= self.date_limite:
                self.statut = "effectué"
            else:
                self.statut = "effectué_Retard"
            self.save()

class SuiviIndicateur(models.Model):
    id_suivi_indicateur = models.AutoField(primary_key=True)
    suivi = models.ForeignKey(Suivi, on_delete=models.CASCADE, related_name='suivi_indicateurs')
    engagement_indicateur = models.ForeignKey(EngagementIndicateur, on_delete=models.CASCADE)
    valeur_mesure = models.FloatField()
    observations = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['suivi', 'engagement_indicateur'],
                name='unique_suivi_engagement_indicateur'
            )
        ]

class EngagementSousAspectEauPollution(models.Model):
    FREQUENCY_CHOICES = [  
        (1, 'Mensuel (12 fois par an)'),  # 1 mois  
        (2, 'Trimestriel (4 fois par an)'),  # 3 mois  
        (3, 'Semestriel (2 fois par an)'),  # 6 mois  
        (4, 'Bisannuel (1 fois par 2 ans)'),  # 12 mois  
        (5, 'Triennal (1 fois par 3 ans)'),  # 36 mois  
    ]  

    id_engagement_sous_aspect = models.AutoField(primary_key=True)
    id_entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    id_sous_aspect = models.ForeignKey(SousAspectEau, on_delete=models.CASCADE)
    lieu_prelevement = models.CharField(max_length=255)
    methode_equipement = models.CharField(max_length=255)
    frequence = models.IntegerField(choices=FREQUENCY_CHOICES)  # Utilisation des choix pour la fréquence  
    responsabilite = models.CharField(max_length=255)
    date_creation = models.DateField()
    date_prochaine_echeance = models.DateField(null=True, blank=True)
    
    class Meta:  
        constraints = [  
            models.UniqueConstraint(  
                fields=['id_sous_aspect'],  
                name='unique_engagement_sous-aspect'  
            )  
        ]  

    def generer_prochaine_echeance(self):  
        """Génère la prochaine échéance et crée un suivi"""  
        self.date_prochaine_echeance = self.calculer_prochaine_date()  
        self.save()  

        if self.date_prochaine_echeance:  
            SuiviSousAspect.objects.create(  
                id_engagement_sous_aspect=self,  
                date_limite=self.date_prochaine_echeance,  
                statut="en attente"  
            )  

    def calculer_prochaine_date(self):  
        """Calculer la date en fonction de la fréquence"""  
        if self.frequence:  
            # Mapping de la fréquence à des mois  
            frequence_mois = {  
                1: 1,   # Mensuel  
                2: 3,   # Trimestriel  
                3: 6,   # Semestriel  
                4: 12,  # Bisannuel  
                5: 36,  # Triennal  
            }  
            return self.date_creation + relativedelta(months=frequence_mois[self.frequence])  
        return None

class EngagementIndicateurSousAspect(models.Model):
    id_engagement_indicateur_sous_aspect = models.AutoField(primary_key=True)
    id_indicateur_eaupollution = models.ForeignKey(IndicateurEauPollution, on_delete=models.CASCADE)
    id_engagement_sous_aspect = models.ForeignKey(EngagementSousAspectEauPollution, on_delete=models.CASCADE, related_name='engagements_indicateurs')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_engagement_sous_aspect', 'id_indicateur_eaupollution'], name='unique_engagement_sous_aspect_indicateur')
        ]
    
    def __str__(self):
        return f"{self.id_engagement_sous_aspect} - {self.id_indicateur.nom}"

class SuiviSousAspect(models.Model):
    id_suivi_sous_aspect = models.AutoField(primary_key=True)
    id_engagement_sous_aspect = models.ForeignKey(EngagementSousAspectEauPollution, on_delete=models.CASCADE, related_name='suivis')
    date_mesure = models.DateField(null=True, blank=True)
    date_limite = models.DateField(null=True, blank=True)
    justificatif_etude = models.FileField(upload_to='justificatifs/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=[('en attente', 'En attente'), ('effectué', 'Effectué'), ('effectué_Retard', 'Effectué_Retard')], default='en attente')
    cloturer = models.BooleanField(default=False)  # Nouveau champ

    def mettre_a_jour_statut(self):
        if self.date_mesure:
            self.statut = 'effectué' if self.date_mesure <= self.date_limite else 'effectué_Retard'
            self.save()

class SuiviIndicateurSousAspect(models.Model):
    id_suivi_indicateur_sous_aspect = models.AutoField(primary_key=True)
    suivi = models.ForeignKey(SuiviSousAspect, on_delete=models.CASCADE, related_name='suivi_indicateurs')
    engagement_indicateur_sous_aspect = models.ForeignKey(EngagementIndicateurSousAspect, on_delete=models.CASCADE)
    valeur_mesure = models.FloatField()
    observations = models.TextField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['suivi', 'engagement_indicateur_sous_aspect'], name='unique_suivi_indicateur_sous_aspect')
        ]
