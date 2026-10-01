import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../components/loader_showcase_dialog.dart';
import '../l10n/translations.dart';
import 'tabs/dashboard_tab.dart';
import 'tabs/create_application_tab.dart';
import 'tabs/profile_tab.dart';
import 'tabs/payments_tab.dart';

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
    if (!mounted) return;
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

    return Directionality(
      textDirection: AppTranslations.currentDirection,
      child: Scaffold(
        backgroundColor: const Color(0xFF0F172A),
        appBar: AppBar(
          backgroundColor: Colors.black,
          elevation: 2,
          title: Row(
            children: [
              Image.asset(
                'assets/logo_black.png',
                height: 38,
                errorBuilder: (context, error, stackTrace) => const Icon(Icons.business, color: Colors.amber),
              ),
              const SizedBox(width: 8),
              Text(
                AppTranslations.t('appTitle'),
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18),
              ),
            ],
          ),
          actions: [
            // Language selector dropdown
            Theme(
              data: Theme.of(context).copyWith(canvasColor: const Color(0xFF1E293B)),
              child: DropdownButton<String>(
                value: AppTranslations.currentLanguage,
                underline: const SizedBox(),
                icon: const Icon(Icons.language, color: Colors.amber, size: 20),
                onChanged: (String? newLang) {
                  if (newLang != null) {
                    setState(() {
                      AppTranslations.currentLanguage = newLang;
                    });
                  }
                },
                items: supportedLanguages.map((lang) {
                  return DropdownMenuItem<String>(
                    value: lang.code,
                    child: Text(
                      '${lang.flag} ${lang.code.toUpperCase()}',
                      style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                  );
                }).toList(),
              ),
            ),
            IconButton(
              tooltip: 'Loaders & Code Source',
              icon: const Icon(Icons.animation, color: Colors.amber),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => const LoaderShowcaseDialog(),
                );
              },
            ),
            Container(
              margin: const EdgeInsets.only(right: 12),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: const Color(0xFF185FA5),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  const Icon(Icons.stars, color: Colors.amber, size: 16),
                  const SizedBox(width: 4),
                  Text(
                    '$_creditsRemaining ${AppTranslations.t('credits')}',
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 11),
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
          items: [
            BottomNavigationBarItem(icon: const Icon(Icons.dashboard), label: AppTranslations.t('tabDashboard')),
            BottomNavigationBarItem(icon: const Icon(Icons.post_add), label: AppTranslations.t('tabCreate')),
            BottomNavigationBarItem(icon: const Icon(Icons.badge), label: AppTranslations.t('tabProfile')),
            BottomNavigationBarItem(icon: const Icon(Icons.payment), label: AppTranslations.t('tabPlans')),
          ],
        ),
      ),
    );
  }
}
