import uuid
from pathlib import Path
from django.conf import settings
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SubscriptionPlan, UserSubscription, Transaction
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer, TransactionSerializer
from .fintech_service import FintechPaymentService

class PlanListView(generics.ListAPIView):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Auto-seed standard credit plans if not present
        if not SubscriptionPlan.objects.exists():
            desc = "Une candidature complète ou CV uniquement vaut 1 crédit, une modification de candidature vaut 1 crédit."
            SubscriptionPlan.objects.create(code='CREDIT_1', name='Formule Parc 1 Crédit à 200 FRS', price_fcfa=200, credits_included=1, description=desc)
            SubscriptionPlan.objects.create(code='CREDIT_5', name='Formule de 5 Crédits à 500 FRS', price_fcfa=500, credits_included=5, description=desc)
            SubscriptionPlan.objects.create(code='CREDIT_25', name='Formule de 25 Crédits à 1000 FRS', price_fcfa=1000, credits_included=25, description=desc)
        return SubscriptionPlan.objects.all().order_by('price_fcfa')

class UserSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sub, _ = UserSubscription.objects.get_or_create(user=request.user)
        return Response(UserSubscriptionSerializer(sub).data)

class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        payment_method = request.data.get('payment_method')
        phone_number = request.data.get('phone_number', '')

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Plan d'abonnement introuvable."}, status=status.HTTP_404_NOT_FOUND)

        # Validation du prefixe du numero de telephone
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        if payment_method == 'AIRTEL_MONEY':
            # Doit commencer par 05 (apres d'éventuels indicatifs pays comme 24205...)
            if not clean_phone.startswith('05') and not clean_phone.startswith('24205'):
                return Response(
                    {"error": "Le numéro Airtel Money doit commencer par 05 (ex: 05XXXXXXX ou +24205XXXXXXX)."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif payment_method == 'MTN_MOMO':
            # Doit commencer par 06 (apres d'éventuels indicatifs pays comme 24206...)
            if not clean_phone.startswith('06') and not clean_phone.startswith('24206'):
                return Response(
                    {"error": "Le numéro MTN Mobile Money doit commencer par 06 (ex: 06XXXXXXX ou +24206XXXXXXX)."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        tx_ref = f"TX-{uuid.uuid4().hex[:10].upper()}"

        tx = Transaction.objects.create(
            user=request.user,
            plan=plan,
            payment_method=payment_method,
            phone_number=phone_number,
            amount_fcfa=plan.price_fcfa,
            transaction_ref=tx_ref,
            status='PENDING'
        )

        fintech_res = {}
        if payment_method == 'AIRTEL_MONEY':
            fintech_res = FintechPaymentService.process_airtel_money_push(phone_number, plan.price_fcfa, tx_ref)
        elif payment_method == 'MTN_MOMO':
            fintech_res = FintechPaymentService.process_mtn_momo_push(phone_number, plan.price_fcfa, tx_ref)
        elif payment_method in ['PAYDUNYA', 'SANKMONEY']:
            fintech_res = FintechPaymentService.process_paydunya_card(phone_number, plan.price_fcfa, tx_ref)

        tx.status = 'SUCCESS'
        receipt_dir = Path(settings.MEDIA_ROOT) / 'receipts'
        receipt_dir.mkdir(parents=True, exist_ok=True)
        receipt_path = str(receipt_dir / f"receipt_{tx_ref}.pdf")

        FintechPaymentService.generate_receipt_pdf(tx, receipt_path)
        tx.receipt_pdf = f"receipts/receipt_{tx_ref}.pdf"
        tx.save()

        sub, _ = UserSubscription.objects.get_or_create(user=request.user)
        sub.plan = plan
        sub.credits_remaining += plan.credits_included
        sub.save()

        return Response({
            "message": "Paiement effectué avec succès.",
            "transaction": TransactionSerializer(tx).data,
            "fintech": fintech_res,
            "credits_remaining": sub.credits_remaining
        }, status=status.HTTP_201_CREATED)
