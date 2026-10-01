import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String baseUrl = 'https://luka-mosala-backend.onrender.com';
  static String? authToken;

  static Map<String, String> get headers => {
        'Content-Type': 'application/json',
        if (authToken != null) 'Authorization': 'Bearer $authToken',
      };

  static Future<bool> registerByPhone(String phone, String password, String confirmPassword) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/register/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'phone_number': phone,
          'username': phone,
          'password': password,
          'password_confirm': confirmPassword,
        }),
      );
      if (response.statusCode == 201) {
        final data = jsonDecode(response.body);
        authToken = data['access'];
        return true;
      }
    } catch (e) {
      debugPrint('Register error: $e');
    }
    return false;
  }

  static Future<bool> updatePackageContent(int pkgId, Map<String, dynamic> data) async {
    try {
      final response = await http.patch(
        Uri.parse('$baseUrl/api/jobs/packages/$pkgId/update-content/'),
        headers: headers,
        body: jsonEncode(data),
      );
      return response.statusCode == 200;
    } catch (e) {
      debugPrint('Update package content error: $e');
    }
    return false;
  }

  static Future<bool> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/auth/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        authToken = data['access'];
        return true;
      } else {
        final regResponse = await http.post(
          Uri.parse('$baseUrl/api/auth/register/'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'username': username,
            'password': password,
            'email': '$username@lukamosala.cg',
            'first_name': username == 'admin' ? 'Admin' : 'Utilisateur',
            'last_name': 'Luka Mosala',
          }),
        );
        if (regResponse.statusCode == 201) {
          final data = jsonDecode(regResponse.body);
          authToken = data['access'];
          return true;
        }
      }
    } catch (e) {
      debugPrint('Login error: $e');
    }
    return false;
  }

  static Future<Map<String, dynamic>?> fetchSubscription() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/subscriptions/me/'),
        headers: headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Fetch subscription error: $e');
    }
    return null;
  }

  static Future<List<dynamic>> fetchPackages() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/jobs/packages/'),
        headers: headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Fetch packages error: $e');
    }
    return [];
  }

  static Future<List<dynamic>> fetchPlans() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/subscriptions/plans/'),
        headers: headers,
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
    } catch (e) {
      debugPrint('Fetch plans error: $e');
    }
    return [];
  }

  static Future<bool> generateApplication(String rawText, String sourceUrl, {String language = 'fr'}) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/jobs/offers/'),
        headers: headers,
        body: jsonEncode({
          'source_type': sourceUrl.isNotEmpty ? 'URL' : 'TEXT',
          'source_url': sourceUrl,
          'language': language,
          'raw_text': rawText,
        }),
      );
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('Generate error: $e');
    }
    return false;
  }

  static Future<bool> payMobileMoney(int planId, String method, String phone) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/subscriptions/pay/'),
        headers: headers,
        body: jsonEncode({
          'plan_id': planId,
          'payment_method': method,
          'phone_number': phone,
        }),
      );
      return response.statusCode == 201;
    } catch (e) {
      debugPrint('Payment error: $e');
    }
    return false;
  }

  // Structured Profile Endpoints
  static Future<Map<String, dynamic>?> fetchProfileInfo() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/api/profile/info/'), headers: headers);
      if (res.statusCode == 200) return jsonDecode(res.body);
    } catch (e) { debugPrint('Error profile info: $e'); }
    return null;
  }

  static Future<bool> saveProfileInfo(Map<String, dynamic> data) async {
    try {
      final res = await http.patch(Uri.parse('$baseUrl/api/profile/info/'), headers: headers, body: jsonEncode(data));
      return res.statusCode == 200;
    } catch (e) { return false; }
  }

  static Future<List<dynamic>> fetchSection(String section) async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/api/profile/$section/'), headers: headers);
      if (res.statusCode == 200) return jsonDecode(res.body);
    } catch (e) { debugPrint('Error section $section: $e'); }
    return [];
  }

  static Future<bool> addSectionItem(String section, Map<String, dynamic> data) async {
    try {
      final res = await http.post(Uri.parse('$baseUrl/api/profile/$section/'), headers: headers, body: jsonEncode(data));
      return res.statusCode == 201;
    } catch (e) { return false; }
  }

  static Future<bool> deleteSectionItem(String section, int id) async {
    try {
      final res = await http.delete(Uri.parse('$baseUrl/api/profile/$section/$id/'), headers: headers);
      return res.statusCode == 204;
    } catch (e) { return false; }
  }

  static Future<Map<String, dynamic>?> uploadProfilePhoto(String filePath) async {
    try {
      final request = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/profile/upload-photo/'));
      if (authToken != null) {
        request.headers['Authorization'] = 'Bearer $authToken';
      }
      request.files.add(await http.MultipartFile.fromPath('cropped_photo', filePath));
      final streamedRes = await request.send();
      final res = await http.Response.fromStream(streamedRes);
      if (res.statusCode == 200) {
        return jsonDecode(res.body);
      }
    } catch (e) {
      debugPrint('Upload photo error: $e');
    }
    return null;
  }
}
