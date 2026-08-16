import 'package:flutter/material.dart';

void main() {
  runApp(const LukaMosalaApp());
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
          tertiary: const Color(0xFF0F6E56),
          surface: const Color(0xFFF1EFE8),
        ),
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Luka Mosala SaaS', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          backgroundColor: const Color(0xFF0B1F3A),
        ),
        body: Container(
          color: const Color(0xFFF1EFE8),
          child: const Center(
            child: Text(
              'Luka Mosala - Générateur Automatisé de Candidatures Sur Mesure',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B1F3A)),
            ),
          ),
        ),
      ),
    );
  }
}
