import smtplib
import ssl
from email.message import EmailMessage
import json
from .models import Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    def send_order_created_notification(self, request, order):

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
                } for item in order.orderitem_set.all()]
            }
        html_message = render_to_string('emails/order_created_notification.html', context)
        plain_message = strip_tags(html_message)
        self.__send_email_notification(request, subject, html_message, plain_message)

    def send_cancel_notification(self, request):
        json_data = json.loads(request.body)
        order_nummer = json_data['order_nummer']

        order = Order.objects.filter(order_nummer=order_nummer, ust_id=request.user.customerprofile.ust_id).first()

        subject = f"Order #{order.order_nummer} has been cancelled!"
        body = f"""
        Your order #{order.order_nummer} has been cancelled.
        """
        plain_message = body
        self.__send_email_notification(request, subject, plain_message, plain_message)

    def send_reorder_notification(self, request):
        json_data = json.loads(request.body)
        order_nummer = json_data['order_nummer']

        order = Order.objects.filter(order_nummer=order_nummer, ust_id=request.user.customerprofile.ust_id).first()

        subject = f"Order #{order.order_nummer} has been reordered!"
        body = f"""
        Your cancelled order #{order.order_nummer} has been reordered again.
        """
        plain_message = body
        self.__send_email_notification(request, subject, plain_message, plain_message)
