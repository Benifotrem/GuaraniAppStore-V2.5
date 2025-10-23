import React, { useState, useEffect } from 'react';
import { Button, Card, Statistic, Row, Col, Modal, message, Spin, Empty, Tag } from 'antd';
import {
  FileTextOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  EyeOutlined,
  PlusOutlined,
  CheckOutlined,
  CloseOutlined
} from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';
import GenerateArticleForm from '../components/blog/GenerateArticleForm';
import {
  getBlogStats,
  getPendingArticles,
  approveArticle,
  rejectArticle
} from '../utils/blogApi';
import './BlogAdminPanel.css';

const BlogAdminPanel = () => {
  const [stats, setStats] = useState(null);
  const [pendingArticles, setPendingArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [showGenerateForm, setShowGenerateForm] = useState(false);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsData, pendingData] = await Promise.all([
        getBlogStats(),
        getPendingArticles()
      ]);
      setStats(statsData);
      setPendingArticles(pendingData);
    } catch (error) {
      console.error('Error cargando datos:', error);
      message.error('Error al cargar datos del blog');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSuccess = () => {
    setShowGenerateForm(false);
    loadData();
  };

  const handlePreview = (article) => {
    setSelectedArticle(article);
    setPreviewVisible(true);
  };

  const handleApprove = async (articleId) => {
    try {
      await approveArticle(articleId);
      message.success('¡Artículo aprobado y publicado!');
      loadData();
      setPreviewVisible(false);
    } catch (error) {
      console.error('Error aprobando artículo:', error);
      message.error('Error al aprobar artículo');
    }
  };

  const handleReject = async (articleId) => {
    try {
      await rejectArticle(articleId);
      message.success('Artículo rechazado');
      loadData();
      setPreviewVisible(false);
    } catch (error) {
      console.error('Error rechazando artículo:', error);
      message.error('Error al rechazar artículo');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-PY', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">📝 Blog Admin Panel</h1>
          <p className="text-gray-600 mt-2">
            Gestión de artículos automatizados y generación bajo demanda
          </p>
        </div>
        <Button
          type="primary"
          size="large"
          icon={<PlusOutlined />}
          onClick={() => setShowGenerateForm(true)}
          style={{ backgroundColor: '#10b981' }}
        >
          Generar Nuevo Artículo
        </Button>
      </div>

      {/* Estadísticas */}
      {stats && (
        <Row gutter={16} className="mb-6">
          <Col span={6}>
            <Card>
              <Statistic
                title="Total de Artículos"
                value={stats.total_posts}
                prefix={<FileTextOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Artículos Publicados"
                value={stats.published_posts}
                prefix={<CheckCircleOutlined />}
                valueStyle={{ color: '#10b981' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Pendientes de Aprobación"
                value={stats.draft_posts}
                prefix={<ClockCircleOutlined />}
                valueStyle={{ color: '#f59e0b' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Vistas Totales"
                value={stats.total_views}
                prefix={<EyeOutlined />}
              />
            </Card>
          </Col>
        </Row>
      )}

      {/* Artículos pendientes */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">
          ⏳ Artículos Pendientes de Aprobación ({pendingArticles.length})
        </h2>
        
        {pendingArticles.length === 0 ? (
          <Empty
            description="No hay artículos pendientes de aprobación"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        ) : (
          <div className="space-y-4">
            {pendingArticles.map((article) => (
              <Card
                key={article.id}
                className="hover:shadow-lg transition-shadow"
                bordered={false}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-2xl">⏰</span>
                      <h3 className="text-lg font-bold mb-0">{article.title}</h3>
                    </div>
                    
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>
                        <strong>{article.author_name}</strong> - {article.author_role}
                      </div>
                      <div>
                        Solicitado: {formatDate(article.requested_at)}
                      </div>
                      <div>
                        Búsqueda: <em>"{article.search_query}"</em>
                      </div>
                      <div>
                        {article.reading_time || 5} min lectura
                      </div>
                    </div>

                    {/* Tags */}
                    <div className="mt-3">
                      {article.tags?.slice(0, 4).map((tag, index) => (
                        <Tag key={index} color="blue">{tag}</Tag>
                      ))}
                    </div>
                  </div>

                  {/* Acciones */}
                  <div className="flex gap-2 ml-4">
                    <Button
                      icon={<EyeOutlined />}
                      onClick={() => handlePreview(article)}
                    >
                      Preview
                    </Button>
                    <Button
                      type="primary"
                      icon={<CheckOutlined />}
                      onClick={() => handleApprove(article.id)}
                      style={{ backgroundColor: '#10b981', borderColor: '#10b981' }}
                    >
                      Aprobar
                    </Button>
                    <Button
                      danger
                      icon={<CloseOutlined />}
                      onClick={() => handleReject(article.id)}
                    >
                      Rechazar
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Modal: Generar artículo */}
      <Modal
        open={showGenerateForm}
        onCancel={() => setShowGenerateForm(false)}
        footer={null}
        width={800}
      >
        <GenerateArticleForm
          onSuccess={handleGenerateSuccess}
          onCancel={() => setShowGenerateForm(false)}
        />
      </Modal>

      {/* Modal: Preview de artículo */}
      <Modal
        title="👁️ Preview de Artículo"
        open={previewVisible}
        onCancel={() => setPreviewVisible(false)}
        width={1200}
        footer={[
          <Button
            key="reject"
            danger
            onClick={() => handleReject(selectedArticle?.id)}
          >
            Rechazar y Eliminar
          </Button>,
          <Button
            key="approve"
            type="primary"
            onClick={() => handleApprove(selectedArticle?.id)}
            style={{ backgroundColor: '#10b981', borderColor: '#10b981' }}
          >
            Aprobar y Publicar
          </Button>
        ]}
      >
        {selectedArticle && (
          <div className="grid grid-cols-12 gap-6">
            {/* Sidebar: Metadata */}
            <div className="col-span-4 bg-gray-50 p-4 rounded">
              <h3 className="font-bold mb-4">📊 Metadata del Artículo</h3>
              
              <div className="space-y-3 text-sm">
                <div>
                  <strong>🕒 Solicitado:</strong><br />
                  {formatDate(selectedArticle.requested_at)}
                </div>
                
                <hr />
                
                <div>
                  <strong>🔍 Búsqueda original:</strong><br />
                  <em>"{selectedArticle.search_query}"</em>
                </div>
                
                <hr />
                
                <div>
                  <strong>👤 Agente:</strong><br />
                  {selectedArticle.author_name}<br />
                  <span className="text-gray-600">{selectedArticle.author_role}</span>
                </div>
                
                <hr />
                
                <div>
                  <strong>📏 Longitud:</strong><br />
                  {selectedArticle.content?.split(' ').length || 0} palabras<br />
                  (~{selectedArticle.reading_time || 5} min lectura)
                </div>
                
                {selectedArticle.keywords && selectedArticle.keywords.length > 0 && (
                  <>
                    <hr />
                    <div>
                      <strong>🔑 Keywords:</strong>
                      <ul className="list-disc list-inside mt-2">
                        {selectedArticle.keywords.map((keyword, index) => (
                          <li key={index}>{keyword}</li>
                        ))}
                      </ul>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Main content: Vista del artículo */}
            <div className="col-span-8 max-h-[600px] overflow-y-auto">
              {/* Imagen */}
              {selectedArticle.image_url && (
                <img
                  src={selectedArticle.image_url}
                  alt={selectedArticle.title}
                  className="w-full h-64 object-cover rounded mb-4"
                />
              )}

              {/* Título */}
              <h1 className="text-3xl font-bold mb-2">{selectedArticle.title}</h1>

              {/* Excerpt */}
              <p className="text-lg text-gray-600 mb-4 italic">{selectedArticle.excerpt}</p>

              <hr className="my-4" />

              {/* Contenido en Markdown */}
              <div className="prose prose-lg max-w-none">
                <ReactMarkdown>{selectedArticle.content}</ReactMarkdown>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default BlogAdminPanel;
