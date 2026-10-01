import 'package:flutter/material.dart';
import '../../services/api_service.dart';
import '../../components/reusable_modal.dart';

class StructuredProfileTab extends StatefulWidget {
  const StructuredProfileTab({super.key});

  @override
  State<StructuredProfileTab> createState() => _StructuredProfileTabState();
}

class _StructuredProfileTabState extends State<StructuredProfileTab> {
  Map<String, dynamic> _info = {};
  List<dynamic> _experiences = [];
  List<dynamic> _certifications = [];
  List<dynamic> _educations = [];
  List<dynamic> _projects = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAll();
  }

  void _loadAll() async {
    setState(() => _isLoading = true);
    final info = await ApiService.fetchProfileInfo();
    final exps = await ApiService.fetchSection('experiences');
    final certs = await ApiService.fetchSection('certifications');
    final edus = await ApiService.fetchSection('educations');
    final projs = await ApiService.fetchSection('projects');

    if (!mounted) return;
    setState(() {
      _info = info ?? {};
      _experiences = exps;
      _certifications = certs;
      _educations = edus;
      _projects = projs;
      _isLoading = false;
    });
  }

  void _editInfoDialog() {
    final lastNameCtrl = TextEditingController(text: _info['last_name'] ?? '');
    final firstNameCtrl = TextEditingController(text: _info['first_name'] ?? '');
    String genderVal = _info['gender'] ?? 'MALE';
    final birthCtrl = TextEditingController(text: _info['birth_date'] ?? '1995-05-10');
    final phoneCtrl = TextEditingController(text: _info['primary_phone'] ?? '');
    final secPhoneCtrl = TextEditingController(text: _info['secondary_phone'] ?? '');
    final addressCtrl = TextEditingController(text: _info['address'] ?? '');
    final countryCtrl = TextEditingController(text: _info['country'] ?? 'Congo');
    final districtCtrl = TextEditingController(text: _info['district'] ?? '');
    final neighborhoodCtrl = TextEditingController(text: _info['neighborhood'] ?? '');
    final summaryCtrl = TextEditingController(text: _info['professional_summary'] ?? '');

    ReusableModal.show(
      context: context,
      title: '1. Informations Générales',
      headerBg: const Color(0xFF185FA5),
      footer: ElevatedButton(
        onPressed: () async {
          final nav = Navigator.of(context);
          await ApiService.saveProfileInfo({
            'last_name': lastNameCtrl.text,
            'first_name': firstNameCtrl.text,
            'gender': genderVal,
            'birth_date': birthCtrl.text,
            'primary_phone': phoneCtrl.text,
            'secondary_phone': secPhoneCtrl.text,
            'address': addressCtrl.text,
            'country': countryCtrl.text,
            'district': districtCtrl.text,
            'neighborhood': neighborhoodCtrl.text,
            'professional_summary': summaryCtrl.text,
          });
          nav.pop();
          _loadAll();
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: const Color(0xFF0F6E56),
          padding: const EdgeInsets.symmetric(vertical: 14),
        ),
        child: const Text('Enregistrer mes informations', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      child: StatefulBuilder(
        builder: (context, setModalState) => Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: lastNameCtrl, decoration: const InputDecoration(labelText: 'Nom *')),
            TextField(controller: firstNameCtrl, decoration: const InputDecoration(labelText: 'Prénom *')),
            DropdownButtonFormField<String>(
              initialValue: genderVal,
              decoration: const InputDecoration(labelText: 'Genre *'),
              items: const [
                DropdownMenuItem(value: 'MALE', child: Text('Homme')),
                DropdownMenuItem(value: 'FEMALE', child: Text('Femme')),
                DropdownMenuItem(value: 'OTHER', child: Text('Autre')),
              ],
              onChanged: (v) { if (v != null) setModalState(() => genderVal = v); },
            ),
            TextField(controller: birthCtrl, decoration: const InputDecoration(labelText: 'Date de naissance *')),
            TextField(controller: phoneCtrl, decoration: const InputDecoration(labelText: 'Numéro principal *')),
            TextField(controller: secPhoneCtrl, decoration: const InputDecoration(labelText: 'Numéro secondaire')),
            TextField(controller: addressCtrl, decoration: const InputDecoration(labelText: 'Adresse')),
            TextField(controller: countryCtrl, decoration: const InputDecoration(labelText: 'Pays')),
            TextField(controller: districtCtrl, decoration: const InputDecoration(labelText: 'Arrondissement')),
            TextField(controller: neighborhoodCtrl, decoration: const InputDecoration(labelText: 'Quartier')),
            TextField(controller: summaryCtrl, decoration: const InputDecoration(labelText: 'Résumé professionnel'), maxLines: 3),
          ],
        ),
      ),
    );
  }

  void _addExpDialog() {
    final titleCtrl = TextEditingController();
    final companyCtrl = TextEditingController();
    final industryCtrl = TextEditingController(text: 'Informatique');
    final locationCtrl = TextEditingController();
    final skillsCtrl = TextEditingController();

    ReusableModal.show(
      context: context,
      title: 'Ajouter une expérience',
      headerBg: const Color(0xFF185FA5),
      footer: ElevatedButton(
        onPressed: () async {
          if (titleCtrl.text.isNotEmpty && companyCtrl.text.isNotEmpty) {
            final nav = Navigator.of(context);
            await ApiService.addSectionItem('experiences', {
              'title': titleCtrl.text,
              'company': companyCtrl.text,
              'industry': industryCtrl.text,
              'location': locationCtrl.text,
              'start_date': '2024-01-01',
              'is_current': true,
              'skills_acquired': skillsCtrl.text,
            });
            nav.pop();
            _loadAll();
          }
        },
        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5), padding: const EdgeInsets.symmetric(vertical: 14)),
        child: const Text('Ajouter', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: titleCtrl, decoration: const InputDecoration(labelText: 'Poste occupé *')),
          TextField(controller: companyCtrl, decoration: const InputDecoration(labelText: 'Structure *')),
          TextField(controller: industryCtrl, decoration: const InputDecoration(labelText: 'Secteur d\'activité *')),
          TextField(controller: locationCtrl, decoration: const InputDecoration(labelText: 'Lieu')),
          TextField(controller: skillsCtrl, decoration: const InputDecoration(labelText: 'Compétences acquises')),
        ],
      ),
    );
  }

  void _addCertDialog() {
    final titleCtrl = TextEditingController();
    final yearCtrl = TextEditingController(text: '2025');
    final instCtrl = TextEditingController();

    ReusableModal.show(
      context: context,
      title: 'Ajouter un certificat',
      headerBg: const Color(0xFF185FA5),
      footer: ElevatedButton(
        onPressed: () async {
          if (titleCtrl.text.isNotEmpty) {
            final nav = Navigator.of(context);
            await ApiService.addSectionItem('certifications', {
              'title': titleCtrl.text,
              'year': int.tryParse(yearCtrl.text) ?? 2025,
              'institution': instCtrl.text,
            });
            nav.pop();
            _loadAll();
          }
        },
        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5), padding: const EdgeInsets.symmetric(vertical: 14)),
        child: const Text('Ajouter', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: titleCtrl, decoration: const InputDecoration(labelText: 'Libellé certificat *')),
          TextField(controller: yearCtrl, decoration: const InputDecoration(labelText: 'Année *'), keyboardType: TextInputType.number),
          TextField(controller: instCtrl, decoration: const InputDecoration(labelText: 'Institution *')),
        ],
      ),
    );
  }

  void _addEduDialog() {
    final titleCtrl = TextEditingController();
    final yearCtrl = TextEditingController(text: '2024');
    final instCtrl = TextEditingController();
    final degreeCtrl = TextEditingController(text: 'Licence');

    ReusableModal.show(
      context: context,
      title: 'Ajouter un diplôme',
      headerBg: const Color(0xFF185FA5),
      footer: ElevatedButton(
        onPressed: () async {
          if (titleCtrl.text.isNotEmpty) {
            final nav = Navigator.of(context);
            await ApiService.addSectionItem('educations', {
              'title': titleCtrl.text,
              'year': int.tryParse(yearCtrl.text) ?? 2024,
              'institution': instCtrl.text,
              'degree_level': degreeCtrl.text,
            });
            nav.pop();
            _loadAll();
          }
        },
        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5), padding: const EdgeInsets.symmetric(vertical: 14)),
        child: const Text('Ajouter', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: titleCtrl, decoration: const InputDecoration(labelText: 'Libellé du diplôme *')),
          TextField(controller: yearCtrl, decoration: const InputDecoration(labelText: 'Année *'), keyboardType: TextInputType.number),
          TextField(controller: instCtrl, decoration: const InputDecoration(labelText: 'Institution *')),
          TextField(controller: degreeCtrl, decoration: const InputDecoration(labelText: 'Niveau d\'étude *')),
        ],
      ),
    );
  }

  void _addProjDialog() {
    final nameCtrl = TextEditingController();
    final industryCtrl = TextEditingController(text: 'Informatique');

    ReusableModal.show(
      context: context,
      title: 'Ajouter un projet',
      headerBg: const Color(0xFF185FA5),
      footer: ElevatedButton(
        onPressed: () async {
          if (nameCtrl.text.isNotEmpty) {
            final nav = Navigator.of(context);
            await ApiService.addSectionItem('projects', {
              'name': nameCtrl.text,
              'industry': industryCtrl.text,
            });
            nav.pop();
            _loadAll();
          }
        },
        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5), padding: const EdgeInsets.symmetric(vertical: 14)),
        child: const Text('Ajouter', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Nom du projet *')),
          TextField(controller: industryCtrl, decoration: const InputDecoration(labelText: 'Secteur d\'activité *')),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Card(
            color: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const CircleAvatar(
                        radius: 30,
                        backgroundColor: Color(0xFF185FA5),
                        child: Icon(Icons.person, color: Colors.white, size: 36),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '${_info['first_name'] ?? 'Christ Dany'} ${_info['last_name'] ?? 'Obiey'}',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0B1F3A)),
                            ),
                            const Text('Photo de Profil Professionnelle', style: TextStyle(fontSize: 11, color: Colors.grey, fontWeight: FontWeight.bold)),
                          ],
                        ),
                      )
                    ],
                  ),
                  const SizedBox(height: 12),
                  // 4 EXPLICIT PHOTO ACTION BUTTONS MATCHING WEB
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      ElevatedButton.icon(
                        onPressed: () => ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Modification de la photo...'))),
                        icon: const Icon(Icons.edit, size: 14),
                        label: const Text('Modifier', style: TextStyle(fontSize: 11)),
                        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6)),
                      ),
                      ElevatedButton.icon(
                        onPressed: () => ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Upload de la photo...'))),
                        icon: const Icon(Icons.upload, size: 14),
                        label: const Text('Uploader', style: TextStyle(fontSize: 11)),
                        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0B1F3A), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6)),
                      ),
                      ElevatedButton.icon(
                        onPressed: () => ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Ouverture de la caméra...'))),
                        icon: const Icon(Icons.camera_alt, size: 14),
                        label: const Text('Caméra', style: TextStyle(fontSize: 11)),
                        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0F6E56), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6)),
                      ),
                      OutlinedButton.icon(
                        onPressed: () => ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Aperçu de la photo...'))),
                        icon: const Icon(Icons.visibility, size: 14),
                        label: const Text('Voir', style: TextStyle(fontSize: 11)),
                        style: OutlinedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6)),
                      ),
                    ],
                  ),
                  const Divider(height: 24),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('1. Informations Générales', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0B1F3A))),
                      IconButton(onPressed: _editInfoDialog, icon: const Icon(Icons.edit, color: Color(0xFF185FA5))),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text('Genre: ${_info['gender'] == 'FEMALE' ? 'Femme' : 'Homme'} | Né(e) le: ${_info['birth_date'] ?? '10/05/1995'}', style: const TextStyle(fontSize: 12, color: Color(0xFF334155))),
                  Text('Téléphone Principal: ${_info['primary_phone'] ?? '+242 06 613 01 18'}', style: const TextStyle(fontSize: 12, color: Color(0xFF334155))),
                  if ((_info['secondary_phone'] ?? '').isNotEmpty) Text('Téléphone Secondaire: ${_info['secondary_phone']}', style: const TextStyle(fontSize: 12, color: Color(0xFF334155))),
                  Text('Adresse: ${_info['address'] ?? 'Avenue de l\'Indépendance'} | Pays: ${_info['country'] ?? 'Congo'}', style: const TextStyle(fontSize: 12, color: Color(0xFF334155))),
                  Text('Arrondissement: ${_info['district'] ?? 'Poto-Poto'} | Quartier: ${_info['neighborhood'] ?? 'Centre'}', style: const TextStyle(fontSize: 12, color: Color(0xFF334155))),
                  if ((_info['professional_summary'] ?? '').isNotEmpty) ...[
                    const SizedBox(height: 8),
                    Text('Résumé: ${_info['professional_summary']}', style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic, color: Color(0xFF475569))),
                  ]
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),

          _buildSectionHeader('Expériences Professionnelles', _addExpDialog),
          ..._experiences.map((exp) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              title: Text(exp['title'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('${exp['company'] ?? ''} (${exp['start_date'] ?? ''})'),
              trailing: IconButton(
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () async {
                  await ApiService.deleteSectionItem('experiences', exp['id']);
                  _loadAll();
                },
              ),
            ),
          )),

          _buildSectionHeader('Certifications et Attestations', _addCertDialog),
          ..._certifications.map((cert) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              title: Text('${cert['title']} (${cert['year']})', style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(cert['institution'] ?? ''),
              trailing: IconButton(
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () async {
                  await ApiService.deleteSectionItem('certifications', cert['id']);
                  _loadAll();
                },
              ),
            ),
          )),

          _buildSectionHeader('Diplômes', _addEduDialog),
          ..._educations.map((edu) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              title: Text('${edu['title']} - ${edu['degree_level']} (${edu['year']})', style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(edu['institution'] ?? ''),
              trailing: IconButton(
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () async {
                  await ApiService.deleteSectionItem('educations', edu['id']);
                  _loadAll();
                },
              ),
            ),
          )),

          _buildSectionHeader('Projets', _addProjDialog),
          ..._projects.map((proj) => Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              title: Text(proj['name'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(proj['industry'] ?? ''),
              trailing: IconButton(
                icon: const Icon(Icons.delete, color: Colors.red),
                onPressed: () async {
                  await ApiService.deleteSectionItem('projects', proj['id']);
                  _loadAll();
                },
              ),
            ),
          )),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title, VoidCallback onAdd) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 12.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
          IconButton(onPressed: onAdd, icon: const Icon(Icons.add_circle, color: Color(0xFF185FA5), size: 28)),
        ],
      ),
    );
  }
}
