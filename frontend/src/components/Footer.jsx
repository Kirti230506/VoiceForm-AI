import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Shield, PhoneCall, CheckCircle, Heart } from 'lucide-react';

export const Footer = () => {
  const { t } = useLanguage();

  return (
    <footer className="mt-5 border-top bg-white pt-4 pb-3" role="contentinfo">
      <div className="container">
        <div className="row g-4 mb-4">
          <div className="col-md-5">
            <h6 className="fw-bold text-primary d-flex align-items-center gap-2">
              <Shield size={18} className="text-danger" />
              VoiceForm AI
            </h6>
            <p className="text-muted small mb-2">
              An AI-assisted citizen empowerment platform enabling voice-first government form filling and automated scheme eligibility matching. Built with OpenAI Whisper, Python NLP/NER, and modern Web accessibility standards.
            </p>
            <div className="badge bg-warning text-dark p-2 text-wrap text-start mt-1">
              ⚠️ {t('disclaimerText')}
            </div>
          </div>

          <div className="col-md-3">
            <h6 className="fw-bold mb-3 small text-uppercase text-secondary">Key Services</h6>
            <ul className="list-unstyled small text-muted d-flex flex-column gap-2 mb-0">
              <li>Income & Caste Certificates</li>
              <li>PM Kisan Samman Nidhi</li>
              <li>Ayushman Bharat PM-JAY</li>
              <li>PMAY Housing Assistance</li>
              <li>Senior Citizen Pension</li>
            </ul>
          </div>

          <div className="col-md-4">
            <h6 className="fw-bold mb-3 small text-uppercase text-secondary">Citizen Support & Accessibility</h6>
            <div className="d-flex align-items-center gap-2 mb-2 text-muted small">
              <PhoneCall size={16} className="text-success" />
              <span>National Citizen Toll-Free: <strong>1800-111-555</strong></span>
            </div>
            <div className="d-flex align-items-center gap-2 text-muted small">
              <CheckCircle size={16} className="text-primary" />
              <span>Languages: English, हिन्दी, मराठी</span>
            </div>
            <div className="mt-3 p-2 bg-light rounded text-muted small border">
              Designed as an AIML Capstone Prototype for Next-Gen Public Administration.
            </div>
          </div>
        </div>

        <div className="border-top pt-3 text-center text-muted small">
          © {new Date().getFullYear()} VoiceForm AI — Digital India Initiative Prototype. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
};
