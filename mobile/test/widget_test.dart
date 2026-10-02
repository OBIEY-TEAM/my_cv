import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/main.dart';

void main() {
  testWidgets('App renders title', (WidgetTester tester) async {
    await tester.pumpWidget(const LukaMosalaApp());
    expect(find.text("Démarrage de l'application Mobile..."), findsAtLeastNWidgets(1));
    await tester.pumpAndSettle(const Duration(seconds: 4));
    expect(find.text('Luka Mosala Mobile'), findsAtLeastNWidgets(1));
  });
}
