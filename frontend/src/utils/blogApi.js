/**
 * Blog API - Funciones para interactuar con endpoints del blog
 */

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

// Helper para obtener token JWT
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
};

/**
 * Generar artículo bajo demanda (Admin)
 */
export const generateCustomArticle = async (data) => {
  const response = await fetch(`${API_URL}/api/blog/generate/custom`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error generando artículo');
  }
  
  return response.json();
};

/**
 * Obtener artículos en cola de aprobación (Admin)
 */
export const getPendingArticles = async () => {
  const response = await fetch(`${API_URL}/api/blog/posts/pending`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Error obteniendo artículos pendientes');
  }
  
  return response.json();
};

/**
 * Obtener preview de artículo sin incrementar vistas (Admin)
 */
export const getArticlePreview = async (postId) => {
  const response = await fetch(`${API_URL}/api/blog/posts/${postId}/preview`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Error obteniendo preview');
  }
  
  return response.json();
};

/**
 * Aprobar y publicar artículo (Admin)
 */
export const approveArticle = async (postId) => {
  const response = await fetch(`${API_URL}/api/blog/posts/${postId}/approve`, {
    method: 'PUT',
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Error aprobando artículo');
  }
  
  return response.json();
};

/**
 * Rechazar artículo (Admin)
 */
export const rejectArticle = async (postId, reason = null) => {
  const url = `${API_URL}/api/blog/posts/${postId}/reject${reason ? `?reason=${encodeURIComponent(reason)}` : ''}`;
  const response = await fetch(url, {
    method: 'PUT',
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Error rechazando artículo');
  }
  
  return response.json();
};

/**
 * Obtener estadísticas del blog (Admin)
 */
export const getBlogStats = async () => {
  const response = await fetch(`${API_URL}/api/blog/stats`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Error obteniendo estadísticas');
  }
  
  return response.json();
};

/**
 * Listar artículos publicados (Público)
 */
export const getPublishedArticles = async (skip = 0, limit = 10) => {
  const response = await fetch(`${API_URL}/api/blog/posts?skip=${skip}&limit=${limit}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  
  if (!response.ok) {
    throw new Error('Error obteniendo artículos');
  }
  
  return response.json();
};

/**
 * Obtener artículo por slug (Público)
 */
export const getArticleBySlug = async (slug) => {
  const response = await fetch(`${API_URL}/api/blog/posts/${slug}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  
  if (!response.ok) {
    throw new Error('Error obteniendo artículo');
  }
  
  return response.json();
};
