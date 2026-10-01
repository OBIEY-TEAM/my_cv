import React, { useState } from 'react';
import { ApiService } from '../services/api';
import { SubscriptionPlan } from '../types';

interface PaymentsTabProps {
  availablePlans: SubscriptionPlan[];
  selectedPlan: number;
  setSelectedPlan: (id: number) => void;
  onSuccess: () => void;
}

export const PaymentsTab: React.FC<PaymentsTabProps> = ({
  availablePlans,
  selectedPlan,
  setSelectedPlan,
  onSuccess
}) => {
  const [paymentMethod, setPaymentMethod] = useState<'AIRTEL_MONEY' | 'MTN_MOMO'>('AIRTEL_MONEY');
  const [phoneNumber, setPhoneNumber] = useState('056130118');
  const [paymentSuccessMsg, setPaymentSuccessMsg] = useState<string | null>(null);
  const [paymentErrorMsg, setPaymentErrorMsg] = useState<string | null>(null);

  const handlePayment = async () => {
    setPaymentSuccessMsg(null);
    setPaymentErrorMsg(null);

    const cleanPhone = phoneNumber.replace(/\D/g, '');
    if (paymentMethod === 'AIRTEL_MONEY' && !cleanPhone.startsWith('05') && !cleanPhone.startsWith('24205')) {
      setPaymentErrorMsg("Pour Airtel Money, le numéro doit commencer par 05 (ex: 05XXXXXXX).");
      return;
    }
    if (paymentMethod === 'MTN_MOMO' && !cleanPhone.startsWith('06') && !cleanPhone.startsWith('24206')) {
      setPaymentErrorMsg("Pour Mobile Money (MTN), le numéro doit commencer par 06 (ex: 06XXXXXXX).");
      return;
    }

    try {
      await ApiService.makePayment(selectedPlan, paymentMethod, phoneNumber);
      const selectedPlanObj = availablePlans.find(p => p.id === selectedPlan);
      setPaymentSuccessMsg(`Achat réussi via ${paymentMethod === 'AIRTEL_MONEY' ? 'Airtel Money' : 'Mobile Money (MTN)'} ! Vos ${selectedPlanObj?.applications_limit || ''} crédits ont été rechargés.`);
      onSuccess();
    } catch (e: any) {
      const errMsg = e?.response?.data?.error || "Échec de la transaction Fintech Mobile Money.";
      setPaymentErrorMsg(errMsg);
    }
  };

  return (
    <div style={{ maxWidth: '1024px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <div style={{ textAlign: 'center' }}>
        <h2 style={{ fontSize: '28px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Formules d'Abonnement</h2>
      </div>
      {paymentSuccessMsg && (
        <div style={{ backgroundColor: '#ecfdf5', border: '1px solid #6ee7b7', padding: '16px', borderRadius: '12px', color: '#065f46', fontWeight: '800', textAlign: 'center' }}>
          {paymentSuccessMsg}
        </div>
      )}

      {/* DYNAMIC SUBSCRIPTION PLANS LIST */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
        {availablePlans.map((planItem) => (
          <div
            key={planItem.id}
            onClick={() => setSelectedPlan(planItem.id)}
            style={{
              backgroundColor: '#ffffff',
              padding: '24px',
              borderRadius: '16px',
              border: selectedPlan === planItem.id ? '3px solid #185FA5' : '1px solid #cbd5e1',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px'
            }}
          >
            <h3 style={{ margin: 0, fontWeight: '900', fontSize: '18px', color: '#0B1F3A' }}>{planItem.name}</h3>
            <div style={{ fontSize: '24px', fontWeight: '900', color: '#185FA5' }}>{planItem.price_fcfa} FCFA</div>
            <p style={{ margin: 0, fontSize: '13px', color: '#64748b' }}>{planItem.description}</p>
            <div style={{ fontSize: '12px', fontWeight: '800', color: '#0F6E56' }}>Crédits: {planItem.applications_limit} candidature(s)</div>
          </div>
        ))}
      </div>

      <div style={{ backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1', maxWidth: '512px', margin: '0 auto', width: '100%', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Mode de Paiement</h3>

        {paymentErrorMsg && (
          <div style={{ backgroundColor: '#fef2f2', border: '1px solid #fca5a5', padding: '12px', borderRadius: '10px', color: '#991b1b', fontSize: '13px', fontWeight: '800' }}>
            {paymentErrorMsg}
          </div>
        )}

        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '8px' }}>Sélectionnez le mode de paiement :</label>
          <select
            value={paymentMethod}
            onChange={e => {
              const method = e.target.value as 'AIRTEL_MONEY' | 'MTN_MOMO';
              setPaymentMethod(method);
              setPhoneNumber(method === 'AIRTEL_MONEY' ? '05' : '06');
            }}
            style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700' }}
          >
            <option value="AIRTEL_MONEY">Airtel Money (Entrer numéro commençant par 05)</option>
            <option value="MTN_MOMO">Mobile Money MTN (Entrer numéro commençant par 06)</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '8px' }}>
            {paymentMethod === 'AIRTEL_MONEY' ? 'Numéro Airtel Money (Débute par 05)' : 'Numéro Mobile Money MTN (Débute par 06)'}
          </label>
          <input
            type="text"
            value={phoneNumber}
            placeholder={paymentMethod === 'AIRTEL_MONEY' ? '05XXXXXXX' : '06XXXXXXX'}
            onChange={e => setPhoneNumber(e.target.value)}
            style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '15px', fontWeight: '700' }}
          />
        </div>

        <div style={{ backgroundColor: '#f8fafc', padding: '16px', borderRadius: '12px', border: '1px solid #e2e8f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '14px', fontWeight: '800', color: '#334155' }}>Montant à payer :</span>
          <span style={{ fontSize: '20px', fontWeight: '900', color: '#185FA5' }}>
            {availablePlans.find(p => p.id === selectedPlan)?.price_fcfa || 0} FCFA
          </span>
        </div>

        <button onClick={handlePayment} style={{ width: '100%', backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '900', fontSize: '16px', padding: '16px', borderRadius: '10px', border: 'none', cursor: 'pointer' }}>
          Acheter ({availablePlans.find(p => p.id === selectedPlan)?.price_fcfa || 0} FCFA)
        </button>
      </div>
    </div>
  );
};
