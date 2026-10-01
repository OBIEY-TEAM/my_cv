import 'package:flutter/material.dart';

class LoaderShowcaseDialog extends StatefulWidget {
  const LoaderShowcaseDialog({super.key});

  @override
  State<LoaderShowcaseDialog> createState() => _LoaderShowcaseDialogState();
}

class _LoaderShowcaseDialogState extends State<LoaderShowcaseDialog> {
  int _activeTab = 0; // 0: Preview, 1: Source Code

  final String _sourceCode = '''
import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

WIDTH, HEIGHT = 600, 400
FPS = 12
TOTAL_FRAMES = 96 # 8 seconds

# Generate particles gathering into LM monogram & animated writing of LUKA MOSSALA
''';

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: const Color(0xFF0F172A),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Container(
        padding: const EdgeInsets.all(16),
        maxWidth: 500,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Row(
                  children: [
                    Icon(Icons.style, color: Colors.amber, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'Loaders & Code Source',
                      style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                  ],
                ),
                IconButton(
                  icon: const Icon(Icons.close, color: Colors.white70),
                  onPressed: () => Navigator.of(context).pop(),
                )
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _activeTab == 0 ? const Color(0xFF185FA5) : Colors.grey[800],
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () => setState(() => _activeTab = 0),
                    child: const Text('Aperçu GIFs'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: _activeTab == 1 ? const Color(0xFF185FA5) : Colors.grey[800],
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () => setState(() => _activeTab = 1),
                    child: const Text('Code Source'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (_activeTab == 0) ...[
              Container(
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.amber.withOpacity(0.5)),
                ),
                padding: const EdgeInsets.all(12),
                child: Column(
                  children: [
                    const Text('Loader Mobile (Fond Noir)', style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Image.asset('assets/loader_black.gif', height: 160, fit: BoxFit.contain),
                    const SizedBox(height: 12),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(foregroundColor: Colors.white),
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Affichage du loader mobile GIF actif.')),
                            );
                          },
                          icon: const Icon(Icons.visibility, size: 16),
                          label: const Text('Voir GIF', style: TextStyle(fontSize: 12)),
                        ),
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF185FA5)),
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Téléchargement de loader_black.gif prêt.')),
                            );
                          },
                          icon: const Icon(Icons.download, size: 16, color: Colors.white),
                          label: const Text('Télécharger', style: TextStyle(fontSize: 12, color: Colors.white)),
                        ),
                      ],
                    )
                  ],
                ),
              ),
              const SizedBox(height: 12),
              Container(
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                ),
                padding: const EdgeInsets.all(12),
                child: Column(
                  children: [
                    const Text('Loader Web (Fond Blanc)', style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    Image.asset('assets/loader_white.gif', height: 140, fit: BoxFit.contain),
                  ],
                ),
              )
            ] else ...[
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.grey[800]!),
                ),
                child: SingleChildScrollView(
                  child: Text(
                    _sourceCode,
                    style: const TextStyle(color: Colors.greenAccent, fontFamily: 'monospace', fontSize: 11),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
