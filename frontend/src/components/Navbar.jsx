import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Mic, Globe, ShieldCheck, FileText, CheckCircle, Database } from 'lucide-react';


export const Navbar = ({ activePage, setActivePage }) => {
  const { lang, setLang, t } = useLanguage();

  return (
    <header>
      <div className="gov-top-bar" aria-hidden="true"></div>
      <nav className="navbar navbar-expand-lg vf-navbar navbar-dark sticky-top" aria-label="Main Navigation">
        <div className="container">
          <button 
            className="navbar-brand vf-brand btn btn-link text-decoration-none p-0 text-start"
            onClick={() => setActivePage('home')}
            aria-label="VoiceForm AI Home"
          >
            <div className="d-flex align-items-center gap-2">
              <span className="p-2 rounded-circle bg-white text-dark d-flex align-items-center justify-content-center shadow-sm" style={{ width: 42, height: 42 }}>
                <Mic className="text-danger" size={24} />
              </span>
              <div>
                <span className="fw-bold fs-4 tracking-wide text-white">VoiceForm AI</span>
                <span className="vf-brand-badge ms-2 d-none d-sm-inline-block">GovTech</span>
                <div className="text-light opacity-75 small" style={{ fontSize: '0.68rem', letterSpacing: '0.5px' }}>
                  DIGITAL INDIA CITIZEN ASSISTANT
                </div>
              </div>
            </div>
          </button>

          <button 
            className="navbar-toggler border-0" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarContent"
            aria-controls="navbarContent"
            aria-expanded="false" 
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse justify-content-end" id="navbarContent">
            <ul className="navbar-nav align-items-lg-center gap-1 my-2 my-lg-0">
              <li className="nav-item">
                <button 
                  className={`nav-link custom-nav btn btn-link text-decoration-none ${activePage === 'home' ? 'active' : ''}`}
                  onClick={() => setActivePage('home')}
                >
                  {t('navHome')}
                </button>
              </li>
              <li className="nav-item">
                <button 
                  className={`nav-link custom-nav btn btn-link text-decoration-none ${activePage === 'form' ? 'active' : ''}`}
                  onClick={() => setActivePage('form')}
                >
                  <FileText size={16} className="me-1 inline" />
                  {t('navVoiceForm')}
                </button>
              </li>
              <li className="nav-item">
                <button 
                  className={`nav-link custom-nav btn btn-link text-decoration-none ${activePage === 'schemes' ? 'active' : ''}`}
                  onClick={() => setActivePage('schemes')}
                >
                  <ShieldCheck size={16} className="me-1 inline" />
                  {t('navSchemes')}
                </button>
              </li>
              <li className="nav-item">
                <button 
                  className={`nav-link custom-nav btn btn-link text-decoration-none ${activePage === 'dataset' ? 'active' : ''}`}
                  onClick={() => setActivePage('dataset')}
                >
                  <Database size={16} className="me-1 inline" />
                  Dataset Studio
                </button>
              </li>
            </ul>


            {/* Language Selector */}
            <div className="d-flex align-items-center ms-lg-3 pt-2 pt-lg-0 border-top border-lg-0 border-secondary">
              <div className="dropdown">
                <button 
                  className="btn btn-sm btn-outline-light dropdown-toggle d-flex align-items-center gap-1 px-3 py-2 rounded-pill"
                  type="button"
                  id="languageDropdown"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <Globe size={15} />
                  <span className="fw-semibold">
                    {lang === 'en' ? 'English' : lang === 'hi' ? 'हिन्दी' : 'मराठी'}
                  </span>
                </button>
                <ul className="dropdown-menu dropdown-menu-end shadow" aria-labelledby="languageDropdown">
                  <li>
                    <button 
                      className={`dropdown-item d-flex align-items-center justify-content-between ${lang === 'en' ? 'active fw-bold' : ''}`}
                      onClick={() => setLang('en')}
                    >
                      English
                      {lang === 'en' && <CheckCircle size={14} className="ms-2" />}
                    </button>
                  </li>
                  <li>
                    <button 
                      className={`dropdown-item d-flex align-items-center justify-content-between ${lang === 'hi' ? 'active fw-bold' : ''}`}
                      onClick={() => setLang('hi')}
                    >
                      हिन्दी (Hindi)
                      {lang === 'hi' && <CheckCircle size={14} className="ms-2" />}
                    </button>
                  </li>
                  <li>
                    <button 
                      className={`dropdown-item d-flex align-items-center justify-content-between ${lang === 'mr' ? 'active fw-bold' : ''}`}
                      onClick={() => setLang('mr')}
                    >
                      मराठी (Marathi)
                      {lang === 'mr' && <CheckCircle size={14} className="ms-2" />}
                    </button>
                  </li>
                </ul>
              </div>
            </div>

          </div>
        </div>
      </nav>
    </header>
  );
};
