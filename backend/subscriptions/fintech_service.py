import uuid
from pdf_generator.service import PDFService

class FintechPaymentService:
    @staticmethod
    def process_airtel_money_push(phone_number, amount, ref):
        return {
            'status': 'SUCCESS',
            'gateway_reference': f"AIRTEL-{uuid.uuid4().hex[:8].upper()}",
            'message': f"Demande USSD Push envoyée au numéro {phone_number} pour {amount} FCFA."
        }

    @staticmethod
    def process_mtn_momo_push(phone_number, amount, ref):
        return {
            'status': 'SUCCESS',
            'gateway_reference': f"MOMO-{uuid.uuid4().hex[:8].upper()}",
            'message': f"Invitation de paiement MoMo envoyée au {phone_number}."
        }

    @staticmethod
    def process_paydunya_card(phone_number, amount, ref):
        return {
            'status': 'SUCCESS',
            'gateway_reference': f"PAYDUNYA-{uuid.uuid4().hex[:8].upper()}",
            'checkout_url': f"https://paydunya.com/checkout/{ref}"
        }

    @staticmethod
    def generate_receipt_pdf(transaction, output_path):
        receipt_data = {
            'name': f"REÇU DE PAIEMENT #{transaction.transaction_ref}",
            'company_name': f"Méthode: {transaction.payment_method}",
            'job_title': f"Montant: {transaction.amount_fcfa} FCFA",
            'city': transaction.phone_number or "Congo",
            'date': transaction.created_at.strftime("%d/%m/%Y %H:%M"),
            'letter_body': (
                f"Client : {transaction.user.username} ({transaction.user.email})\n\n"
                f"Forfait souscrit : {transaction.plan.name}\n"
                f"Nombre de crédits ajoutés : {transaction.plan.credits_included}\n"
                f"Statut : {transaction.status}\n\n"
                f"Merci pour votre confiance sur AI JobApply SaaS."
            )
        }
        PDFService.generate_cover_letter_pdf(receipt_data, output_path)
        return output_path
