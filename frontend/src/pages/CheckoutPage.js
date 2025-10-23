import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './CheckoutPage.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CheckoutPage = () => {
  const { serviceId } = useParams();
  const navigate = useNavigate();
  
  const [service, setService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [processing, setProcessing] = useState(false);
  
  // Checkout state
  const [planType, setPlanType] = useState('annual'); // 'monthly', 'annual', 'one_time'
  const [platform, setPlatform] = useState('whatsapp'); // 'whatsapp', 'telegram', 'web', null
  const [paymentMethod, setPaymentMethod] = useState('pagopar'); // 'pagopar', 'btc', 'eth', 'usdt'
  
  // Calculated values
  const [basePrice, setBasePrice] = useState(0);
  const [discount, setDiscount] = useState(0);
  const [finalPrice, setFinalPrice] = useState(0);
  
  // Order result
  const [order, setOrder] = useState(null);

  useEffect(() => {
    fetchService();
  }, [serviceId]);

  useEffect(() => {
    calculatePrice();
  }, [service, planType, platform, paymentMethod]);

  const fetchService = async () => {
    try {
      const response = await axios.get(`${API}/services`);
      const foundService = response.data.find(s => s.id === serviceId);
      
      if (!foundService) {
        setError('Servicio no encontrado');
        setLoading(false);
        return;
      }
      
      setService(foundService);
      
      // Set default platform based on service
      if (foundService.slug === 'organizador-facturas' || 
          foundService.slug === 'organizador-agenda' ||
          foundService.slug === 'generador-blogs' ||
          foundService.slug === 'ecommerce-automation' ||
          foundService.slug === 'redes-sociales') {
        setPlatform('web');
      }
      
      // Set default plan type
      if (foundService.slug === 'consultoria-tecnica' || 
          foundService.slug === 'prospeccion-comercial') {
        setPlanType('one_time');
      }
      
      setLoading(false);
    } catch (e) {
      setError('Error al cargar el servicio');
      setLoading(false);
    }
  };

  const calculatePrice = () => {
    if (!service) return;
    
    let price = 0;
    
    // Get base price
    if (planType === 'monthly') {
      price = service.price_monthly;
    } else if (planType === 'annual') {
      price = service.price_annual;
    } else if (planType === 'one_time') {
      price = service.price_monthly; // One-time uses monthly price
    }
    
    setBasePrice(price);
    
    // Calculate discount
    let totalDiscount = 0;
    
    // Telegram discount (20%)
    if (platform === 'telegram') {
      totalDiscount += 20;
    }
    
    // Crypto discount (25%) - ONLY BTC and ETH
    if (['btc', 'eth'].includes(paymentMethod)) {
      totalDiscount += 25;
    }
    
    setDiscount(totalDiscount);
    
    // Calculate final price
    const final = price * (1 - totalDiscount / 100);
    setFinalPrice(final);
  };

  const formatPrice = (price) => {
    return 'Gs. ' + new Intl.NumberFormat('es-PY', {
      minimumFractionDigits: 0
    }).format(price);
  };

  const handleCheckout = async () => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Por favor inicia sesión para continuar');
      navigate('/');
      return;
    }

    setProcessing(true);
    setError('');

    try {
      const response = await axios.post(
        `${API}/checkout/create-order`,
        {
          service_id: serviceId,
          plan_type: planType,
          platform: platform === 'web' ? null : platform,
          payment_method: paymentMethod
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setOrder(response.data);
      setProcessing(false);
    } catch (e) {
      setError(e.response?.data?.detail || 'Error al procesar el pago');
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="checkout-page">
        <div className="max-w-4xl mx-auto px-6 py-12">
          <p className="text-center text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  if (error && !service) {
    return (
      <div className="checkout-page">
        <div className="max-w-4xl mx-auto px-6 py-12">
          <div className="bg-red-50 border-2 border-red-300 rounded-lg p-6 text-center">
            <p className="text-red-700 font-semibold">{error}</p>
            <button
              onClick={() => navigate('/')}
              className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Volver al inicio
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Show order result (payment instructions)
  if (order) {
    return (
      <div className="checkout-page min-h-screen py-12 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="glass-strong rounded-2xl p-8 border-2 border-emerald-400">
            <div className="text-center mb-8">
              <div className="w-20 h-20 bg-emerald-500 rounded-full mx-auto mb-4 flex items-center justify-center">
                <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold text-emerald-900 mb-2">¡Orden Creada!</h2>
              <p className="text-gray-600">Orden #{order.order_number}</p>
            </div>

            {/* Pagopar Payment */}
            {order.payment_method === 'pagopar' && order.payment_url && (
              <div className="bg-white rounded-xl p-6 mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Completar Pago con Pagopar</h3>
                <p className="text-gray-600 mb-6">Haz clic en el botón para completar tu pago de forma segura</p>
                <a
                  href={order.payment_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-center py-4 rounded-xl font-bold text-lg hover:from-emerald-600 hover:to-teal-700"
                >
                  Pagar {formatPrice(order.final_price)} con Pagopar
                </a>
              </div>
            )}

            {/* Crypto Payment */}
            {['btc', 'eth', 'usdt'].includes(order.payment_method) && (
              <div className="bg-white rounded-xl p-6 mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  Instrucciones de Pago - {order.payment_method.toUpperCase()}
                </h3>
                
                <div className="space-y-4">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600 mb-2">Enviar exactamente:</p>
                    <p className="text-2xl font-bold text-emerald-700">{order.crypto_amount} {order.payment_method.toUpperCase()}</p>
                    <p className="text-xs text-gray-500 mt-1">Valor: {formatPrice(order.final_price)}</p>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4">
                    <p className="text-sm text-gray-600 mb-2">A la dirección:</p>
                    <div className="flex items-center gap-2">
                      <code className="flex-1 bg-white px-3 py-2 rounded border text-sm break-all">
                        {order.crypto_address}
                      </code>
                      <button
                        onClick={() => {
                          navigator.clipboard.writeText(order.crypto_address);
                          alert('Dirección copiada al portapapeles');
                        }}
                        className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 text-sm font-semibold"
                      >
                        Copiar
                      </button>
                    </div>
                    {order.payment_method === 'usdt' && (
                      <p className="text-xs text-orange-600 font-semibold mt-2">
                        ⚠️ Red: Ethereum (ERC-20) - No envíes por otra red
                      </p>
                    )}
                  </div>

                  <div className="bg-yellow-50 border-2 border-yellow-300 rounded-lg p-4">
                    <p className="text-sm font-semibold text-yellow-800 mb-2">⚡ Importante:</p>
                    <ul className="text-sm text-yellow-700 space-y-1 list-disc list-inside">
                      <li>Envía el monto exacto indicado</li>
                      <li>Usa la red correcta ({order.payment_method === 'btc' ? 'Bitcoin' : order.payment_method === 'usdt' ? 'Ethereum (ERC-20)' : 'Ethereum'})</li>
                      <li>Una vez enviado, ingresa el Transaction Hash abajo</li>
                    </ul>
                  </div>

                  <CryptoVerificationForm orderId={order.id} />
                </div>
              </div>
            )}

            <div className="text-center">
              <button
                onClick={() => navigate('/')}
                className="text-emerald-600 hover:text-emerald-700 font-semibold"
              >
                ← Volver al inicio
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Checkout form
  return (
    <div className="checkout-page min-h-screen py-12 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <button
            onClick={() => navigate('/')}
            className="text-emerald-600 hover:text-emerald-700 font-semibold mb-4"
          >
            ← Volver
          </button>
          <h1 className="text-4xl font-bold text-gray-900">Checkout</h1>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Checkout Options */}
          <div className="lg:col-span-2 space-y-6">
            {/* Service Info */}
            <div className="glass-strong rounded-2xl p-6 border-2 border-gray-200">
              <h2 className="text-2xl font-bold text-emerald-700 mb-2">{service.name}</h2>
              <p className="text-gray-600">{service.description}</p>
            </div>

            {/* Plan Selection */}
            <div className="glass-strong rounded-2xl p-6 border-2 border-gray-200">
              <h3 className="text-xl font-bold text-gray-900 mb-4">1. Selecciona tu plan</h3>
              <div className="space-y-3">
                {service.price_monthly > 0 && planType !== 'one_time' && (
                  <>
                    <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition">
                      <input
                        type="radio"
                        name="planType"
                        value="monthly"
                        checked={planType === 'monthly'}
                        onChange={(e) => setPlanType(e.target.value)}
                        className="w-5 h-5 text-emerald-600"
                      />
                      <div className="ml-4 flex-1">
                        <p className="font-semibold text-gray-900">Mensual</p>
                        <p className="text-sm text-gray-600">{formatPrice(service.price_monthly)}/mes</p>
                      </div>
                    </label>

                    {service.price_annual > 0 && (
                      <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition relative">
                        <input
                          type="radio"
                          name="planType"
                          value="annual"
                          checked={planType === 'annual'}
                          onChange={(e) => setPlanType(e.target.value)}
                          className="w-5 h-5 text-emerald-600"
                        />
                        <div className="ml-4 flex-1">
                          <p className="font-semibold text-gray-900">Anual</p>
                          <p className="text-sm text-gray-600">{formatPrice(service.price_annual)}/año</p>
                          <p className="text-xs text-green-600 font-semibold">💰 Ahorras 2 meses</p>
                        </div>
                        <div className="absolute -top-2 -right-2 bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                          RECOMENDADO
                        </div>
                      </label>
                    )}
                  </>
                )}

                {planType === 'one_time' && (
                  <div className="p-4 bg-purple-50 border-2 border-purple-300 rounded-xl">
                    <p className="font-semibold text-purple-800">💎 Pago Único</p>
                    <p className="text-sm text-purple-600">No caduca - Usa bajo demanda</p>
                  </div>
                )}
              </div>
            </div>

            {/* Platform Selection */}
            {!['organizador-facturas', 'organizador-agenda', 'generador-blogs', 'ecommerce-automation', 'redes-sociales', 'consultoria-tecnica', 'prospeccion-comercial', 'suite-crypto'].includes(service.slug) && (
              <div className="glass-strong rounded-2xl p-6 border-2 border-gray-200">
                <h3 className="text-xl font-bold text-gray-900 mb-4">2. Selecciona la plataforma</h3>
                <div className="space-y-3">
                  <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition">
                    <input
                      type="radio"
                      name="platform"
                      value="whatsapp"
                      checked={platform === 'whatsapp'}
                      onChange={(e) => setPlatform(e.target.value)}
                      className="w-5 h-5 text-emerald-600"
                    />
                    <div className="ml-4">
                      <p className="font-semibold text-gray-900">💚 WhatsApp</p>
                      <p className="text-sm text-gray-600">Precio estándar</p>
                    </div>
                  </label>

                  <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition relative">
                    <input
                      type="radio"
                      name="platform"
                      value="telegram"
                      checked={platform === 'telegram'}
                      onChange={(e) => setPlatform(e.target.value)}
                      className="w-5 h-5 text-emerald-600"
                    />
                    <div className="ml-4">
                      <p className="font-semibold text-gray-900">✈️ Telegram</p>
                      <p className="text-sm text-emerald-600 font-semibold">20% más barato - Más estable</p>
                    </div>
                    <div className="absolute -top-2 -right-2 bg-emerald-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                      -20%
                    </div>
                  </label>
                </div>
              </div>
            )}

            {/* Payment Method */}
            <div className="glass-strong rounded-2xl p-6 border-2 border-gray-200">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                {['organizador-facturas', 'organizador-agenda', 'generador-blogs', 'ecommerce-automation', 'redes-sociales', 'consultoria-tecnica', 'prospeccion-comercial', 'suite-crypto'].includes(service.slug) ? '2' : '3'}. Método de pago
              </h3>
              <div className="space-y-3">
                <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="pagopar"
                    checked={paymentMethod === 'pagopar'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-5 h-5 text-emerald-600"
                  />
                  <div className="ml-4 flex items-center gap-3">
                    <img src="/assets/payment/pyg.png" alt="Guaraníes" className="w-10 h-10 rounded" />
                    <div>
                      <p className="font-semibold text-gray-900">Guaraníes (PYG)</p>
                      <p className="text-sm text-gray-600">Pagopar - Pago local</p>
                    </div>
                  </div>
                </label>

                <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition relative">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="btc"
                    checked={paymentMethod === 'btc'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-5 h-5 text-emerald-600"
                  />
                  <div className="ml-4 flex items-center gap-3">
                    <img src="/assets/payment/btc.png" alt="Bitcoin" className="w-10 h-10 rounded" />
                    <div>
                      <p className="font-semibold text-gray-900">Bitcoin (BTC)</p>
                      <p className="text-sm text-orange-600 font-semibold">25% de descuento</p>
                    </div>
                  </div>
                  <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                    -25%
                  </div>
                </label>

                <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition relative">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="eth"
                    checked={paymentMethod === 'eth'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-5 h-5 text-emerald-600"
                  />
                  <div className="ml-4 flex items-center gap-3">
                    <img src="/assets/payment/eth.png" alt="Ethereum" className="w-10 h-10 rounded" />
                    <div>
                      <p className="font-semibold text-gray-900">Ethereum (ETH)</p>
                      <p className="text-sm text-orange-600 font-semibold">25% de descuento</p>
                    </div>
                  </div>
                  <div className="absolute -top-2 -right-2 bg-orange-500 text-white text-xs font-bold px-3 py-1 rounded-full">
                    -25%
                  </div>
                </label>

                <label className="flex items-center p-4 border-2 rounded-xl cursor-pointer hover:border-emerald-400 transition">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="usdt"
                    checked={paymentMethod === 'usdt'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="w-5 h-5 text-emerald-600"
                  />
                  <div className="ml-4 flex items-center gap-3">
                    <img src="/assets/payment/usdt.png" alt="USDT" className="w-10 h-10 rounded" />
                    <div>
                      <p className="font-semibold text-gray-900">USDT (ERC-20)</p>
                      <p className="text-sm text-gray-600">Stablecoin en dólares</p>
                      <p className="text-xs text-gray-500">Red Ethereum</p>
                    </div>
                  </div>
                </label>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="glass-strong rounded-2xl p-6 border-2 border-emerald-400 sticky top-6">
              <h3 className="text-xl font-bold text-gray-900 mb-6">Resumen de Compra</h3>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-700">
                  <span>Servicio:</span>
                  <span className="font-semibold text-right">{service.name}</span>
                </div>
                
                <div className="flex justify-between text-gray-700">
                  <span>Plan:</span>
                  <span className="font-semibold capitalize">{planType === 'one_time' ? 'Pago Único' : planType === 'monthly' ? 'Mensual' : 'Anual'}</span>
                </div>
                
                {platform && platform !== 'web' && (
                  <div className="flex justify-between text-gray-700">
                    <span>Plataforma:</span>
                    <span className="font-semibold capitalize">{platform}</span>
                  </div>
                )}
                
                <div className="flex justify-between text-gray-700">
                  <span>Método de pago:</span>
                  <span className="font-semibold uppercase">{paymentMethod}</span>
                </div>
                
                <div className="border-t pt-4">
                  <div className="flex justify-between text-gray-600 mb-2">
                    <span>Precio base:</span>
                    <span>{formatPrice(basePrice)}</span>
                  </div>
                  
                  {discount > 0 && (
                    <div className="flex justify-between text-green-600 font-semibold mb-2">
                      <span>Descuento ({discount}%):</span>
                      <span>-{formatPrice(basePrice - finalPrice)}</span>
                    </div>
                  )}
                  
                  <div className="flex justify-between text-2xl font-bold text-emerald-700 pt-4 border-t">
                    <span>Total:</span>
                    <span>{formatPrice(finalPrice)}</span>
                  </div>
                </div>
              </div>

              {error && (
                <div className="bg-red-50 border-2 border-red-300 rounded-lg p-4 mb-4">
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              )}

              <button
                onClick={handleCheckout}
                disabled={processing || finalPrice === 0}
                className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed text-white py-4 rounded-xl font-bold text-lg shadow-lg"
              >
                {processing ? 'Procesando...' : 'Proceder al Pago'}
              </button>
              
              <p className="text-xs text-gray-500 text-center mt-4">
                🔒 Pago seguro y encriptado
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Component for crypto verification
const CryptoVerificationForm = ({ orderId }) => {
  const [txHash, setTxHash] = useState('');
  const [verifying, setVerifying] = useState(false);
  const [result, setResult] = useState(null);

  const handleVerify = async () => {
    if (!txHash.trim()) {
      alert('Por favor ingresa el Transaction Hash');
      return;
    }

    setVerifying(true);
    setResult(null);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${BACKEND_URL}/api/payments/crypto/verify`,
        {
          order_id: orderId,
          tx_hash: txHash
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setResult(response.data);
      setVerifying(false);
    } catch (e) {
      setResult({
        success: false,
        message: e.response?.data?.detail || 'Error al verificar la transacción'
      });
      setVerifying(false);
    }
  };

  return (
    <div className="bg-white rounded-lg p-4 border-2 border-gray-200">
      <h4 className="font-semibold text-gray-900 mb-3">Verificar Transacción</h4>
      
      <div className="space-y-3">
        <div>
          <label className="block text-sm text-gray-600 mb-1">Transaction Hash (TX Hash):</label>
          <input
            type="text"
            value={txHash}
            onChange={(e) => setTxHash(e.target.value)}
            placeholder="0x..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
          />
        </div>

        <button
          onClick={handleVerify}
          disabled={verifying || !txHash.trim()}
          className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white py-3 rounded-lg font-semibold"
        >
          {verifying ? 'Verificando...' : 'Verificar Pago'}
        </button>

        {result && (
          <div className={`p-4 rounded-lg ${result.success ? 'bg-green-50 border-2 border-green-300' : 'bg-yellow-50 border-2 border-yellow-300'}`}>
            <p className={`font-semibold ${result.success ? 'text-green-800' : 'text-yellow-800'}`}>
              {result.message}
            </p>
            {result.status === 'completed' && (
              <p className="text-sm text-green-600 mt-2">
                ✅ Tu pago ha sido confirmado. Recibirás un email con las instrucciones de acceso.
              </p>
            )}
            {result.status === 'pending' && (
              <p className="text-sm text-yellow-600 mt-2">
                ⏳ El pago está siendo procesado. Esto puede tardar unos minutos.
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default CheckoutPage;
