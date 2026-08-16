import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/main.dart';

void main() {
  testWidgets('App renders title', (WidgetTester tester) async {
    await tester.pumpWidget(const AIJobApplyApp());
    expect(find.text('AI JobApply SaaS'), findsOneWidget);
  });
}
