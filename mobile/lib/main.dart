import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const LukaMosalaApp());
}

class ApiService {
  static const String baseUrl = 'https://luka-mosala-backend.onrender.com';
  static String? authToken;

  static Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (authToken != null) 'Authorization': 'Bearer $authToken',
      };

  static Future<bool> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        authToken = data['access'];
        return true;
      } else {
        final regResponse = await http.post(
          Uri.parse('$baseUrl/api/auth/register/'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'username': username,
            'password': password,
            'email': '$username@lukamosala.cg',
            'first_name': username == 'admin' ? 'Admin' : 'Utilisateur',
            'last_name': 'Luka Mosala',
          }),
        );
        if (regResponse.statusCode == 201) {
          final data = jsonDecode(regResponse.body);
          authToken = data['access'];
          return true;
        }
      }
    } catch (e) {
      debugPrint('Login error: $e');
    }
    return false;
  }

  static Future<Map<String, dynamic>?> fetchSubscription() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/subscriptions/me/'),
        headers: headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Fetch subscription error: $e');
    }
    return null;
  }

  static Future<List<dynamic>> fetchPackages() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/jobs/packages/'),
        headers: headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Fetch packages error: $e');
    }
    return [];
  }

  static Future<List<dynamic>> fetchPlans() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/subscriptions/plans/'),
        headers: headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Fetch plans error: $e');
    }
    return [];
  }

  static Future<bool> generateApplication(String rawText, String sourceUrl) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/jobs/offers/'),
        headers: headers,
        body: jsonEncode({
          'source_type': sourceUrl.isNotEmpty ? 'URL' : 'TEXT',
          'source_url': sourceUrl,
          'raw_text': rawText,
        }),
      );
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('Generate error: $e');
    }
    return false;
  }

  static Future<bool> payMobileMoney(int planId, String method, String phone) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/subscriptions/pay/'),
        headers: headers,
        body: jsonEncode({
          'plan_id': planId,
          'payment_method': method,
          'phone_number': phone,
        }),
      );
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('Payment error: $e');
    }
    return false;
  }

  // Structured Profile Endpoints
  static Future<Map<String, dynamic>?> fetchProfileInfo() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/api/profile/info/'), headers: headers);
      if (res.statusCode == 200) return jsonDecode(res.body);
    } catch (e) { debugPrint('Error profile info: $e'); }
    return null;
  }

  static Future<bool> saveProfileInfo(Map<String, dynamic> data) async {
    try {
      final res = await http.patch(Uri.parse('$baseUrl/api/profile/info/'), headers: headers, body: jsonEncode(data));
      return res.statusCode == 200;
    } catch (e) { return false; }
  }

  static Future<List<dynamic>> fetchSection(String section) async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/api/profile/$section/'), headers: headers);
      if (res.statusCode == 200) return jsonDecode(res.body);
    } catch (e) { debugPrint('Error section $section: $e'); }
    return [];
  }

  static Future<bool> addSectionItem(String section, Map<String, dynamic> data) async {
    try {
      final res = await http.post(Uri.parse('$baseUrl/api/profile/$section/'), headers: headers, body: jsonEncode(data));
      return res.statusCode == 201;
    } catch (e) { return false; }
  }

  static Future<bool> deleteSectionItem(String section, int id) async {
    try {
      final res = await http.delete(Uri.parse('$baseUrl/api/profile/$section/$id/'), headers: headers);
      return res.statusCode == 204;
    } catch (e) { return false; }
  }
}

class LukaMosalaApp extends StatelessWidget {
  const LukaMosalaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Luka Mosala SaaS',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0B1F3A),
          primary: const Color(0xFF0B1F3A),
          secondary: const Color(0xFF185FA5),
        ),
        scaffoldBackgroundColor: const Color(0xFFF8FAFC),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0B1F3A),
          foregroundColor: Colors.white,
          elevation: 0,
        ),
      ),
      home: const LoginOrMainScreen(),
    );
  }
}

class LoginOrMainScreen extends StatefulWidget {
  const LoginOrMainScreen({super.key});

  @override
  State<LoginOrMainScreen> createState() => _LoginOrMainScreenState();
}

