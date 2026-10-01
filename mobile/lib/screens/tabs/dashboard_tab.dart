import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import '../../components/reusable_modal.dart';

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

  void _openPdfPreviewModal(dynamic pkg, String docTitle, String content) {
    ReusableModal.show(
      context: context,
      title: 'Aperçu PDF - $docTitle',
      subtitle: 'Prévisualisation en direct du document rédigé par Luka Mossala',
      headerBg: const Color(0xFF0B1F3A),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFFF1F5F9),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: const Color(0xFFCBD5E1)),
            ),
            child: Text(
              content.isNotEmpty ? content : 'Aucun contenu disponible pour l\'aperçu.',
              style: const TextStyle(fontSize: 14, height: 1.5, color: Color(0xFF1E293B)),
            ),
          ),
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Téléchargement du PDF $docTitle en cours...')),
              );
            },
            icon: const Icon(Icons.download),
            label: const Text('Télécharger le PDF', style: TextStyle(fontWeight: FontWeight.bold)),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0B1F3A),
              padding: const EdgeInsets.symmetric(vertical: 12),
            ),
          ),
        ],
      ),
    );
  }

  void _openEditModal(dynamic pkg) {
    final offer = pkg['job_offer'] ?? {};
    final cvCtrl = TextEditingController(text: pkg['cv_text'] ?? 'Résumé / Contenu du CV pour ${offer['title']}');
    final lmCtrl = TextEditingController(text: pkg['lm_text'] ?? 'Corps de la lettre de motivation pour ${offer['title']}');
    final emailCtrl = TextEditingController(text: pkg['email_text'] ?? pkg['email_body'] ?? 'Objet : Candidature\n\nMadame, Monsieur...');

    ReusableModal.show(
      context: context,
      title: 'Éditeur - ${offer['title'] ?? 'Candidature'}',
      subtitle: 'Modifiez le contenu puis enregistrez pour régénérer le PDF sur mesure.',
      headerBg: const Color(0xFF185FA5),
      footer: Row(
        children: [
          Expanded(
            child: OutlinedButton.icon(
              onPressed: () {
                _openPdfPreviewModal(
                  pkg,
                  offer['title'] ?? 'Candidature',
                  '--- CONTENU DU CV ---\n\n${cvCtrl.text}\n\n--- LETTRE DE MOTIVATION ---\n\n${lmCtrl.text}\n\n--- EMAIL ---\n\n${emailCtrl.text}',
                );
              },
              icon: const Icon(Icons.visibility, size: 16),
              label: const Text('Aperçu PDF', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
              style: OutlinedButton.styleFrom(
                foregroundColor: const Color(0xFF0B1F3A),
                side: const BorderSide(color: Color(0xFF0B1F3A)),
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            flex: 2,
            child: ElevatedButton.icon(
              onPressed: () async {
                final nav = Navigator.of(context);
                final success = await ApiService.updatePackageContent(pkg['id'], {
                  'cv_text': cvCtrl.text,
                  'lm_text': lmCtrl.text,
                  'email_text': emailCtrl.text,
                });
                if (!mounted) return;
                nav.pop();
                if (success) {
                  _loadPackages();
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Contenu modifié et PDF régénéré par Luka Mossala !')),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Erreur lors de la modification.')),
                  );
                }
              },
              icon: const Icon(Icons.save, size: 16),
              label: const Text('Enregistrer & Régénérer PDF', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0F6E56),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text('1. Contenu / Résumé CV', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF0B1F3A))),
          const SizedBox(height: 4),
          TextField(
            controller: cvCtrl,
            maxLines: 4,
            decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Texte du CV'),
          ),
          const SizedBox(height: 12),

          const Text('2. Lettre de Motivation (LM)', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF0B1F3A))),
          const SizedBox(height: 4),
          TextField(
            controller: lmCtrl,
            maxLines: 5,
            decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Texte de la LM'),
          ),
          const SizedBox(height: 12),

          const Text('3. Email de Candidature', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF0B1F3A))),
          const SizedBox(height: 4),
          TextField(
            controller: emailCtrl,
            maxLines: 4,
            decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Texte de l\'Email'),
          ),
        ],
      ),
    );
  }

  void _openDetailModal(dynamic pkg, String docType) {
    final offer = pkg['job_offer'] ?? {};
    final paymentStatus = pkg['payment_status'] ?? 'approuved';
    final processingStatus = pkg['processing_status'] ?? 'finalized';

    final cvPdf = pkg['cv_pdf'] ?? '';
    final lmPdf = pkg['cover_letter_pdf'] ?? '';
    final emailTxt = pkg['email_txt'] ?? '';

    bool isAvailable = true;
    if (docType == 'CV' && (cvPdf == null || cvPdf.toString().isEmpty)) isAvailable = false;
    if (docType == 'LM' && (lmPdf == null || lmPdf.toString().isEmpty)) isAvailable = false;
    if (docType == 'EMAIL' && (emailTxt == null || emailTxt.toString().isEmpty)) isAvailable = false;

    ReusableModal.show(
      context: context,
      title: '$docType - ${offer['title'] ?? 'Poste'}',
      subtitle: 'Société: ${offer['company'] ?? 'Recruteur'}',
      headerBg: const Color(0xFF0B1F3A),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
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
          if (!isAvailable)
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: const Color(0xFFFEF3C7), borderRadius: BorderRadius.circular(10)),
              child: const Text('Document en cours de rédaction ...', textAlign: TextAlign.center, style: TextStyle(color: Color(0xFF92400E), fontWeight: FontWeight.bold)),
            )
          else ...[
            ElevatedButton.icon(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Aperçu du PDF $docType...')));
              },
              icon: const Icon(Icons.visibility),
              label: Text('Voir / Télécharger PDF $docType'),
              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0B1F3A)),
            ),
            const SizedBox(height: 10),
            if (docType == 'CV' || docType == 'LM')
              OutlinedButton.icon(
                onPressed: () {
                  final docxFile = docType == 'CV'
                      ? (pkg['cv_docx'] ?? (cvPdf.toString().endsWith('.pdf') ? cvPdf.toString().replaceAll(RegExp(r'\.pdf$', caseSensitive: false), '.docx') : cvPdf))
                      : (pkg['cover_letter_docx'] ?? (lmPdf.toString().endsWith('.pdf') ? lmPdf.toString().replaceAll(RegExp(r'\.pdf$', caseSensitive: false), '.docx') : lmPdf));
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Ouverture/Téléchargement Word (.docx) : $docxFile')),
                  );
                },
                icon: const Icon(Icons.description),
                label: const Text('Ouvrir avec Word (.docx)'),
                style: OutlinedButton.styleFrom(foregroundColor: const Color(0xFF185FA5), side: const BorderSide(color: Color(0xFF185FA5))),
              ),
          ],
          const SizedBox(height: 16),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.pop(context);
              widget.onSwitchTab(3); // Switch to payments tab
            },
            icon: const Icon(Icons.payment),
            label: const Text('Payer / Recharger Crédits'),
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0F6E56)),
          ),
        ],
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
                            ElevatedButton.icon(
                              onPressed: () => _openEditModal(pkg),
                              icon: const Icon(Icons.edit, size: 14),
                              label: const Text('Modifier', style: TextStyle(fontSize: 12)),
                              style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFD97706), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8)),
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
