import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class PaymentsTab extends StatefulWidget {
  final VoidCallback onPaid;
  const PaymentsTab({super.key, required this.onPaid});

  @override
  State<PaymentsTab> createState() => _PaymentsTabState();
}

class _PaymentsTabState extends State<PaymentsTab> {
  List<dynamic> _plans = [];
  int? _selectedPlanId;
  String _paymentMethod = 'AIRTEL_MONEY';
  final _phoneController = TextEditingController(text: '056130118');
  bool _isLoadingPlans = true;
  bool _isPaying = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadPlans();
  }

  void _loadPlans() async {
    setState(() => _isLoadingPlans = true);
    final plansList = await ApiService.fetchPlans();
    if (!mounted) return;
    setState(() {
      _plans = plansList;
      if (_plans.isNotEmpty) {
        _selectedPlanId = _plans[0]['id'];
      }
      _isLoadingPlans = false;
    });
  }

  void _pay() async {
    setState(() {
      _errorMessage = null;
    });

    if (_selectedPlanId == null) {
      setState(() => _errorMessage = 'Veuillez sélectionner un forfait.');
      return;
    }

    final cleanPhone = _phoneController.text.replaceAll(RegExp(r'\D'), '');
    if (_paymentMethod == 'AIRTEL_MONEY' && !cleanPhone.startsWith('05') && !cleanPhone.startsWith('24205')) {
      setState(() => _errorMessage = 'Le numéro Airtel Money doit commencer par 05.');
      return;
    }
    if (_paymentMethod == 'MTN_MOMO' && !cleanPhone.startsWith('06') && !cleanPhone.startsWith('24206')) {
      setState(() => _errorMessage = 'Le numéro Mobile Money MTN doit commencer par 06.');
      return;
    }

    setState(() => _isPaying = true);
    final success = await ApiService.payMobileMoney(_selectedPlanId!, _paymentMethod, _phoneController.text);
    if (!mounted) return;
    setState(() => _isPaying = false);

    if (success) {
      widget.onPaid();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Achat réussi ! Crédits rechargés.')),
      );
    } else {
      setState(() => _errorMessage = 'Échec de la transaction Fintech Mobile Money.');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoadingPlans) {
      return const Center(child: CircularProgressIndicator());
    }

    dynamic selectedPlanObj;
    try {
      selectedPlanObj = _plans.firstWhere((p) => p['id'] == _selectedPlanId);
    } catch (_) {}

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text('Forfaits Crédits', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
          const SizedBox(height: 12),

          // DISPLAY DYNAMIC PLANS LIST
          ..._plans.map((plan) {
            final isSelected = plan['id'] == _selectedPlanId;
            return Card(
              color: isSelected ? const Color(0xFFEFF6FF) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: isSelected ? const Color(0xFF185FA5) : Colors.grey.shade300, width: isSelected ? 2 : 1),
              ),
              margin: const EdgeInsets.only(bottom: 10),
              child: ListTile(
                onTap: () => setState(() => _selectedPlanId = plan['id']),
                title: Text(plan['name'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
                subtitle: Text('${plan['description'] ?? ''}\n${plan['applications_limit'] ?? 0} Crédit(s)'),
                isThreeLine: true,
                trailing: Text('${plan['price_fcfa']} FCFA', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF185FA5))),
              ),
            );
          }),

          const SizedBox(height: 16),
          Card(
            color: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Mode de Paiement', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
                  const SizedBox(height: 16),

                  if (_errorMessage != null)
                    Container(
                      padding: const EdgeInsets.all(10),
                      margin: const EdgeInsets.only(bottom: 12),
                      decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8)),
                      child: Text(_errorMessage!, style: TextStyle(color: Colors.red.shade900, fontSize: 12, fontWeight: FontWeight.bold)),
                    ),

                  DropdownButtonFormField<String>(
                    initialValue: _paymentMethod,
                    decoration: const InputDecoration(
                      labelText: 'Type de paiement',
                      border: OutlineInputBorder(),
                    ),
                    items: const [
                      DropdownMenuItem(value: 'AIRTEL_MONEY', child: Text('Airtel Money (Débute par 05)')),
                      DropdownMenuItem(value: 'MTN_MOMO', child: Text('Mobile Money MTN (Débute par 06)')),
                    ],
                    onChanged: (val) {
                      if (val != null) {
                        setState(() {
                          _paymentMethod = val;
                          _phoneController.text = val == 'AIRTEL_MONEY' ? '056130118' : '066130118';
                        });
                      }
                    },
                  ),
                  const SizedBox(height: 16),

                  TextField(
                    controller: _phoneController,
                    keyboardType: TextInputType.phone,
                    decoration: InputDecoration(
                      labelText: _paymentMethod == 'AIRTEL_MONEY' ? 'Numéro Airtel Money (05...)' : 'Numéro Mobile Money MTN (06...)',
                      border: const OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 20),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Montant à payer :', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      Text('${selectedPlanObj != null ? selectedPlanObj['price_fcfa'] : 0} FCFA', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF185FA5))),
                    ],
                  ),
                  const SizedBox(height: 16),

                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _isPaying ? null : _pay,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF0F6E56),
                        padding: const EdgeInsets.symmetric(vertical: 14),
                      ),
                      child: Text(
                        _isPaying ? 'Achat en cours...' : 'Acheter (${selectedPlanObj != null ? selectedPlanObj['price_fcfa'] : 0} FCFA)',
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
