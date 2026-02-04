import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Check API health status
 */
export const checkHealth = async () => {
    const response = await api.get('/health');
    return response.data;
};

/**
 * Submit code for review
 */
export const reviewCode = async (code, description, language = 'python') => {
    const response = await api.post('/review-code', {
        code,
        description,
        language,
    });
    return response.data;
};

/**
 * Upload coding standards
 */
export const uploadStandards = async (content, source = 'uploaded') => {
    const response = await api.post('/upload-standards', {
        content,
        source,
    });
    return response.data;
};

/**
 * Upload standards file
 */
export const uploadStandardsFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload-standards', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

/**
 * Reload all standards
 */
export const reloadStandards = async () => {
    const response = await api.post('/reload-standards');
    return response.data;
};

export default api;
