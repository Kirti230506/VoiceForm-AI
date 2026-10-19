import React, { useState, useEffect } from 'react';
import { Bot, X, Send, Lightbulb, HelpCircle, CheckCircle2, MessageSquare } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { queryAssistantChat, explainFormField } from '../services/api';

export const SmartAssistantModal = ({ activeFieldToExplain, onCloseFieldExplain }) => {
  const { lang, t } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [inputQuery, setInputQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: lang === 'hi' 
        ? 'नमस्ते! मैं वॉइसफॉर्म एआई सहायक हूँ। आप मुझसे सरकारी फॉर्म या योजनाओं के बारे में कुछ भी पूछ सकते हैं।'
        : lang === 'mr'
        ? 'नमस्कार! मी व्हॉइसफॉर्म एआय सहाय्यक आहे. आपण मला शासकीय अर्ज किंवा योजनांबद्दल काहीही विचारू शकता.'
        : 'Hello! I am your VoiceForm AI Assistant. How can I assist you with government forms or welfare schemes today?'
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [fieldExplanation, setFieldExplanation] = useState(null);

  // Quick prompt chips
  const QUICK_QUESTIONS = [
    { en: "Who is eligible for PM Kisan?", hi: "पीएम किसान के लिए कौन पात्र है?", mr: "पीएम किसानसाठी कोण पात्र आहे?" },
    { en: "What documents are required for Income Certificate?", hi: "आय प्रमाण पत्र के लिए क्या दस्तावेज चाहिए?", mr: "उत्पन्न दाखल्यासाठी काय कागदपत्रे लागतात?" },
    { en: "What is Ayushman Bharat coverage limit?", hi: "आयुष्मान भारत की बीमा सीमा क्या है?", mr: "आयुष्मान भारत मर्यादा किती आहे?" }
  ];

  // If a specific field was requested to be explained from the form
  useEffect(() => {
    if (activeFieldToExplain) {
      setIsOpen(true);
      fetchFieldExplanation(activeFieldToExplain);
    }
  }, [activeFieldToExplain, lang]);

  const fetchFieldExplanation = async (fieldId) => {
    try {
      const data = await explainFormField(fieldId, lang);
      setFieldExplanation(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSend = async (userText = null) => {
    const query = userText || inputQuery;
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    if (!userText) setInputQuery('');
    setLoading(true);

    try {
      const res = await queryAssistantChat(query, lang);
      setMessages((prev) => [...prev, { sender: 'ai', text: res.answer }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'ai', text: "Sorry, I am unable to connect to the assistant right now." }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button
        type="button"
        className="floating-assistant-btn btn"
        onClick={() => setIsOpen(true)}
        aria-label="Open Smart Form Assistant"
      >
        <span className="p-1 bg-white text-primary rounded-circle d-flex align-items-center justify-content-center">
          <Bot size={18} />
        </span>
        <span>{t('smartAssistant')}</span>
      </button>

      {/* Modal / Offcanvas Drawer */}
      {isOpen && (
        <div 
          className="modal fade show d-block" 
          tabIndex="-1" 
          role="dialog"
          style={{ backgroundColor: 'rgba(11, 37, 69, 0.55)', backdropFilter: 'blur(3px)' }}
        >
          <div className="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div className="modal-content shadow-lg border-0 rounded-4 overflow-hidden">
              {/* Header */}
              <div className="modal-header text-white" style={{ background: 'linear-gradient(135deg, #0B2545, #134074)' }}>
                <div className="d-flex align-items-center gap-2">
                  <div className="p-2 bg-white text-primary rounded-circle">
                    <Bot size={22} />
                  </div>
                  <div>
                    <h5 className="modal-title fw-bold mb-0">{t('smartAssistant')}</h5>
                    <small className="text-light opacity-75">Citizen Guidance & Form Explainer</small>
                  </div>
                </div>
                <button
                  type="button"
                  className="btn-close btn-close-white"
                  aria-label="Close"
                  onClick={() => {
                    setIsOpen(false);
                    setFieldExplanation(null);
                    if (onCloseFieldExplain) onCloseFieldExplain();
                  }}
                ></button>
              </div>

              {/* Body */}
              <div className="modal-body p-4" style={{ maxHeight: '65vh', overflowY: 'auto' }}>
                {/* Field Explanation Banner if active */}
                {fieldExplanation && (
                  <div className="alert alert-info border-info border-2 rounded-3 mb-4 shadow-sm">
                    <div className="d-flex align-items-start gap-2">
                      <Lightbulb size={24} className="text-primary flex-shrink-0 mt-1" />
                      <div>
                        <h6 className="fw-bold mb-1 text-primary">
                          Field Guide: {fieldExplanation.field_id.replace('_', ' ').toUpperCase()}
                        </h6>
                        <p className="mb-2 text-dark">{fieldExplanation.explanation}</p>
                        {fieldExplanation.example && (
                          <div className="badge bg-light text-dark border p-2 text-start">
                            <strong>Example:</strong> {fieldExplanation.example}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Chat History */}
                <div className="d-flex flex-column gap-3 mb-3">
                  {messages.map((m, idx) => (
                    <div
                      key={idx}
                      className={`d-flex ${m.sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`}
                    >
                      <div
                        className={`p-3 rounded-4 shadow-sm ${
                          m.sender === 'user'
                            ? 'bg-primary text-white'
                            : 'bg-light text-dark border'
                        }`}
                        style={{ maxWidth: '80%', fontSize: '0.94rem' }}
                      >
                        <div className="d-flex align-items-center gap-2 mb-1 opacity-75 small fw-semibold">
                          {m.sender === 'user' ? 'You' : 'VoiceForm AI'}
                        </div>
                        <div>{m.text}</div>
                      </div>
                    </div>
                  ))}

                  {loading && (
                    <div className="d-flex justify-content-start">
                      <div className="p-3 bg-light border rounded-4 text-muted small d-flex align-items-center gap-2">
                        <span className="spinner-border spinner-border-sm" role="status"></span>
                        VoiceForm AI is thinking...
                      </div>
                    </div>
                  )}
                </div>

                {/* Quick Question Chips */}
                <div className="mt-4 pt-3 border-top">
                  <div className="small text-muted mb-2 fw-medium">Suggested Questions:</div>
                  <div className="d-flex flex-wrap gap-2">
                    {QUICK_QUESTIONS.map((q, idx) => (
                      <button
                        key={idx}
                        type="button"
                        className="btn btn-outline-primary btn-sm rounded-pill text-start"
                        style={{ fontSize: '0.82rem' }}
                        onClick={() => handleSend(q[lang] || q.en)}
                      >
                        💡 {q[lang] || q.en}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Footer Input */}
              <div className="modal-footer bg-light border-top p-3">
                <form
                  className="w-100 d-flex gap-2"
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSend();
                  }}
                >
                  <input
                    type="text"
                    className="form-control rounded-pill px-3"
                    placeholder={t('typeQuestion')}
                    value={inputQuery}
                    onChange={(e) => setInputQuery(e.target.value)}
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    className="btn btn-primary rounded-pill px-4 d-flex align-items-center gap-1"
                    disabled={loading || !inputQuery.trim()}
                  >
                    <Send size={16} />
                    <span>{t('askBtn')}</span>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
