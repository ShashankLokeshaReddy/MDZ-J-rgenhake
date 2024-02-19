import smtplib
import ssl
from email.message import EmailMessage
import json
from .models import Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from django.contrib.staticfiles import finders
import os

class NotificationService:
    def __send_email_notification(self, request, subject, html_message, plain_message):
        email_sender = 'jurgenhaketest@gmail.com'
        email_password = 'azuexffmhvurppvu'
        email_receiver = request.user.email

        em = MIMEMultipart('alternative')
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(plain_message, 'plain')
        part2 = MIMEText(html_message, 'html')
        em.attach(part1)
        em.attach(part2)

        # Embed image to email
        img_data = open('media/General/logo.png', 'rb').read()
        logo = MIMEImage(img_data)
        logo.add_header('Content-ID', '<logo>')
        logo.add_header('Content-Disposition', 'inline', filename='logo')
        em.attach(logo)     

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def __send_email_notification_with_attachment(self, request, subject, html_message, plain_message, attachmentFileName):
        email_sender = 'jurgenhaketest@gmail.com'
        email_password = 'azuexffmhvurppvu'
        email_receiver = request.user.email

        em = MIMEMultipart('alternative')
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(plain_message, 'plain')
        part2 = MIMEText(html_message, 'html')
        em.attach(part1)
        em.attach(part2)

        # Embed image to email
        img_data = open('media/General/logo.png', 'rb').read()
        logo = MIMEImage(img_data)
        logo.add_header('Content-ID', '<logo>')
        logo.add_header('Content-Disposition', 'inline', filename='logo')
        em.attach(logo)     

        # locate and attach desired attachments
        att_name = os.path.basename(attachmentFileName)
        _f = open(attachmentFileName, 'rb')
        att = MIMEApplication(_f.read(), _subtype="txt")
        _f.close()
        att.add_header('Content-Disposition', 'attachment', filename=att_name)
        em.attach(att)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def send_order_created_notification(self, request, order, ui_labels):
        email_body_firma_name = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-name'), '')
        firma_adresse_1 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'firma-adresse-1'), '')
        firma_adresse_2 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'firma-adresse-2'), '')
        email_body_ordering_text = next((label['label_value'] for label in ui_labels if label['label_key'] == 'E-Mail-Body-Ordering-text'), '')
        email_body_fon = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-fon'), '')
        email_body_mob = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-mob'), '')
        email_body_fax = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-fax'), '')
        email_body_email = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-email'), '')
        email_body_firma_1 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-1'), '')
        email_body_firma_2 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-2'), '')
        subject = f'Eingangsbestätigung und Übersicht Ihrer Bestellung: "{order.order_nummer}"'
        context = {
            'order_nummer': order.order_nummer,
            'ust_id': order.ust_id,
            'order_datum': order.order_datum,
            'bestelldetails': order.bestelldetails,
            'order_status' : order.order_status,
            'last_name': request.user.last_name,
            'gesamt': sum([item.gesamt for item in order.orderitem_set.all()]),
            'items': [{
                    'item_nummer': item.item_nummer,
                    'mit_120_Ohm_CAN_Bus_Widerstand': item.mit_120_Ohm_CAN_Bus_Widerstand,
                    'akkuvariante': item.akkuvariante,
                    'kabelvariante': item.kabelvariante,
                    'schnittstelle': item.schnittstelle,
                    'masse': item.masse,
                    'menge': item.menge,
                    'original_preis': item.original_preis,
                    'reduzierter_preis': item.reduzierter_preis,
                    'gesamt': item.gesamt
                } for item in order.orderitem_set.all()],
            'email_body_firma_name': email_body_firma_name,
            'firma_adresse_1': firma_adresse_1,
            'firma_adresse_2': firma_adresse_2,
            'email_body_ordering_text': email_body_ordering_text,
            'email_body_fon': email_body_fon,
            'email_body_mob': email_body_mob,
            'email_body_fax': email_body_fax,
            'email_body_email': email_body_email,
            'email_body_firma_1': email_body_firma_1,
            'email_body_firma_2': email_body_firma_2,
        }
        html_message = render_to_string('emails/order_created_notification.html', context)
        plain_message = strip_tags(html_message)
        self.__send_email_notification(request, subject, html_message, plain_message)
    
    def send_offer_requested_notification(self, request, order, ui_labels):
        email_body_firma_name = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-name'), '')
        firma_adresse_1 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'firma-adresse-1'), '')
        firma_adresse_2 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'firma-adresse-2'), '')
        email_body_offer_text = next((label['label_value'] for label in ui_labels if label['label_key'] == 'E-Mail-Body-Offer-text'), '')
        email_body_fon = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-fon'), '')
        email_body_mob = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-mob'), '')
        email_body_fax = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-fax'), '')
        email_body_email = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-email'), '')
        email_body_firma_1 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-1'), '')
        email_body_firma_2 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-2'), '')
        subject = f'Eingangsbestätigung der Angebotsanfrage'
        context = {
            'order_nummer': order.order_nummer,
            'ust_id': order.ust_id,
            'order_datum': order.order_datum,
            'bestelldetails': order.bestelldetails,
            'order_status' : order.order_status,
            'last_name': request.user.last_name,
            'gesamt': sum([item.gesamt for item in order.orderitem_set.all()]),
            'items': [{
                    'item_nummer': item.item_nummer,
                    'mit_120_Ohm_CAN_Bus_Widerstand': item.mit_120_Ohm_CAN_Bus_Widerstand,
                    'akkuvariante': item.akkuvariante,
                    'kabelvariante': item.kabelvariante,
                    'schnittstelle': item.schnittstelle,
                    'masse': item.masse,
                    'menge': item.menge,
                    'original_preis': item.original_preis,
                    'reduzierter_preis': item.reduzierter_preis,
                    'gesamt': item.gesamt
                } for item in order.orderitem_set.all()],
            'email_body_firma_name': email_body_firma_name,
            'firma_adresse_1': firma_adresse_1,
            'firma_adresse_2': firma_adresse_2,
            'email_body_offer_text': email_body_offer_text,
            'email_body_fon': email_body_fon,
            'email_body_mob': email_body_mob,
            'email_body_fax': email_body_fax,
            'email_body_email': email_body_email,
            'email_body_firma_1': email_body_firma_1,
            'email_body_firma_2': email_body_firma_2,
        }
        html_message = render_to_string('emails/offer_requested_notification.html', context)
        plain_message = strip_tags(html_message)
        self.__send_email_notification(request, subject, html_message, plain_message)

    def send_special_order_notification(self, request, special_order, ui_labels):
        email_body_firma_name = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-name'), '')
        firma_adresse_1 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'firma-adresse-1'), '')
        firma_adresse_2 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'firma-adresse-2'), '')
        email_body_special_solution_text = next((label['label_value'] for label in ui_labels if label['label_key'] == 'E-Mail-Body-Special-Solution-text'), '')
        email_body_fon = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-fon'), '')
        email_body_mob = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-mob'), '')
        email_body_fax = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-fax'), '')
        email_body_email = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-email'), '')
        email_body_firma_1 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-1'), '')
        email_body_firma_2 = next((label['label_value'] for label in ui_labels if label['label_key'] == 'email-body-firma-2'), '')

        subject = f'Eingangsbestätigung_Sonderlösung'
        context = {
            'last_name': request.user.last_name,
            'email_body_firma_name': email_body_firma_name,
            'firma_adresse_1': firma_adresse_1,
            'firma_adresse_2': firma_adresse_2,
            'email_body_special_solution_text': email_body_special_solution_text,
            'email_body_fon': email_body_fon,
            'email_body_mob': email_body_mob,
            'email_body_fax': email_body_fax,
            'email_body_email': email_body_email,
            'email_body_firma_1': email_body_firma_1,
            'email_body_firma_2': email_body_firma_2,
        }
        html_message = render_to_string('emails/special_order_created_notification.html', context)
        plain_message = strip_tags(html_message)
        self.__send_email_notification_with_attachment(request, subject, html_message, plain_message, special_order.hochgeladene_datei.path)

    def send_cancel_notification(self, request):
        json_data = json.loads(request.body)
        order_nummer = json_data['order_nummer']

        order = Order.objects.filter(order_nummer=order_nummer, ust_id=request.user.customerprofile.ust_id).first()

        subject = f"Bestellung #{order.order_nummer} wurde storniert!"
        body = f"""
        Ihre Bestellung #{order.order_nummer} wurde storniert.
        """
        plain_message = body
        self.__send_email_notification(request, subject, plain_message, plain_message)

    def send_reorder_notification(self, request):
        json_data = json.loads(request.body)
        order_nummer = json_data['order_nummer']

        order = Order.objects.filter(order_nummer=order_nummer, ust_id=request.user.customerprofile.ust_id).first()

        subject = f"Bestellung #{order.order_nummer} wurde nachbestellt!"
        body = f"""
        Ihre stornierte Bestellung #{order.order_nummer} wurde erneut bestellt.
        """
        plain_message = body
        self.__send_email_notification(request, subject, plain_message, plain_message)
