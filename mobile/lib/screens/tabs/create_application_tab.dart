import 'package:flutter/material.dart';
import '../../services/api_service.dart';

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
    final success = await ApiService.generateApplication(rawTxt, _urlController.text);
    if (!mounted) return;
    setState(() => _isGenerating = false);

    if (success) {
      _urlController.clear();
      _textController.clear();
      widget.onGenerated();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Génération effectuée par Groq Cloud AI !')),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Erreur lors de la génération. Vérifiez vos crédits.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Card(
        color: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text('Générer un Dossier Sur Mesure',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
              const SizedBox(height: 6),
              const Text(
                'Laissez les champs vides pour générer le CV uniquement (sans offre d\'emploi).',
                style: TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _urlController,
                decoration: const InputDecoration(
                  labelText: 'Lien URL de l\'offre (Optionnel)',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.link),
                ),
              ),
              const SizedBox(height: 12),
              const Center(child: Text('OU', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey))),
              const SizedBox(height: 12),
              TextField(
                controller: _textController,
                maxLines: 4,
                decoration: const InputDecoration(
                  labelText: 'Texte brut de l\'offre (Optionnel)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _isGenerating ? null : _generate,
                icon: _isGenerating ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) : const Icon(Icons.auto_awesome),
                label: Text(_isGenerating ? 'Génération Groq AI...' : 'Générer (Groq Cloud AI)'),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5)),
              )
            ],
          ),
        ),
      ),
    );
  }
}
