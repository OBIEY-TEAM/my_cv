import 'package:flutter/material.dart';

void main() {
  runApp(const AIJobApplyApp());
}

class AIJobApplyApp extends StatelessWidget {
  const AIJobApplyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI JobApply SaaS',
      home: Scaffold(
        appBar: AppBar(title: const Text('AI JobApply SaaS')),
        body: const Center(
          child: Text('Générateur Automatisé de Candidatures Sur Mesure'),
        ),
      ),
    );
  }
}
