import axios from 'axios';

// Create configured axios instance with optional custom backend URL (for Vercel deployment)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  headers: {
    'Accept': 'application/json',
  }
});

// Voice & Whisper API
export const transcribeAudio = async (audioBlob, filename = 'speech.wav', language = null) => {
  const formData = new FormData();
  formData.append('file', audioBlob, filename);
  if (language) formData.append('language', language);
  
  const response = await api.post('/api/voice/transcribe', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const extractAndFillVoice = async (audioBlob, formId = 'income_certificate', filename = 'speech.wav', language = null) => {
  const formData = new FormData();
  formData.append('file', audioBlob, filename);
  if (formId) formData.append('form_id', formId);
  if (language) formData.append('language', language);

  const response = await api.post('/api/voice/extract-and-fill', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

// NLP Text Extraction
export const extractFromText = async (text, formId = 'income_certificate', existingData = {}) => {
  const response = await api.post('/api/nlp/extract', {
    text,
    form_id: formId,
    existing_data: existingData
  });
  return response.data;
};

// Government Forms API
export const getForms = async () => {
  const response = await api.get('/api/forms');
  return response.data.forms;
};

export const getFormById = async (formId) => {
  const response = await api.get(`/api/forms/${formId}`);
  return response.data.form;
};

export const validateFormData = async (formId, formData) => {
  const response = await api.post('/api/forms/validate', {
    form_id: formId,
    form_data: formData
  });
  return response.data;
};

export const submitApplication = async (payload) => {
  const response = await api.post('/api/forms/submit', payload);
  return response.data;
};

export const getSubmissionById = async (submissionId) => {
  const response = await api.get(`/api/forms/submissions/${submissionId}`);
  return response.data.submission;
};

export const getPdfDownloadUrl = (submissionId) => {
  return `/api/forms/submissions/${submissionId}/pdf`;
};

// Schemes Engine API
export const getSchemes = async (category = null) => {
  const url = category ? `/api/schemes?category=${encodeURIComponent(category)}` : '/api/schemes';
  const response = await api.get(url);
  return response.data;
};

export const checkSchemeEligibility = async (profileData) => {
  const response = await api.post('/api/schemes/check-eligibility', profileData);
  return response.data;
};

// Assistant API
export const explainFormField = async (fieldId, lang = 'en') => {
  const response = await api.get(`/api/assistant/explain?field_id=${encodeURIComponent(fieldId)}&lang=${encodeURIComponent(lang)}`);
  return response.data;
};

export const queryAssistantChat = async (query, lang = 'en') => {
  const response = await api.post('/api/assistant/chat', { query, language: lang });
  return response.data;
};

// Draft PDF Download
export const downloadDraftPdf = async (formId, formData) => {
  const response = await api.post('/api/forms/draft-pdf', {
    form_id: formId,
    form_data: formData
  }, { responseType: 'blob' });
  return response.data;
};

// Dataset Management API
export const getDatasetStatus = async () => {
  const response = await api.get('/api/dataset/status');
  return response.data;
};

export const runDatasetValidation = async (limit = 5) => {
  const response = await api.get(`/api/dataset/validate?limit=${limit}`);
  return response.data;
};

export const submitConsentedSample = async (formDataObj) => {
  const response = await api.post('/api/dataset/samples', formDataObj, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const getCollectedSamples = async (status = null, language = null) => {
  let url = '/api/dataset/samples';
  const params = [];
  if (status) params.push(`status=${encodeURIComponent(status)}`);
  if (language) params.push(`language=${encodeURIComponent(language)}`);
  if (params.length > 0) url += `?${params.join('&')}`;

  const response = await api.get(url);
  return response.data;
};

export const reviewCollectedSample = async (sampleId, reviewPayload) => {
  const response = await api.post(`/api/dataset/samples/${sampleId}/review`, reviewPayload);
  return response.data;
};

export const deleteCollectedSample = async (sampleId) => {
  const response = await api.delete(`/api/dataset/samples/${sampleId}`);
  return response.data;
};

export const getFormExtractionSamples = async () => {
  const response = await api.get('/api/dataset/form-extraction');
  return response.data;
};

export const evaluateFormExtractionApi = async (split = 'test') => {
  const response = await api.get(`/api/dataset/form-extraction/evaluate?split=${encodeURIComponent(split)}`);
  return response.data;
};

// Sample Audio Fetch
export const fetchSampleAudio = async () => {
  const response = await api.get('/sample-audio', { responseType: 'blob' });
  return response.data;
};

export default api;


