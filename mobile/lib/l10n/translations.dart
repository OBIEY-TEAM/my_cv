import 'package:flutter/material.dart';

class LanguageOption {
  final String code;
  final String label;
  final String flag;
  final TextDirection dir;

  const LanguageOption({
    required this.code,
    required this.label,
    required this.flag,
    this.dir = TextDirection.ltr,
  });
}

const List<LanguageOption> supportedLanguages = [
  LanguageOption(code: 'fr', label: 'Français', flag: '🇫🇷'),
  LanguageOption(code: 'en', label: 'English', flag: '🇬🇧'),
  LanguageOption(code: 'ar', label: 'العربية', flag: '🇸🇦', dir: TextDirection.rtl),
  LanguageOption(code: 'pt', label: 'Português', flag: '🇵🇹'),
  LanguageOption(code: 'es', label: 'Español', flag: '🇪🇸'),
  LanguageOption(code: 'sw', label: 'Kiswahili', flag: '🇰🇪'),
  LanguageOption(code: 'zh', label: '中文', flag: '🇨🇳'),
];

class AppTranslations {
  static String currentLanguage = 'fr';

  static final Map<String, Map<String, String>> _translations = {
    'fr': {
      'appTitle': 'Luka Mosala',
      'generateTitle': 'Générer par Luka Mossala',
      'generateSubtitle': 'Laissez les champs vides pour générer le CV uniquement (sans offre d\'emploi).',
      'urlLabel': 'Lien URL de l\'offre (Optionnel)',
      'or': 'OU',
      'textLabel': 'Texte brut de l\'offre (Optionnel)',
      'btnGenerate': 'Générer par Luka Mossala',
      'btnGenerating': 'Génération par Luka Mossala...',
      'tabDashboard': 'Candidatures',
      'tabCreate': 'Luka Mosala',
      'tabProfile': 'Profil',
      'tabPlans': 'Abonnement',
      'credits': 'CR',
    },
    'en': {
      'appTitle': 'Luka Mosala',
      'generateTitle': 'Generate with Luka Mossala',
      'generateSubtitle': 'Leave fields empty to generate CV only (without job offer).',
      'urlLabel': 'Job Offer URL (Optional)',
      'or': 'OR',
      'textLabel': 'Raw Job Description (Optional)',
      'btnGenerate': 'Generate with Luka Mossala',
      'btnGenerating': 'Generating with Luka Mossala...',
      'tabDashboard': 'Applications',
      'tabCreate': 'Luka Mosala',
      'tabProfile': 'Profile',
      'tabPlans': 'Subscription',
      'credits': 'CR',
    },
    'ar': {
      'appTitle': 'لوكا موسالا',
      'generateTitle': 'إنشاء بواسطة لوكا موسالا',
      'generateSubtitle': 'اترك الحقول فارغة لإنشاء السيرة الذاتية فقط (بدون عرض عمل).',
      'urlLabel': 'رابط عرض العمل (اختياري)',
      'or': 'أو',
      'textLabel': 'نص عرض العمل (اختياري)',
      'btnGenerate': 'إنشاء بواسطة لوكا موسالا',
      'btnGenerating': 'جاري الإنشاء...',
      'tabDashboard': 'الطلبات',
      'tabCreate': 'لوكا موسالا',
      'tabProfile': 'الملف الشخصي',
      'tabPlans': 'الاشتراك',
      'credits': 'رصيد',
    },
    'pt': {
      'appTitle': 'Luka Mosala',
      'generateTitle': 'Gerar com Luka Mossala',
      'generateSubtitle': 'Deixe os campos em branco para gerar apenas o CV (sem oferta de emprego).',
      'urlLabel': 'URL da oferta (Opcional)',
      'or': 'OU',
      'textLabel': 'Texto da oferta (Opcional)',
      'btnGenerate': 'Gerar com Luka Mossala',
      'btnGenerating': 'Gerando com Luka Mossala...',
      'tabDashboard': 'Candidaturas',
      'tabCreate': 'Luka Mosala',
      'tabProfile': 'Perfil',
      'tabPlans': 'Assinatura',
      'credits': 'CR',
    },
    'es': {
      'appTitle': 'Luka Mosala',
      'generateTitle': 'Generar con Luka Mossala',
      'generateSubtitle': 'Deje los campos vacíos para generar solo el CV (sin oferta de trabajo).',
      'urlLabel': 'URL de la oferta (Opcional)',
      'or': 'O',
      'textLabel': 'Texto de la oferta (Opcional)',
      'btnGenerate': 'Generar con Luka Mossala',
      'btnGenerating': 'Generando con Luka Mossala...',
      'tabDashboard': 'Candidaturas',
      'tabCreate': 'Luka Mosala',
      'tabProfile': 'Perfil',
      'tabPlans': 'Suscripción',
      'credits': 'CR',
    },
    'sw': {
      'appTitle': 'Luka Mosala',
      'generateTitle': 'Tengeneza kwa Luka Mossala',
      'generateSubtitle': 'Acha nafasi wazi kutengeneza CV pekee (bila tangazo la kazi).',
      'urlLabel': 'Kiungo cha Tangazo (Hiari)',
      'or': 'AU',
      'textLabel': 'Maelezo ya Tangazo (Hiari)',
      'btnGenerate': 'Tengeneza kwa Luka Mossala',
      'btnGenerating': 'Inatengeneza...',
      'tabDashboard': 'Maombi',
      'tabCreate': 'Luka Mosala',
      'tabProfile': 'Profaili',
      'tabPlans': 'Usajili',
      'credits': 'CR',
    },
    'zh': {
      'appTitle': 'Luka Mosala',
      'generateTitle': '由 Luka Mossala 生成',
      'generateSubtitle': '留空字段将仅生成简历（无需招聘信息）。',
      'urlLabel': '招聘链接 (可选)',
      'or': '或',
      'textLabel': '招聘原文 (可选)',
      'btnGenerate': '由 Luka Mossala 生成',
      'btnGenerating': '生成中...',
      'tabDashboard': '求职申请',
      'tabCreate': 'Luka Mosala',
      'tabProfile': '个人资料',
      'tabPlans': '订阅',
      'credits': '积分',
    },
  };

  static String t(String key) {
    return _translations[currentLanguage]?[key] ?? _translations['fr']?[key] ?? key;
  }

  static TextDirection get currentDirection {
    return currentLanguage == 'ar' ? TextDirection.rtl : TextDirection.ltr;
  }
}
