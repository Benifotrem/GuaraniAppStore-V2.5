import React, { useState } from 'react';
import { Button, Input, Select, Checkbox, message, Tag } from 'antd';
import { generateCustomArticle } from '../../utils/blogApi';

const { TextArea } = Input;
const { Option } = Select;

const GenerateArticleForm = ({ onSuccess, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    search_query: '',
    target_keywords: [],
    agent_id: null,
    tone: 'profesional',
    length: 'medium',
    include_faq: true
  });
  const [keywordInput, setKeywordInput] = useState('');

  const agents = [
    { id: null, name: 'Detectar automáticamente' },
    { id: 1, name: 'Junior Cucurella - Automatización' },
    { id: 2, name: 'Jacinto Torrelavega - E-commerce' },
    { id: 3, name: 'Alex Albiol - Marketing Digital' },
    { id: 4, name: 'Silvia Garcia - SEO y Contenido' },
    { id: 5, name: 'Blanca Garcia - Procesos' },
    { id: 6, name: 'Rocío Almeida - Prospección' }
  ];

  const handleAddKeyword = () => {
    if (keywordInput.trim() && formData.target_keywords.length < 10) {
      setFormData({
        ...formData,
        target_keywords: [...formData.target_keywords, keywordInput.trim()]
      });
      setKeywordInput('');
    }
  };

  const handleRemoveKeyword = (keyword) => {
    setFormData({
      ...formData,
      target_keywords: formData.target_keywords.filter(k => k !== keyword)
    });
  };

  const handleSubmit = async () => {
    if (!formData.search_query.trim()) {
      message.error('Por favor ingresa una consulta de búsqueda');
      return;
    }

    setLoading(true);
    try {
      const result = await generateCustomArticle(formData);
      message.success('¡Artículo generado! Revísalo en la cola de aprobación.');
      if (onSuccess) onSuccess(result);
    } catch (error) {
      console.error('Error generando artículo:', error);
      message.error(error.message || 'Error al generar el artículo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generate-article-form">
      <h2 className="text-2xl font-bold mb-4">🎨 Generar Nuevo Artículo</h2>

      {/* Consulta de búsqueda */}
      <div className="mb-4">
        <label className="block mb-2 font-semibold">📝 Consulta de búsqueda *</label>
        <TextArea
          rows={3}
          placeholder="Ejemplo: cómo automatizar prospección comercial con IA"
          value={formData.search_query}
          onChange={(e) => setFormData({ ...formData, search_query: e.target.value })}
        />
      </div>

      {/* Keywords objetivo */}
      <div className="mb-4">
        <label className="block mb-2 font-semibold">🔑 Keywords objetivo (opcional)</label>
        <div className="flex flex-wrap gap-2 mb-2">
          {formData.target_keywords.map((keyword, index) => (
            <Tag
              key={index}
              color="blue"
              closable
              onClose={() => handleRemoveKeyword(keyword)}
            >
              {keyword}
            </Tag>
          ))}
        </div>
        <div className="flex gap-2">
          <Input
            placeholder="Agregar keyword"
            value={keywordInput}
            onChange={(e) => setKeywordInput(e.target.value)}
            onPressEnter={handleAddKeyword}
          />
          <Button onClick={handleAddKeyword}>Agregar +</Button>
        </div>
      </div>

      {/* Opciones: Agente, Tono, Longitud */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block mb-2 font-semibold">👤 Agente</label>
          <Select
            value={formData.agent_id}
            onChange={(value) => setFormData({ ...formData, agent_id: value })}
            className="w-full"
            style={{ color: '#000' }}
            dropdownStyle={{ color: '#000' }}
            popupClassName="dropdown-black-text"
          >
            {agents.map(agent => (
              <Option 
                key={agent.id} 
                value={agent.id} 
                style={{ color: '#000', fontWeight: '500' }}
              >
                <span style={{ color: '#000', fontWeight: '500' }}>{agent.name}</span>
              </Option>
            ))}
          </Select>
        </div>

        <div>
          <label className="block mb-2 font-semibold">🎭 Tono</label>
          <Select
            value={formData.tone}
            onChange={(value) => setFormData({ ...formData, tone: value })}
            className="w-full"
            style={{ color: '#000' }}
            dropdownStyle={{ color: '#000' }}
            popupClassName="dropdown-black-text"
          >
            <Option value="profesional" style={{ color: '#000', fontWeight: '500' }}>
              <span style={{ color: '#000', fontWeight: '500' }}>Profesional</span>
            </Option>
            <Option value="casual" style={{ color: '#000', fontWeight: '500' }}>
              <span style={{ color: '#000', fontWeight: '500' }}>Casual</span>
            </Option>
            <Option value="técnico" style={{ color: '#000', fontWeight: '500' }}>
              <span style={{ color: '#000', fontWeight: '500' }}>Técnico</span>
            </Option>
          </Select>
        </div>

        <div>
          <label className="block mb-2 font-semibold">📏 Longitud</label>
          <Select
            value={formData.length}
            onChange={(value) => setFormData({ ...formData, length: value })}
            className="w-full"
            style={{ color: '#000' }}
            dropdownStyle={{ color: '#000' }}
            popupClassName="dropdown-black-text"
          >
            <Option value="short" style={{ color: '#000', fontWeight: '500' }}>
              <span style={{ color: '#000', fontWeight: '500' }}>Short (800 palabras)</span>
            </Option>
            <Option value="medium" style={{ color: '#000', fontWeight: '500' }}>
              <span style={{ color: '#000', fontWeight: '500' }}>Medium (1200 palabras)</span>
            </Option>
            <Option value="long" style={{ color: '#000', fontWeight: '500' }}>
              <span style={{ color: '#000', fontWeight: '500' }}>Long (1500 palabras)</span>
            </Option>
          </Select>
        </div>
      </div>

      {/* Opciones adicionales */}
      <div className="mb-4">
        <label className="block mb-2 font-semibold">⚙️ Opciones adicionales</label>
        <Checkbox
          checked={formData.include_faq}
          onChange={(e) => setFormData({ ...formData, include_faq: e.target.checked })}
        >
          Incluir sección de preguntas frecuentes (FAQ)
        </Checkbox>
      </div>

      {/* Nota informativa */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
        <p className="text-sm">
          <strong>📌 Nota:</strong> El artículo será generado y quedará en cola de aprobación.
          Podrás revisarlo antes de publicarlo.
        </p>
      </div>

      {/* Botones */}
      <div className="flex justify-end gap-2">
        <Button onClick={onCancel}>Cancelar</Button>
        <Button
          type="primary"
          loading={loading}
          onClick={handleSubmit}
        >
          Generar Artículo
        </Button>
      </div>
    </div>
  );
};

export default GenerateArticleForm;
