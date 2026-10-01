import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'main_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _isLoggedIn = false;
  bool _isLoading = false;
  bool _isRegisterMode = false;
  bool _isInitializing = true;

  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(milliseconds: 1200), () {
      if (mounted) {
        setState(() {
          _isInitializing = false;
        });
      }
    });
  }
  final _usernameController = TextEditingController(text: 'admin');
  final _phoneController = TextEditingController(text: '066130118');
  final _passwordController = TextEditingController(text: 'admin1234');
  final _confirmPasswordController = TextEditingController(text: 'admin1234');
  String? _errorMessage;

  void _handleAuth() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    bool success = false;
    if (_isRegisterMode) {
      if (_passwordController.text != _confirmPasswordController.text) {
        setState(() {
          _isLoading = false;
          _errorMessage = 'Les mots de passe ne correspondent pas.';
        });
        return;
      }
      success = await ApiService.registerByPhone(
        _phoneController.text,
        _passwordController.text,
        _confirmPasswordController.text,
      );
    } else {
      success = await ApiService.login(
        _usernameController.text,
        _passwordController.text,
      );
    }

    if (!mounted) return;

    setState(() {
      _isLoading = false;
      _isLoggedIn = success;
      if (!success) {
        _errorMessage = _isRegisterMode
            ? 'Échec de la création automatique du compte.'
            : 'Identifiants incorrects ou serveur indisponible.';
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isInitializing) {
      return Scaffold(
        backgroundColor: const Color(0xFF0B1F3A),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: Image.asset(
                  'assets/logo_black.png',
                  width: 100,
                  height: 100,
                  fit: BoxFit.cover,
                ),
              ),
              const SizedBox(height: 24),
              Image.asset(
                'assets/loader_black.gif',
                width: 70,
                height: 70,
              ),
              const SizedBox(height: 16),
              const Text(
                'Démarrage de l\'application Mobile...',
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
              ),
            ],
          ),
        ),
      );
    }

    if (_isLoggedIn) {
      return const MainTabScreen();
    }

    return Scaffold(
      backgroundColor: const Color(0xFF0B1F3A),
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
                    ClipRRect(
                      borderRadius: BorderRadius.circular(16),
                      child: Image.asset(
                        'assets/logo_black.png',
                        width: 70,
                        height: 70,
                        fit: BoxFit.cover,
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'Luka Mosala Mobile',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A)),
                    ),
                    if (_isLoading) ...[
                      const SizedBox(height: 12),
                      Image.asset('assets/loader_black.gif', width: 48, height: 48),
                    ],
                    const SizedBox(height: 6),
                    const Text(
                      'Générateur automatique de candidatures sur mesure',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Color(0xFF444441), fontSize: 13),
                    ),
                    const SizedBox(height: 24),
                    // MODE TOGGLE BUTTONS
                    Row(
                      children: [
                        Expanded(
                          child: ElevatedButton(
                            onPressed: () => setState(() {
                              _isRegisterMode = false;
                              _errorMessage = null;
                            }),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: !_isRegisterMode ? const Color(0xFF185FA5) : Colors.grey.shade200,
                              foregroundColor: !_isRegisterMode ? Colors.white : const Color(0xFF0B1F3A),
                              elevation: !_isRegisterMode ? 2 : 0,
                            ),
                            child: const Text('Se connecter', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: ElevatedButton(
                            onPressed: () => setState(() {
                              _isRegisterMode = true;
                              _errorMessage = null;
                            }),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: _isRegisterMode ? const Color(0xFF185FA5) : Colors.grey.shade200,
                              foregroundColor: _isRegisterMode ? Colors.white : const Color(0xFF0B1F3A),
                              elevation: _isRegisterMode ? 2 : 0,
                            ),
                            child: const Text('Créer un compte', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

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

                    if (!_isRegisterMode) ...[
                      TextField(
                        controller: _usernameController,
                        decoration: const InputDecoration(
                          labelText: 'Nom d\'utilisateur ou Téléphone',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.person),
                        ),
                      ),
                      const SizedBox(height: 16),
                    ] else ...[
                      TextField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        decoration: const InputDecoration(
                          labelText: 'Numéro de Téléphone',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.phone),
                        ),
                      ),
                      const SizedBox(height: 16),
                    ],

                    TextField(
                      controller: _passwordController,
                      obscureText: true,
                      decoration: const InputDecoration(
                        labelText: 'Mot de passe',
                        border: OutlineInputBorder(),
                        prefixIcon: Icon(Icons.lock),
                      ),
                    ),

                    if (_isRegisterMode) ...[
                      const SizedBox(height: 16),
                      TextField(
                        controller: _confirmPasswordController,
                        obscureText: true,
                        decoration: const InputDecoration(
                          labelText: 'Confirmer le mot de passe',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.lock_outline),
                        ),
                      ),
                    ],

                    const SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _handleAuth,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF185FA5),
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                        child: _isLoading
                            ? const CircularProgressIndicator(color: Colors.white)
                            : Text(_isRegisterMode ? 'Créer mon compte' : 'Se connecter', style: const TextStyle(fontWeight: FontWeight.bold)),
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
