export interface ProfileData {
  title: string;
  phone: string;
  cities: string;
  readme_content: string;
  cropped_photo: string | null;
  original_photo: string | null;
}

export interface UserInfo {
  first_name: string;
  last_name: string;
  gender: string;
  birth_date: string | null;
  primary_phone: string;
  secondary_phone: string;
  professional_summary: string;
  address: string;
  country: string;
  district: string;
  neighborhood: string;
}

export interface Experience {
  id?: number;
  title: string;
  company: string;
  industry: string;
  location: string;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  skills_acquired: string;
}

export interface Certification {
  id?: number;
  title: string;
  year: number;
  institution: string;
  location: string;
  start_date: string | null;
  end_date: string | null;
  description: string;
  pdf_url: string;
}

export interface Education {
  id?: number;
  title: string;
  year: number;
  institution: string;
  degree_level: string;
  field_of_study: string;
  location: string;
  start_date: string | null;
  end_date: string | null;
  description: string;
  skills_acquired: string;
  pdf_url: string;
}

export interface Project {
  id?: number;
  name: string;
  industry: string;
  beneficiary: string;
  link_url: string;
  description: string;
}

export interface ApplicationPackage {
  id: number;
  job_offer: {
    title: string;
    company: string;
    site_category: string;
    abbreviation: string;
  };
  cv_pdf: string;
  cover_letter_pdf: string;
  email_txt: string;
  zip_package: string;
  cv_text?: string;
  lm_text?: string;
  email_text?: string;
  email_body?: string;
  payment_status: 'approuved' | 'pending' | 'failed';
  processing_status: 'finalized' | 'pending' | 'inprocess';
  created_at: string;
}

export interface SubscriptionPlan {
  id: number;
  name: string;
  price_fcfa: number;
  applications_limit: number;
  duration_days: number;
  description: string;
}

export interface SubscriptionData {
  credits_remaining: number;
  plan: {
    name: string;
  } | null;
}
