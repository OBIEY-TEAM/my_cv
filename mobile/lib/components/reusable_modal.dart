import 'package:flutter/material.dart';

class ReusableModal extends StatefulWidget {
  final String title;
  final String? subtitle;
  final Color headerBg;
  final Widget child;
  final Widget? footer;
  final bool initialFullScreen;
  final VoidCallback? onClose;

  const ReusableModal({
    super.key,
    required this.title,
    this.subtitle,
    this.headerBg = const Color(0xFF185FA5),
    required this.child,
    this.footer,
    this.initialFullScreen = false,
    this.onClose,
  });

  static Future<T?> show<T>({
    required BuildContext context,
    required String title,
    String? subtitle,
    Color headerBg = const Color(0xFF185FA5),
    required Widget child,
    Widget? footer,
    bool isScrollControlled = true,
  }) {
    return showModalBottomSheet<T>(
      context: context,
      isScrollControlled: isScrollControlled,
      backgroundColor: Colors.transparent,
      builder: (ctx) => ReusableModal(
        title: title,
        subtitle: subtitle,
        headerBg: headerBg,
        footer: footer,
        onClose: () => Navigator.of(ctx).pop(),
        child: child,
      ),
    );
  }

  @override
  State<ReusableModal> createState() => _ReusableModalState();
}

class _ReusableModalState extends State<ReusableModal> {
  late bool _isFullScreen;

  @override
  void initState() {
    super.initState();
    _isFullScreen = widget.initialFullScreen;
  }

  @override
  Widget build(BuildContext context) {
    final media = MediaQuery.of(context);
    final bottomPadding = media.viewInsets.bottom;

    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      height: _isFullScreen ? media.size.height : null,
      constraints: BoxConstraints(
        maxHeight: _isFullScreen ? media.size.height : media.size.height * 0.9,
      ),
      margin: _isFullScreen ? EdgeInsets.zero : const EdgeInsets.only(top: 24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: _isFullScreen
            ? BorderRadius.zero
            : const BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: SafeArea(
        top: _isFullScreen,
        bottom: false,
        child: Column(
          mainAxisSize: _isFullScreen ? MainAxisSize.max : MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // HEADER WITH TITLE, FULLSCREEN TOGGLE AND CLOSE BUTTON
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: widget.headerBg,
                borderRadius: _isFullScreen
                    ? BorderRadius.zero
                    : const BorderRadius.vertical(top: Radius.circular(20)),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          widget.title,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                          overflow: TextOverflow.ellipsis,
                        ),
                        if (widget.subtitle != null) ...[
                          const SizedBox(height: 2),
                          Text(
                            widget.subtitle!,
                            style: const TextStyle(
                              color: Colors.white70,
                              fontSize: 11,
                            ),
                            overflow: TextOverflow.ellipsis,
                          ),
                        ]
                      ],
                    ),
                  ),
                  IconButton(
                    tooltip: _isFullScreen ? 'Réduire' : 'Agrandir (Plein Écran)',
                    icon: Icon(
                      _isFullScreen ? Icons.fullscreen_exit : Icons.fullscreen,
                      color: Colors.white,
                    ),
                    onPressed: () {
                      setState(() {
                        _isFullScreen = !_isFullScreen;
                      });
                    },
                  ),
                  IconButton(
                    tooltip: 'Fermer',
                    icon: const Icon(Icons.close, color: Colors.white),
                    onPressed: widget.onClose ?? () => Navigator.of(context).pop(),
                  ),
                ],
              ),
            ),

            // BODY
            Expanded(
              flex: _isFullScreen ? 1 : 0,
              child: SingleChildScrollView(
                padding: EdgeInsets.only(
                  left: 16,
                  right: 16,
                  top: 16,
                  bottom: bottomPadding + 16,
                ),
                child: widget.child,
              ),
            ),

            // FOOTER IF ANY
            if (widget.footer != null) ...[
              Container(
                padding: const EdgeInsets.all(12),
                decoration: const BoxDecoration(
                  color: Color(0xFFF8FAFC),
                  border: Border(top: BorderSide(color: Color(0xFFCBD5E1))),
                ),
                child: widget.footer,
              ),
            ]
          ],
        ),
      ),
    );
  }
}
