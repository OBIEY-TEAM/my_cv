import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import '../../l10n/translations.dart';

class CreateApplicationTab extends StatefulWidget {
  final VoidCallback onGenerated;
  const CreateApplicationTab({super.key, required this.onGenerated});

  @override
  State<CreateApplicationTab> createState() => _CreateApplicationTabState();
}

class _CreateApplicationTabState extends State<CreateApplicationTab> {
  final _urlController = TextEditingController();
  final _textController = TextEditingController();
  bool _isGenerating = false;

  void _generate() async {
    final rawTxt = _textController.text.isEmpty && _urlController.text.isEmpty
        ? "RÉDACTION CV UNIQUEMENT SANS OFFRE D'EMPLOI"
        : _textController.text;

    setState(() => _isGenerating = true);
    final success = await ApiService.generateApplication(
      rawTxt,
      _urlController.text,
      language: AppTranslations.currentLanguage,
    );
    if (!mounted) return;
    setState(() => _isGenerating = false);

    if (success) {
      _urlController.clear();
      _textController.clear();
      widget.onGenerated();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Génération effectuée par Luka Mossala !')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Erreur lors de la génération. Vérifiez vos crédits.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: AppTranslations.currentDirection,
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Card(
          color: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  AppTranslations.t('generateTitle'),
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A)),
                ),
                const SizedBox(height: 6),
                Text(
                  AppTranslations.t('generateSubtitle'),
                  style: const TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _urlController,
                  decoration: InputDecoration(
                    labelText: AppTranslations.t('urlLabel'),
                    border: const OutlineInputBorder(),
                    prefixIcon: const Icon(Icons.link),
                  ),
                ),
                const SizedBox(height: 12),
                Center(
                  child: Text(
                    AppTranslations.t('or'),
                    style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.grey),
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: _textController,
                  maxLines: 4,
                  decoration: InputDecoration(
                    labelText: AppTranslations.t('textLabel'),
                    border: const OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),
                ElevatedButton.icon(
                  onPressed: _isGenerating ? null : _generate,
                  icon: _isGenerating
                      ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Icon(Icons.post_add),
                  label: Text(_isGenerating ? AppTranslations.t('btnGenerating') : AppTranslations.t('btnGenerate')),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5)),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
