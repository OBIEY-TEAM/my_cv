import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || (
  window.location.hostname.includes('onrender.com')
    ? 'https://luka-mosala-backend.onrender.com'
    : ''
);

axios.defaults.baseURL = API_BASE_URL;

export const setAuthToken = (token: string | null) => {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }
};

export class ApiService {
  static async login(username: string, password: string) {
    try {
      const res = await axios.post('/api/auth/login/', { username, password });
      return res.data.access;
    } catch (e: any) {
      const regRes = await axios.post('/api/auth/register/', {
        username,
        password,
        email: `${username}@lukamosala.cg`,
        first_name: username === 'admin' ? 'Admin' : 'Utilisateur',
        last_name: 'Luka Mosala'
      });
      return regRes.data.access;
    }
  }

  static async fetchAllProfileData() {
    const [profRes, infoRes, subRes, pkgsRes, expRes, certRes, eduRes, projRes, plansRes] = await Promise.all([
      axios.get('/api/profile/'),
      axios.get('/api/profile/info/'),
      axios.get('/api/subscriptions/me/'),
      axios.get('/api/jobs/packages/'),
      axios.get('/api/profile/experiences/'),
      axios.get('/api/profile/certifications/'),
      axios.get('/api/profile/educations/'),
      axios.get('/api/profile/projects/'),
      axios.get('/api/subscriptions/plans/')
    ]);

    return {
      profile: profRes.data,
      userInfo: infoRes.data,
      subscription: subRes.data,
      packages: pkgsRes.data,
      experiences: expRes.data,
      certifications: certRes.data,
      educations: eduRes.data,
      projects: projRes.data,
      plans: plansRes.data
    };
  }

  static async uploadPhoto(file: File) {
    const formData = new FormData();
    formData.append('photo', file);
    const res = await axios.post('/api/profile/crop-photo/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  }

  static async updateUserInfo(userInfo: any) {
    return await axios.patch('/api/profile/info/', userInfo);
  }

  static async saveExperience(exp: any) {
    if (exp.id) {
      return await axios.put(`/api/profile/experiences/${exp.id}/`, exp);
    }
    return await axios.post('/api/profile/experiences/', exp);
  }

  static async deleteExperience(id: number) {
    return await axios.delete(`/api/profile/experiences/${id}/`);
  }

  static async saveCertification(certForm: any, pdfFile: File | null) {
    const formData = new FormData();
    Object.keys(certForm).forEach(key => {
      const val = (certForm as any)[key];
      if (val !== null && val !== undefined) formData.append(key, val);
    });
    if (pdfFile) formData.append('pdf_file', pdfFile);

    if (certForm.id) {
      return await axios.put(`/api/profile/certifications/${certForm.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    }
    return await axios.post('/api/profile/certifications/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }

  static async deleteCertification(id: number) {
    return await axios.delete(`/api/profile/certifications/${id}/`);
  }

  static async saveEducation(eduForm: any, pdfFile: File | null) {
    const formData = new FormData();
    Object.keys(eduForm).forEach(key => {
      const val = (eduForm as any)[key];
      if (val !== null && val !== undefined) formData.append(key, val);
    });
    if (pdfFile) formData.append('pdf_file', pdfFile);

    if (eduForm.id) {
      return await axios.put(`/api/profile/educations/${eduForm.id}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    }
    return await axios.post('/api/profile/educations/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }

  static async deleteEducation(id: number) {
    return await axios.delete(`/api/profile/educations/${id}/`);
  }

  static async saveProject(proj: any) {
    if (proj.id) {
      return await axios.put(`/api/profile/projects/${proj.id}/`, proj);
    }
    return await axios.post('/api/profile/projects/', proj);
  }

  static async deleteProject(id: number) {
    return await axios.delete(`/api/profile/projects/${id}/`);
  }

  static async generateApplication(jobText: string, sourceUrl: string) {
    return await axios.post('/api/jobs/offers/', {
      source_type: sourceUrl ? 'URL' : 'TEXT',
      source_url: sourceUrl,
      raw_text: jobText || "RÉDACTION CV UNIQUEMENT SANS OFFRE D'EMPLOI"
    });
  }

  static async makePayment(planId: number, method: string, phone: string) {
    return await axios.post('/api/subscriptions/pay/', {
      plan_id: planId,
      payment_method: method,
      phone_number: phone
    });
  }
}
