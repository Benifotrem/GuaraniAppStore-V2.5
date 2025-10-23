import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import { Spin, Empty } from 'antd';
import { getPublishedArticles, getArticleBySlug } from '../utils/blogApi';
import './Blog.css';

const Blog = () => {
  const navigate = useNavigate();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [viewingArticle, setViewingArticle] = useState(false);

  useEffect(() => {
    loadArticles();
  }, []);

  const loadArticles = async () => {
    try {
      const data = await getPublishedArticles(0, 20);
      setArticles(data);
    } catch (error) {
      console.error('Error cargando artículos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReadArticle = async (slug) => {
    try {
      setLoading(true);
      const article = await getArticleBySlug(slug);
      setSelectedArticle(article);
      setViewingArticle(true);
    } catch (error) {
      console.error('Error cargando artículo:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-PY', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (viewingArticle && selectedArticle) {
    // Determinar si la imagen flota a la izquierda o derecha (día par/impar)
    const publishedDate = new Date(selectedArticle.published_at);
    const dayOfMonth = publishedDate.getDate();
    const imageFloatClass = dayOfMonth % 2 === 0 ? 'float-right' : 'float-left';
    
    return (
      <div className="blog-page">
        <header className="blog-header">
          <div className="blog-header-container">
            <button onClick={() => setViewingArticle(false)} className="back-button">
              ← Volver al blog
            </button>
          </div>
        </header>

        <main className="blog-content">
          <article className="blog-article-full">
            <div className="article-header">
              <h1 className="article-title">{selectedArticle.title}</h1>
              
              <div className="article-meta">
                <div className="author-info">
                  <div>
                    <div className="author-name">{selectedArticle.author_name}</div>
                    <div className="author-role">{selectedArticle.author_role}</div>
                  </div>
                </div>
                <div className="article-stats">
                  <span>📅 {formatDate(selectedArticle.published_at)}</span>
                  <span>⏱️ {selectedArticle.reading_time || 5} min lectura</span>
                  <span>👁️ {selectedArticle.views} vistas</span>
                </div>
              </div>
            </div>

            <div className="article-content">
              <ReactMarkdown 
                rehypePlugins={[rehypeRaw]}
                components={{
                  p: ({node, ...props}) => <p style={{marginBottom: '1.5rem'}} {...props} />,
                  h1: ({node, ...props}) => <h1 style={{fontSize: '2.5rem', fontWeight: '800', marginTop: '2rem', marginBottom: '1rem'}} {...props} />,
                  h2: ({node, ...props}) => <h2 style={{fontSize: '1.875rem', fontWeight: '700', marginTop: '2.5rem', marginBottom: '1rem', borderBottom: '2px solid #10b981', paddingBottom: '0.5rem'}} {...props} />,
                  h3: ({node, ...props}) => <h3 style={{fontSize: '1.5rem', fontWeight: '600', marginTop: '2rem', marginBottom: '0.75rem'}} {...props} />,
                  ul: ({node, ...props}) => <ul style={{marginLeft: '2rem', marginBottom: '1.5rem'}} {...props} />,
                  ol: ({node, ...props}) => <ol style={{marginLeft: '2rem', marginBottom: '1.5rem'}} {...props} />,
                  li: ({node, ...props}) => <li style={{marginBottom: '0.5rem'}} {...props} />
                }}
              >
                {selectedArticle.content}
              </ReactMarkdown>
            </div>

            {selectedArticle.tags && selectedArticle.tags.length > 0 && (
              <div className="article-tags">
                <strong>Tags:</strong>
                {selectedArticle.tags.map((tag, index) => (
                  <span key={index} className="tag">{tag}</span>
                ))}
              </div>
            )}
          </article>
        </main>
      </div>
    );
  }

  return (
    <div className="blog-page">
      <header className="blog-header">
        <div className="blog-header-container">
          <button onClick={() => navigate('/')} className="back-button">
            ← Volver al inicio
          </button>
          <h1 className="blog-title">📝 Blog GuaraniAppStore</h1>
          <p className="blog-subtitle">Insights sobre IA, automatización, transformación digital y cryptomonedas</p>
        </div>
      </header>

      <main className="blog-content">
        <div className="blog-container">
          {loading ? (
            <div className="loading-container">
              <Spin size="large" />
            </div>
          ) : articles.length === 0 ? (
            <div className="coming-soon-box">
              <Empty
                description="Aún no hay artículos publicados"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
              />
              <p className="mt-4">
                Estamos preparando contenido increíble. ¡Vuelve pronto!
              </p>
            </div>
          ) : (
            <div className="articles-grid">
              {articles.map((article) => (
                <article key={article.id} className="article-card">
                  {article.image_url && (
                    <img 
                      src={article.image_url} 
                      alt={article.title}
                      className="article-image"
                    />
                  )}
                  
                  <div className="article-body">
                    <h2 className="article-card-title">{article.title}</h2>
                    <p className="article-excerpt">{article.excerpt}</p>
                    
                    <div className="article-card-footer">
                      <div className="article-author">
                        <div>
                          <div className="author-name-small">{article.author_name}</div>
                          <div className="publish-date">{formatDate(article.published_at)}</div>
                        </div>
                      </div>
                      
                      <button 
                        onClick={() => handleReadArticle(article.slug)}
                        className="read-more-btn"
                      >
                        Leer más →
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </main>

      <footer className="blog-footer">
        <div className="blog-footer-container">
          <p>© {new Date().getFullYear()} GuaraniAppStore. Todos los derechos reservados.</p>
        </div>
      </footer>
    </div>
  );
};

export default Blog;
