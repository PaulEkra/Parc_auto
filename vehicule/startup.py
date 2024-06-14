import time
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F

from Model.models import Vehicule
from twilio.rest import Client


def envoyer_emails_assurance_vehicules():
    destinaires = ["infos@glaroche.com"]
    date_actuelle = datetime.now().date()
    une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    vehicules_avec_assurance_expiree = Vehicule.objects.filter(date_expiration_assurance__lt=date_actuelle)
    vehicules_proches_expiration = Vehicule.objects.filter(
        date_expiration_assurance__gte=date_actuelle, date_expiration_assurance__lte=une_semaine_plus_tard
    ).exclude(id__in=vehicules_avec_assurance_expiree)

    if vehicules_avec_assurance_expiree:
        sujet_assurance_expiree = "Véhicules avec assurance déjà expirée"
        message_assurance_expiree = "Voici la liste des véhicules avec une assurance déjà expirée :\n\n"

        for vehicule in vehicules_avec_assurance_expiree:
            jours_depuis_expiration = (date_actuelle - vehicule.date_expiration_assurance).days
            message_assurance_expiree += f"- Véhicule {vehicule} : L'assurance est déjà expirée depuis {jours_depuis_expiration} jours\n"

        try:
            send_mail(
                sujet_assurance_expiree,
                message_assurance_expiree,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec assurance expirée envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec assurance expirée : {e}")

    if vehicules_proches_expiration:
        sujet_proches_expiration = "Véhicules avec assurance expirant bientôt"
        message_proches_expiration = "Voici la liste des véhicules avec une assurance expirant dans les 3 prochains jours ou moins:\n\n"

        for vehicule in vehicules_proches_expiration:
            jours_restants = (vehicule.date_expiration_assurance - date_actuelle).days
            message_proches_expiration += f"- Véhicule {vehicule} : {jours_restants} jours restants\n"

        try:
            send_mail(
                sujet_proches_expiration,
                message_proches_expiration,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec assurance expirant bientôt envoyé avec succès")
        except Exception as e:
            print(
                f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec assurance expirant bientôt : {e}")

    if not vehicules_avec_assurance_expiree and not vehicules_proches_expiration:
        print("Aucun véhicule avec assurance expirée ou expirant bientôt trouvé.")


def envoyer_emails_visite_vehicules():
    destinaires = ["infos@glaroche.com"]
    date_actuelle = datetime.now().date()
    une_demi_semaine_plus_tard = date_actuelle + timedelta(days=3)

    vehicules_proches_expiration_technique = Vehicule.objects.filter(date_visite_technique__lt=date_actuelle)
    vehicules_proches_expiration = Vehicule.objects.filter(
        date_visite_technique__gte=date_actuelle, date_visite_technique__lte=une_demi_semaine_plus_tard
    ).exclude(id__in=vehicules_proches_expiration_technique)

    if vehicules_proches_expiration_technique.exists():
        sujet_visite_expiree = "Véhicules avec date de visite dépassée"
        message_visite_expiree = "Voici la liste des véhicules avec une date de visite dépassée :\n\n"

        for vehicule in vehicules_proches_expiration_technique:
            jours_depuis_expiration = (date_actuelle - vehicule.date_visite_technique).days
            message_visite_expiree += f"- Véhicule {vehicule} : La visite est déjà dépassée depuis {jours_depuis_expiration} jours\n"


        try:
            send_mail(
                sujet_visite_expiree,
                message_visite_expiree,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec visite dépassée envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec visite dépassée : {e}")

    if vehicules_proches_expiration.exists():
        sujet_proches_expiration = "Véhicules avec visite à faire bientôt"
        message_proches_expiration = "Voici la liste des véhicules avec une visite à faire dans les 3 prochains jours " \
                                     ":\n\n"

        for vehicule in vehicules_proches_expiration:
            jours_restants = (vehicule.date_visite_technique - date_actuelle).days
            message_proches_expiration += f"- Véhicule {vehicule} : {jours_restants} jours restants\n"


        try:
            send_mail(
                sujet_proches_expiration,
                message_proches_expiration,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec visite technique expirant bientôt envoyé avec succès")
        except Exception as e:
            print(
                f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec visite technique expirant bientôt : {e}")

    if not vehicules_proches_expiration_technique.exists() and not vehicules_proches_expiration.exists():
        print("Aucun véhicule avec date de visite dépassée ou arrivant bientôt trouvé.")


def envoyer_emails_vehicules_proches_vidange():
    destinaires = ["infos@glaroche.com"]
    vehicules_proches_vidanges = Vehicule.objects.filter(kilometrage__lte=F('videnge') - 100)
    vehicules_vidanges = Vehicule.objects.filter(kilometrage__gte=F('videnge'))
    if vehicules_proches_vidanges.exists():
        sujet_vidange_proche = "Véhicules proches de la vidange"
        message_vidange_proche = "Voici la liste des véhicules qui sont proches de la vidange :\n\n"

        for vehicule in vehicules_proches_vidanges:
            kilometrage_restant = vehicule.videnge - vehicule.kilometrage
            message_vidange_proche += f"- Véhicule {vehicule} : Il reste {kilometrage_restant} km avant la vidange\n"

        try:
            send_mail(
                sujet_vidange_proche,
                message_vidange_proche,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules proches de la vidange envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules proches de la vidange : {e}")
    elif vehicules_vidanges.exists():
        sujet_vidange = "Véhicules devant faire leur vidange"
        message_vidange = "Voici la liste des véhicules qui doivent faire leur vidange :\n\n"

        for vehicule in vehicules_vidanges:
            message_vidange += f"- Véhicule {vehicule} \n"

        try:
            send_mail(
                sujet_vidange,
                message_vidange,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules devant faire leur vidange envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules devant faire leur vidange : {e}")

    else:
        print("Aucun véhicule proche de la vidange ou devant faire leur vidange trouvé.")


def envoyer_emails_recepisse_vehicules():
    destinaires = ["infos@glaroche.com"]
    date_actuelle = datetime.now().date()
    une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    vehicules_avec_recepisse_expiree = Vehicule.objects.filter(date_limite_recepisse__lt=date_actuelle)
    vehicules_proches_expiration = Vehicule.objects.filter(
        date_limite_recepisse__gte=date_actuelle, date_limite_recepisse__lte=une_semaine_plus_tard
    ).exclude(id__in=vehicules_avec_recepisse_expiree)

    if vehicules_avec_recepisse_expiree:
        sujet_recepisse_expiree = "Véhicules avec recepissé déjà expirée"
        message_recepisse_expiree = "Voici la liste des véhicules avec un recepissé déjà expirée :\n\n"

        for vehicule in vehicules_avec_recepisse_expiree:
            jours_depuis_expiration = (date_actuelle - vehicule.date_limite_recepisse).days
            message_recepisse_expiree += f"- Véhicule {vehicule} : Le recepissé est déjà expirée depuis {jours_depuis_expiration} jours\n"

        try:
            send_mail(
                sujet_recepisse_expiree,
                message_recepisse_expiree,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec recepissé expiré envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec recepissé expirée : {e}")

    if vehicules_proches_expiration:
        sujet_proches_expiration = "Véhicules avec recepissé expirant bientôt"
        message_proches_expiration = "Voici la liste des véhicules avec un recepissé expirant dans les 3 prochains " \
                                     "jours ou moins:\n\n"

        for vehicule in vehicules_proches_expiration:
            jours_restants = (vehicule.date_limite_recepisse - date_actuelle).days
            message_proches_expiration += f"- Véhicule {vehicule} : {jours_restants} jours restants\n"

        try:
            send_mail(
                sujet_proches_expiration,
                message_proches_expiration,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec recepissé expirant bientôt envoyé avec succès")
        except Exception as e:
            print(
                f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec recepissé expirant bientôt : {e}")

    if not vehicules_avec_recepisse_expiree and not vehicules_proches_expiration:
        print("Aucun véhicule avec recepissé expirée ou expirant bientôt trouvé.")


def envoyer_emails_assurance_carteBrune_vehicules():
    destinaires = ["infos@glaroche.com"]
    date_actuelle = datetime.now().date()
    une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    vehicules_avec_assurance_carteBrune_expiree = Vehicule.objects.filter(
        date_limite_assurance_carteBrune__lt=date_actuelle)
    vehicules_proches_expiration = Vehicule.objects.filter(
        date_limite_assurance_carteBrune__gte=date_actuelle, date_limite_assurance_carteBrune__lte=une_semaine_plus_tard
    ).exclude(id__in=vehicules_avec_assurance_carteBrune_expiree)

    if vehicules_avec_assurance_carteBrune_expiree:
        sujet_assurance_carteBrune_expiree = "Véhicules avec assurance carte Brune déjà expirée"
        message_assurance_carteBrune_expiree = "Voici la liste des véhicules avec un recepissé déjà expirée :\n\n"

        for vehicule in vehicules_avec_assurance_carteBrune_expiree:
            jours_depuis_expiration = (date_actuelle - vehicule.date_limite_assurance_carteBrune).days
            message_assurance_carteBrune_expiree += f"- Véhicule {vehicule} : L'assurance carte Brune est déjà expirée depuis {jours_depuis_expiration} jours\n"

        try:
            send_mail(
                sujet_assurance_carteBrune_expiree,
                message_assurance_carteBrune_expiree,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec assurance carte Brune expiré envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec assurance carte Brune "
                  f"expirée : {e}")

    if vehicules_proches_expiration:
        sujet_proches_expiration = "Véhicules avec assurance carteBrune expirant bientôt"
        message_proches_expiration = "Voici la liste des véhicules avec une assurance carteBrune expirant dans les 3 " \
                                     "prochains jours ou moins:\n\n"

        for vehicule in vehicules_proches_expiration:
            jours_restants = (vehicule.date_limite_assurance_carteBrune - date_actuelle).days
            message_proches_expiration += f"- Véhicule {vehicule} : {jours_restants} jours restants\n"

        try:
            send_mail(
                sujet_proches_expiration,
                message_proches_expiration,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec assurance carteBrune expirant bientôt envoyé avec succès")
        except Exception as e:
            print(
                f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec assurance carteBrune "
                f"expirant bientôt : {e}")

    if not vehicules_avec_assurance_carteBrune_expiree and not vehicules_proches_expiration:
        print("Aucun véhicule avec assurance carteBrune expirée ou expirant bientôt trouvé.")


def envoyer_emails_taxe_vehicules():
    destinaires = ["infos@glaroche.com"]
    date_actuelle = datetime.now().date()
    une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    vehicules_avec_taxe_expires = Vehicule.objects.filter(
        date_limite_taxe__lt=date_actuelle)
    vehicules_proches_expiration = Vehicule.objects.filter(
        date_limite_taxe__gte=date_actuelle, date_limite_taxe__lte=une_semaine_plus_tard
    ).exclude(id__in=vehicules_avec_taxe_expires)

    if vehicules_avec_taxe_expires:
        sujet_taxe = "Véhicules avec taxes impayées"
        message_taxe = "Voici la liste des véhicules  :\n\n"

        for vehicule in vehicules_avec_taxe_expires:
            jours_depuis_expiration = (date_actuelle - vehicule.date_limite_taxe).days
            message_taxe += f"- Véhicule {vehicule} : La date limite de la taxe est déjà expirée depuis {jours_depuis_expiration} jours\n"

        try:
            send_mail(
                sujet_taxe,
                message_taxe,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec taxes expirées envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec taxes expirées "
                  f"expirée : {e}")

    if vehicules_proches_expiration:
        sujet_proches_expiration = "Véhicules avec date limite de taxe expirant bientôt"
        message_proches_expiration = "Voici la liste des véhicules avec une date limite de taxe expirant dans les 3 " \
                                     "prochains jours ou moins:\n\n"

        for vehicule in vehicules_proches_expiration:
            jours_restants = (vehicule.date_limite_taxe - date_actuelle).days
            message_proches_expiration += f"- Véhicule {vehicule} : {jours_restants} jours restants\n"

        try:
            send_mail(
                sujet_proches_expiration,
                message_proches_expiration,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec taxes  expirant bientôt envoyé avec succès")
        except Exception as e:
            print(
                f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec taxes "
                f"expirant bientôt : {e}")

    if not vehicules_avec_taxe_expires and not vehicules_proches_expiration:
        print("Aucun véhicule avec date limite de taxe expirée ou expirant bientôt trouvé.")


def envoyer_emails_certificatVignette_vehicules():
    destinaires = ["infos@glaroche.com"]
    date_actuelle = datetime.now().date()
    une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    vehicules_avec_certificatVignette_expires = Vehicule.objects.filter(
        date_limite_certificatVignette__lt=date_actuelle)
    vehicules_proches_expiration = Vehicule.objects.filter(
        date_limite_certificatVignette__gte=date_actuelle, date_limite_certificatVignette__lte=une_semaine_plus_tard
    ).exclude(id__in=vehicules_avec_certificatVignette_expires)

    if vehicules_avec_certificatVignette_expires:
        sujet_certificatVignette = "Véhicules avec certificat Vignette expires"
        message_certificatVignette = "Voici la liste des véhicules  :\n\n"

        for vehicule in vehicules_avec_certificatVignette_expires:
            message_certificatVignette += f"- Véhicule {vehicule} \n"

        try:
            send_mail(
                sujet_certificatVignette,
                message_certificatVignette,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec certificat Vignette expirées envoyé avec succès")
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec certificat Vignette expirées "
                  f"expirée : {e}")

    if vehicules_proches_expiration:
        sujet_proches_expiration = "Véhicules avec date limite de certificat Vignette expirant bientôt"
        message_proches_expiration = "Voici la liste des véhicules avec un certificat Vignette expirant dans les 3 " \
                                     "prochains jours ou moins:\n\n"

        for vehicule in vehicules_proches_expiration:
            jours_restants = (vehicule.date_limite_certificatVignette - date_actuelle).days
            message_proches_expiration += f"- Véhicule {vehicule} : {jours_restants} jours restants\n"

        try:
            send_mail(
                sujet_proches_expiration,
                message_proches_expiration,
                settings.EMAIL_HOST_USER,
                destinaires,
                fail_silently=False,
            )
            print("Email pour véhicules avec certificat Vignette  expirant bientôt envoyé avec succès")
        except Exception as e:
            print(
                f"Une erreur est survenue lors de l'envoi de l'email pour véhicules avec certificat Vignette "
                f"expirant bientôt : {e}")

    if not vehicules_avec_certificatVignette_expires and not vehicules_proches_expiration:
        print("Aucun véhicule avec certificat Vignette expirée ou expirant bientôt trouvé.")


# def envoyer_sms(message, destinataire):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     max_length = 1600  # Twilio SMS message length limit
#
#     # Split message into chunks of max_length
#     chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]
#
#     for chunk in chunks:
#         try:
#             message = client.messages.create(
#                 body=chunk,
#                 from_=settings.TWILIO_PHONE_NUMBER,
#                 to=destinataire
#             )
#             print(f"SMS sent successfully to {destinataire}")
#         except Exception as e:
#             print(f"An error occurred when sending SMS to {destinataire}: {e}")
#
#
# def envoyer_notifications_assurance_vehicules():
#     date_actuelle = datetime.now().date()
#     une_semaine_plus_tard = date_actuelle + timedelta(days=3)
#
#     vehicules_avec_assurance_expiree = Vehicule.objects.filter(date_expiration_assurance__lt=date_actuelle)
#     vehicules_proches_expiration = Vehicule.objects.filter(
#         date_expiration_assurance__gte=date_actuelle, date_expiration_assurance__lte=une_semaine_plus_tard
#     ).exclude(id__in=vehicules_avec_assurance_expiree)
#
#     if vehicules_avec_assurance_expiree:
#         message_assurance_expiree = "Voici la liste des véhicules avec une assurance déjà expirée :\n\n"
#
#         for vehicule in vehicules_avec_assurance_expiree:
#             jours_depuis_expiration = (date_actuelle - vehicule.date_expiration_assurance).days
#             message_assurance_expiree += f"- Véhicule {vehicule.id} : L'assurance est déjà expirée depuis {jours_depuis_expiration} jours\n"
#
#         destinataire_assurance_expiree = "+2250153314972"  # Remplacez par le numéro de téléphone du destinataire
#         envoyer_sms(message_assurance_expiree, destinataire_assurance_expiree)
#
#     if vehicules_proches_expiration:
#         message_proches_expiration = "Voici la liste des véhicules avec une assurance expirant dans les 3 prochains jours :\n\n"
#
#         for vehicule in vehicules_proches_expiration:
#             jours_restants = (vehicule.date_expiration_assurance - date_actuelle).days
#             message_proches_expiration += f"- Véhicule {vehicule.id} : {jours_restants} jours restants\n"
#
#         destinataire_proches_expiration = "+2250153314972"  # Remplacez par le numéro de téléphone du destinataire
#         envoyer_sms(message_proches_expiration, destinataire_proches_expiration)
#
#     if not vehicules_avec_assurance_expiree and not vehicules_proches_expiration:
#         print("Aucun véhicule avec assurance expirée ou expirant bientôt trouvé.")
#

def start_scheduler():
    target_hour = 00
    target_minute = 00
    while True:
        now = datetime.now()
        if now.hour == target_hour and now.minute == target_minute:
            # envoyer_notifications_assurance_vehicules()
            envoyer_emails_assurance_vehicules()
            envoyer_emails_visite_vehicules()
            envoyer_emails_vehicules_proches_vidange()
            envoyer_emails_recepisse_vehicules()
            envoyer_emails_assurance_carteBrune_vehicules()
            envoyer_emails_taxe_vehicules()
            envoyer_emails_certificatVignette_vehicules()

            # Attendre 24 heures avant de vérifier à nouveau
            time.sleep(24 * 60 * 60)
        time.sleep(30)  # Vérifie toutes les 30 secondes