class _LoginOrMainScreenState extends State<LoginOrMainScreen> {
  bool _isLoggedIn = false;
  bool _isLoading = false;
  final _usernameController = TextEditingController(text: 'admin');
  final _passwordController = TextEditingController(text: 'admin1234');
  String? _errorMessage;

  void _handleLogin() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final success = await ApiService.login(
      _usernameController.text,
      _passwordController.text,
    );

    setState(() {
      _isLoading = false;
      _isLoggedIn = success;
      if (!success) {
        _errorMessage = 'Identifiants incorrects ou serveur indisponible.';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoggedIn) {
      return const MainTabScreen();
    }

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Card(
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: const Color(0xFF185FA5),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: const Icon(Icons.work, color: Colors.white, size: 36),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Luka Mosala SaaS',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A)),
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      'Générateur automatique de candidatures sur mesure',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Color(0xFF444441), fontSize: 13),
                    ),
                    const SizedBox(height: 24),
                    if (_errorMessage != null)
                      Container(
                        padding: const EdgeInsets.all(12),
                        margin: const EdgeInsets.only(bottom: 16),
                        decoration: BoxDecoration(
                          color: Colors.red.shade50,
                          border: Border.all(color: Colors.red.shade200),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          _errorMessage!,
                          style: TextStyle(color: Colors.red.shade800, fontSize: 13),
                        ),
                      ),
                    TextField(
                      controller: _usernameController,
                      decoration: const InputDecoration(
                        labelText: 'Nom d\'utilisateur',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.person),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _passwordController,
                      obscureText: true,
                      decoration: const InputDecoration(
                        labelText: 'Mot de passe',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.lock),
                      ),
                    ),
                    const SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _handleLogin,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF185FA5),
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                        child: _isLoading
                            ? const CircularProgressIndicator(color: Colors.white)
                            : const Text('Se connecter / S\'inscrire', style: TextStyle(fontWeight: FontWeight.bold)),
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      '💡 Compte par défaut: admin / admin1234',
                      style: TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class MainTabScreen extends StatefulWidget {
  const MainTabScreen({super.key});

  @override
  State<MainTabScreen> createState() => _MainTabScreenState();
}

class _MainTabScreenState extends State<MainTabScreen> {
  int _currentIndex = 0;
  int _creditsRemaining = 1;

  @override
  void initState() {
    super.initState();
    _loadSubscription();
  }

