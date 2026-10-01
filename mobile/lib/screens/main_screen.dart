import 'package:flutter/material.dart';
import '../services/api_service.dart';
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
          BottomNavigationBarItem(icon: Icon(Icons.post_add), label: 'Luka Mosala'),
          BottomNavigationBarItem(icon: Icon(Icons.badge), label: 'Profil'),
          BottomNavigationBarItem(icon: Icon(Icons.payment), label: 'Abonnement'),
        ],
      ),
    );
  }
}
