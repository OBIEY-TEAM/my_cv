import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class DashboardTab extends StatefulWidget {
  final VoidCallback onRefresh;
  final Function(int) onSwitchTab;
  const DashboardTab({super.key, required this.onRefresh, required this.onSwitchTab});

  @override
  State<DashboardTab> createState() => _DashboardTabState();
}

class _DashboardTabState extends State<DashboardTab> {
  List<dynamic> _packages = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadPackages();
  }

  void _loadPackages() async {
    setState(() => _isLoading = true);
    final list = await ApiService.fetchPackages();
    if (!mounted) return;
    setState(() {
      _packages = list;
      _isLoading = false;
    });
    widget.onRefresh();
  }

  void _openDetailModal(dynamic pkg, String docType) {
    final offer = pkg['job_offer'] ?? {};
    final paymentStatus = pkg['payment_status'] ?? 'approuved';
    final processingStatus = pkg['processing_status'] ?? 'finalized';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '$docType - ${offer['title'] ?? 'Poste'}',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A)),
                ),
                IconButton(onPressed: () => Navigator.pop(ctx), icon: const Icon(Icons.close)),
              ],
            ),
            const Divider(),
            const SizedBox(height: 12),
            Row(
              children: [
                const Text('Status de Paiement: ', style: TextStyle(fontWeight: FontWeight.bold)),
                Chip(
                  label: Text(paymentStatus, style: const TextStyle(fontSize: 11, color: Colors.white, fontWeight: FontWeight.bold)),
                  backgroundColor: paymentStatus == 'approuved' ? Colors.green : Colors.orange,
                  padding: EdgeInsets.zero,
                ),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Text('Status de Traitement: ', style: TextStyle(fontWeight: FontWeight.bold)),
                Chip(
                  label: Text(processingStatus, style: const TextStyle(fontSize: 11, color: Colors.white, fontWeight: FontWeight.bold)),
                  backgroundColor: processingStatus == 'finalized' ? Colors.blue : Colors.orange,
                  padding: EdgeInsets.zero,
                ),
              ],
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Aperçu du $docType en cours...')));
              },
              icon: const Icon(Icons.visibility),
              label: Text('Voir $docType'),
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0B1F3A)),
            ),
            const SizedBox(height: 10),
            OutlinedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Téléchargement du $docType en cours...')));
              },
              icon: const Icon(Icons.download),
              label: Text('Télécharger $docType'),
            ),
            const SizedBox(height: 10),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.pop(ctx);
                widget.onSwitchTab(3); // Switch to payments tab
              },
              icon: const Icon(Icons.payment),
              label: const Text('Payer / Recharger Crédits'),
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0F6E56)),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    return RefreshIndicator(
      onRefresh: () async => _loadPackages(),
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              color: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Bienvenue 👋', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
                    SizedBox(height: 6),
                    Text('Vos dossiers de candidature sur mesure (CV 1P & LM 1P) prêts à l\'emploi.',
                        style: TextStyle(color: Color(0xFF444441), fontSize: 13, fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            if (_packages.isEmpty)
              const Card(
                color: Colors.white,
                child: Padding(
                  padding: EdgeInsets.all(32.0),
                  child: Center(
                    child: Text('Aucune candidature générée pour le moment.'),
                  ),
                ),
              )
            else
              ..._packages.map((pkg) {
                final offer = pkg['job_offer'] ?? {};
                return Card(
                  color: Colors.white,
                  margin: const EdgeInsets.only(bottom: 12),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              decoration: BoxDecoration(color: const Color(0xFFE0F2FE), borderRadius: BorderRadius.circular(8)),
                              child: Text(offer['site_category'] ?? 'ACPE', style: const TextStyle(color: Color(0xFF0369A1), fontWeight: FontWeight.bold, fontSize: 11)),
                            ),
                            Text(pkg['processing_status'] ?? 'finalized', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.green)),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(offer['title'] ?? 'Intitulé non spécifié', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
                        Text(offer['company'] ?? 'Recruteur', style: const TextStyle(color: Color(0xFF444441), fontSize: 13)),
                        const Divider(height: 20),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            ElevatedButton(
                              onPressed: () => _openDetailModal(pkg, 'CV'),
                              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0B1F3A), padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8)),
                              child: const Text('CV', style: TextStyle(fontSize: 12)),
                            ),
                            ElevatedButton(
                              onPressed: () => _openDetailModal(pkg, 'LM'),
                              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0B1F3A), padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8)),
                              child: const Text('LM', style: TextStyle(fontSize: 12)),
                            ),
                            ElevatedButton(
                              onPressed: () => _openDetailModal(pkg, 'EMAIL'),
                              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5), padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8)),
                              child: const Text('EMAIL', style: TextStyle(fontSize: 12)),
                            ),
                            ElevatedButton(
                              onPressed: () => _openDetailModal(pkg, 'Paiement'),
                              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0F6E56), padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8)),
                              child: const Text('Payer', style: TextStyle(fontSize: 12)),
                            ),
                          ],
                        )
                      ],
                    ),
                  ),
                );
              }),
          ],
        ),
      ),
    );
  }
}
