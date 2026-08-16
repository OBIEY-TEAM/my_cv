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
        // Try auto register
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
      DashboardTab(onRefresh: _loadSubscription),
      CreateApplicationTab(onGenerated: _loadSubscription),
      const ProfileTab(),
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
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profil'),
          BottomNavigationBarItem(icon: Icon(Icons.payment), label: 'Abonnement'),
        ],
      ),
    );
  }
}

class DashboardTab extends StatefulWidget {
  final VoidCallback onRefresh;
  const DashboardTab({super.key, required this.onRefresh});

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
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(color: const Color(0xFFE0F2FE), borderRadius: BorderRadius.circular(8)),
                          child: Text(offer['site_category'] ?? 'ACPE', style: const TextStyle(color: Color(0xFF0369A1), fontWeight: FontWeight.bold, fontSize: 11)),
                        ),
                        const SizedBox(height: 8),
                        Text(offer['title'] ?? 'Intitulé non spécifié', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
                        Text(offer['company'] ?? 'Recruteur', style: const TextStyle(color: Color(0xFF444441), fontSize: 13)),
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
    if (_urlController.text.isEmpty && _textController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Veuillez spécifier l\'URL ou le texte de l\'offre.')),
      );
      return;
    }

    setState(() => _isGenerating = true);
    final success = await ApiService.generateApplication(_textController.text, _urlController.text);
    setState(() => _isGenerating = false);

    if (success) {
      _urlController.clear();
      _textController.clear();
      widget.onGenerated();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Candidature sur mesure générée avec succès !')),
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
              const SizedBox(height: 16),
              TextField(
                controller: _urlController,
                decoration: const InputDecoration(
                  labelText: 'Lien URL de l\'offre',
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
                  labelText: 'Texte brut de l\'offre',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _isGenerating ? null : _generate,
                icon: _isGenerating ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) : const Icon(Icons.auto_awesome),
                label: Text(_isGenerating ? 'Génération en cours...' : 'Lancer la Génération IA'),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5)),
              )
            ],
          ),
        ),
      ),
    );
  }
}

class ProfileTab extends StatelessWidget {
  const ProfileTab({super.key});

  @override
  Widget build(BuildContext context) {
    return const SingleChildScrollView(
      padding: EdgeInsets.all(16.0),
      child: Card(
        color: Colors.white,
        child: Padding(
          padding: EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Mon Profil README / Markdown', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
              SizedBox(height: 16),
              TextField(
                decoration: InputDecoration(labelText: 'Titre Principal', border: OutlineInputBorder()),
              ),
              SizedBox(height: 12),
              TextField(
                maxLines: 6,
                decoration: InputDecoration(labelText: 'Markdown CV Source', border: OutlineInputBorder()),
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
  final _phoneController = TextEditingController(text: '+242066130118');
  bool _isPaying = false;

  void _pay() async {
    setState(() => _isPaying = true);
    final success = await ApiService.payMobileMoney(2, 'AIRTEL_MONEY', _phoneController.text);
    setState(() => _isPaying = false);

    if (success) {
      widget.onPaid();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Paiement réussi ! Crédits rechargés.')),
        );
      }
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Échec de la transaction.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Card(
            color: Colors.white,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Pack 5 Candidatures', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A))),
                  const SizedBox(height: 4),
                  const Text('2 000 FCFA', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF185FA5))),
                  const SizedBox(height: 16),
                  TextField(
                    controller: _phoneController,
                    decoration: const InputDecoration(
                      labelText: 'Numéro Mobile Money (+242)',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _isPaying ? null : _pay,
                    style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0F6E56)),
                    child: Text(_isPaying ? 'Traitement...' : 'Payer via Airtel / MTN MoMo'),
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