  void _loadSubscription() async {
    final sub = await ApiService.fetchSubscription();
    if (sub != null && sub.containsKey('credits_remaining')) {
      setState(() {
        _creditsRemaining = sub['credits_remaining'];
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> tabs = [
      DashboardTab(onRefresh: _loadSubscription, onSwitchTab: (index) => setState(() => _currentIndex = index)),
      CreateApplicationTab(onGenerated: _loadSubscription),
      const StructuredProfileTab(),
      PaymentsTab(onPaid: _loadSubscription),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Luka Mosala SaaS',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 16),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: const Color(0xFF185FA5),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              children: [
                const Icon(Icons.stars, color: Colors.amber, size: 18),
                const SizedBox(width: 6),
                Text(
                  '$_creditsRemaining Crédit(s)',
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
                ),
              ],
            ),
          )
        ],
      ),
      body: tabs[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        selectedItemColor: const Color(0xFF185FA5),
        unselectedItemColor: Colors.grey[600],
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: 'Candidatures'),
          BottomNavigationBarItem(icon: Icon(Icons.auto_awesome), label: 'Générer'),
          BottomNavigationBarItem(icon: Icon(Icons.badge), label: 'Profil'),
          BottomNavigationBarItem(icon: Icon(Icons.payment), label: 'Abonnement'),
        ],
      ),
    );
  }
}

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

    showDialog(
      context: context,
      builder: (ctx) => StatefulBuilder(
        builder: (context, setModalState) => AlertDialog(
          title: const Text('1. Informations Générales'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(controller: lastNameCtrl, decoration: const InputDecoration(labelText: 'Nom *')),
                TextField(controller: firstNameCtrl, decoration: const InputDecoration(labelText: 'Prénom *')),
                DropdownButtonFormField<String>(
                  value: genderVal,
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
          actions: [
            TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
            ElevatedButton(
              onPressed: () async {
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
                Navigator.pop(ctx);
                _loadAll();
              },
              child: const Text('Enregistrer'),
            )
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

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Ajouter une expérience'),
        content: SingleChildScrollView(
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
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
          ElevatedButton(
            onPressed: () async {
              if (titleCtrl.text.isNotEmpty && companyCtrl.text.isNotEmpty) {
                await ApiService.addSectionItem('experiences', {
                  'title': titleCtrl.text,
                  'company': companyCtrl.text,
                  'industry': industryCtrl.text,
                  'location': locationCtrl.text,
                  'start_date': '2024-01-01',
                  'is_current': true,
                  'skills_acquired': skillsCtrl.text,
                });
                Navigator.pop(ctx);
                _loadAll();
              }
            },
            child: const Text('Ajouter'),
          )
        ],
      ),
    );
  }

  void _addCertDialog() {
    final titleCtrl = TextEditingController();
    final yearCtrl = TextEditingController(text: '2025');
    final instCtrl = TextEditingController();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Ajouter un certificat'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: titleCtrl, decoration: const InputDecoration(labelText: 'Libellé certificat *')),
            TextField(controller: yearCtrl, decoration: const InputDecoration(labelText: 'Année *'), keyboardType: TextInputType.number),
            TextField(controller: instCtrl, decoration: const InputDecoration(labelText: 'Institution *')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
          ElevatedButton(
            onPressed: () async {
              if (titleCtrl.text.isNotEmpty) {
                await ApiService.addSectionItem('certifications', {
                  'title': titleCtrl.text,
                  'year': int.tryParse(yearCtrl.text) ?? 2025,
                  'institution': instCtrl.text,
                });
                Navigator.pop(ctx);
                _loadAll();
              }
            },
            child: const Text('Ajouter'),
          )
        ],
      ),
    );
  }

  void _addEduDialog() {
    final titleCtrl = TextEditingController();
    final yearCtrl = TextEditingController(text: '2024');
    final instCtrl = TextEditingController();
    final degreeCtrl = TextEditingController(text: 'Licence');

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Ajouter un diplôme'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: titleCtrl, decoration: const InputDecoration(labelText: 'Libellé du diplôme *')),
            TextField(controller: yearCtrl, decoration: const InputDecoration(labelText: 'Année *'), keyboardType: TextInputType.number),
            TextField(controller: instCtrl, decoration: const InputDecoration(labelText: 'Institution *')),
            TextField(controller: degreeCtrl, decoration: const InputDecoration(labelText: 'Niveau d\'étude *')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
          ElevatedButton(
            onPressed: () async {
              if (titleCtrl.text.isNotEmpty) {
                await ApiService.addSectionItem('educations', {
                  'title': titleCtrl.text,
                  'year': int.tryParse(yearCtrl.text) ?? 2024,
                  'institution': instCtrl.text,
                  'degree_level': degreeCtrl.text,
                });
                Navigator.pop(ctx);
                _loadAll();
              }
            },
            child: const Text('Ajouter'),
          )
        ],
      ),
    );
  }

  void _addProjDialog() {
    final nameCtrl = TextEditingController();
    final industryCtrl = TextEditingController(text: 'Informatique');

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Ajouter un projet'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: 'Nom du projet *')),
            TextField(controller: industryCtrl, decoration: const InputDecoration(labelText: 'Secteur d\'activité *')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Annuler')),
          ElevatedButton(
            onPressed: () async {
              if (nameCtrl.text.isNotEmpty) {
                await ApiService.addSectionItem('projects', {
                  'name': nameCtrl.text,
                  'industry': industryCtrl.text,
                });
                Navigator.pop(ctx);
                _loadAll();
              }
            },
            child: const Text('Ajouter'),
          )
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
    setState(() => _isGenerating = false);

    if (success) {
      _urlController.clear();
      _textController.clear();
      widget.onGenerated();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Génération effectuée par Groq Cloud AI !')),
        );
      }
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Erreur lors de la génération. Vérifiez vos crédits.')),
        );
      }
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
    setState(() => _isPaying = false);

    if (success) {
      widget.onPaid();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Achat réussi ! Crédits rechargés.')),
        );
      }
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
                    value: _paymentMethod,
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
