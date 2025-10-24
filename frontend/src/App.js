import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css';
import LandingPage from './pages/LandingPage';
import CheckoutPage from './pages/CheckoutPage';
import Dashboard from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';
import CryptoSuite from './pages/services/CryptoSuite';
import AsistenteDirectivos from './pages/services/AsistenteDirectivos';
import PreseleccionCurricular from './pages/services/PreseleccionCurricular';
import OrganizadorFacturas from './pages/services/OrganizadorFacturas';
import OrganizadorAgenda from './pages/services/OrganizadorAgenda';
import ConsultoriaTecnica from './pages/services/ConsultoriaTecnica';
import GeneradorBlogs from './pages/services/GeneradorBlogs';
import AutomatizacionEcommerce from './pages/services/AutomatizacionEcommerce';
import AutomatizacionRedesSociales from './pages/services/AutomatizacionRedesSociales';
import ProspeccionComercial from './pages/services/ProspeccionComercial';
import AgenteVentasIA from './pages/services/AgenteVentasIA';
import FAQ from './pages/FAQ';
import TermsConditions from './pages/TermsConditions';
import PrivacyPolicy from './pages/PrivacyPolicy';
import Blog from './pages/Blog';
import BlogAdminPanel from './pages/BlogAdminPanel';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function App() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      const response = await axios.get(`${API}/services`);
      
      // Definir servicios "próximamente" - actualizar según se desarrollen
      const proximamenteList = [
        'Automatización y Gestión de E-commerce',
        'Automatización de Contenidos en redes sociales',
        'Generador de Blogs Automatizado y SEO',
        'Agente de Ventas IA'
      ];
      
      const allServices = response.data.services || response.data;
      
      // Marcar servicios próximamente
      const servicesWithStatus = allServices.map(service => ({
        ...service,
        status: proximamenteList.includes(service.name) ? 'coming_soon' : (service.status || 'active')
      }));
      
      // Separar y reordenar: crypto primero, luego activos, luego próximamente
      const cryptoService = servicesWithStatus.find(s => s.slug === 'suite-crypto' || s.name.toLowerCase().includes('crypto'));
      const activeServices = servicesWithStatus.filter(s => s.status === 'active' && s.slug !== 'suite-crypto' && !s.name.toLowerCase().includes('crypto'));
      const comingSoonServices = servicesWithStatus.filter(s => s.status === 'coming_soon');
      
      const orderedServices = [];
      if (cryptoService) orderedServices.push(cryptoService);
      orderedServices.push(...activeServices);
      orderedServices.push(...comingSoonServices);
      
      setServices(orderedServices);
    } catch (error) {
      console.error('Error fetching services:', error);
    }
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage services={services} />} />
        <Route path="/checkout/:serviceId" element={<CheckoutPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/services/crypto-suite" element={<CryptoSuite />} />
        <Route path="/services/asistente-directivos" element={<AsistenteDirectivos />} />
        <Route path="/services/preseleccion-curricular" element={<PreseleccionCurricular />} />
        <Route path="/services/organizador-facturas" element={<OrganizadorFacturas />} />
        <Route path="/services/organizador-agenda" element={<OrganizadorAgenda />} />
        <Route path="/services/consultoria-tecnica" element={<ConsultoriaTecnica />} />
        <Route path="/services/generador-blogs" element={<GeneradorBlogs />} />
        <Route path="/services/automatizacion-ecommerce" element={<AutomatizacionEcommerce />} />
        <Route path="/services/automatizacion-redes-sociales" element={<AutomatizacionRedesSociales />} />
        <Route path="/services/prospeccion-comercial" element={<ProspeccionComercial />} />
        <Route path="/services/agente-ventas-ia" element={<AgenteVentasIA />} />
        <Route path="/faq" element={<FAQ />} />
        <Route path="/terms" element={<TermsConditions />} />
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/blog" element={<Blog />} />
        <Route path="/admin/blog" element={<BlogAdminPanel />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
