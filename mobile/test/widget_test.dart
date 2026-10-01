import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/main.dart';

void main() {
  testWidgets('App renders title', (WidgetTester tester) async {
    await tester.pumpWidget(const LukaMosalaApp());
    await tester.pump(const Duration(seconds: 2));
    expect(find.text('Luka Mosala Mobile'), findsAtLeastNWidgets(1));
  });
}
