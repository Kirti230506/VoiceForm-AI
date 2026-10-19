import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { 
  Mic, 
  Sparkles, 
  FileText, 
  ShieldCheck, 
  ArrowRight, 
  CheckCircle2, 
  Languages, 
  HelpCircle,
  Landmark,
  HeartHandshake
} from 'lucide-react';

export const Home = ({ onNavigate }) => {
  const { lang, t } = useLanguage();

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section text-center">
        <div className="container py-4">
          <div className="row justify-content-center">
            <div className="col-lg-9">
              <div className="d-inline-flex align-items-center gap-2 bg-white bg-opacity-10 border border-white border-opacity-25 rounded-pill px-3 py-1 mb-3">
                <span className="badge bg-danger rounded-pill px-2 py-1">AI-Powered</span>
                <span className="small text-white">Digital India e-Governance Prototype</span>
              </div>

              <h1 className="display-4 fw-bold mb-3 tracking-tight">
                {t('tagline')}
              </h1>

              <p className="lead mb-4 text-light opacity-90 px-md-5">
                VoiceForm AI breaks the barrier of complicated paperwork. Simply speak naturally in <strong>English, Hindi, or Marathi</strong>, and let Whisper AI & NLP extract your information and fill government applications automatically.
              </p>

              <div className="d-flex flex-wrap gap-3 justify-content-center pt-2">
                <button
                  type="button"
                  className="btn btn-gov-primary btn-lg px-4 py-3 shadow"
                  onClick={() => onNavigate('form')}
                >
                  <Mic size={22} />
                  <span>{t('startVoiceForm')}</span>
                  <ArrowRight size={18} className="ms-1" />
                </button>

                <button
                  type="button"
                  className="btn btn-gov-secondary btn-lg px-4 py-3 shadow"
                  onClick={() => onNavigate('schemes')}
                >
                  <ShieldCheck size={22} className="text-primary" />
                  <span>{t('checkEligibility')}</span>
                </button>
              </div>

              <div className="mt-4 pt-3 d-flex flex-wrap justify-content-center gap-4 text-light opacity-80 small">
                <div className="d-flex align-items-center gap-2">
                  <CheckCircle2 size={16} className="text-warning" />
                  <span>Zero Manual Typing Needed</span>
                </div>
                <div className="d-flex align-items-center gap-2">
                  <Languages size={16} className="text-warning" />
                  <span>Multilingual (EN / HI / MR)</span>
                </div>
                <div className="d-flex align-items-center gap-2">
                  <HeartHandshake size={16} className="text-warning" />
                  <span>Automated Scheme Matching</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container my-5 py-3">
        <div className="text-center mb-5">
          <span className="text-uppercase text-danger fw-bold small tracking-wider">Simple 4-Step Process</span>
          <h2 className="fw-bold mt-1">{t('howItWorks')}</h2>
          <p className="text-muted">Designed for senior citizens, farmers, and every common citizen.</p>
        </div>

        <div className="row g-4">
          <div className="col-md-3">
            <div className="vf-card p-4 h-100 text-center border-top border-4 border-primary">
              <div className="p-3 bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex mb-3">
                <Mic size={28} />
              </div>
              <h5 className="fw-bold mb-2">{t('speakTitle')}</h5>
              <p className="text-muted small mb-0">{t('speakDesc')}</p>
            </div>
          </div>

          <div className="col-md-3">
            <div className="vf-card p-4 h-100 text-center border-top border-4 border-danger">
              <div className="p-3 bg-danger bg-opacity-10 text-danger rounded-circle d-inline-flex mb-3">
                <Sparkles size={28} />
              </div>
              <h5 className="fw-bold mb-2">{t('whisperTitle')}</h5>
              <p className="text-muted small mb-0">{t('whisperDesc')}</p>
            </div>
          </div>

          <div className="col-md-3">
            <div className="vf-card p-4 h-100 text-center border-top border-4 border-warning">
              <div className="p-3 bg-warning bg-opacity-10 text-warning rounded-circle d-inline-flex mb-3">
                <FileText size={28} />
              </div>
              <h5 className="fw-bold mb-2">{t('nlpTitle')}</h5>
              <p className="text-muted small mb-0">{t('nlpDesc')}</p>
            </div>
          </div>

          <div className="col-md-3">
            <div className="vf-card p-4 h-100 text-center border-top border-4 border-success">
              <div className="p-3 bg-success bg-opacity-10 text-success rounded-circle d-inline-flex mb-3">
                <CheckCircle2 size={28} />
              </div>
              <h5 className="fw-bold mb-2">{t('autofillTitle')}</h5>
              <p className="text-muted small mb-0">{t('autofillDesc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Services & Schemes Quick Access */}
      <section className="container my-5">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4">
          <div>
            <h3 className="fw-bold mb-1">Popular Citizen Forms & Welfare Schemes</h3>
            <p className="text-muted mb-0">Select any service to fill with voice or verify your eligibility</p>
          </div>
          <button 
            className="btn btn-outline-primary btn-sm rounded-pill mt-2 mt-md-0"
            onClick={() => onNavigate('schemes')}
          >
            Explore All Schemes →
          </button>
        </div>

        <div className="row g-4">
          <div className="col-md-4">
            <div className="vf-card p-4 h-100 d-flex flex-column justify-content-between scheme-card eligible">
              <div>
                <span className="badge bg-success-subtle text-success border border-success-subtle mb-2">
                  Direct Benefit Transfer
                </span>
                <h5 className="fw-bold mb-2">PM Kisan Samman Nidhi</h5>
                <p className="text-muted small">
                  ₹6,000 per year directly into farmer bank accounts in 3 installments of ₹2,000.
                </p>
                <div className="text-secondary small mb-3">
                  <strong>Eligibility:</strong> Landholding farmer families with cultivable land.
                </div>
              </div>
              <button 
                className="btn btn-sm btn-gov-primary w-100 mt-2"
                onClick={() => onNavigate('form', 'pm_kisan')}
              >
                <Mic size={16} /> Fill with Voice
              </button>
            </div>
          </div>

          <div className="col-md-4">
            <div className="vf-card p-4 h-100 d-flex flex-column justify-content-between scheme-card">
              <div>
                <span className="badge bg-primary-subtle text-primary border border-primary-subtle mb-2">
                  Universal Health
                </span>
                <h5 className="fw-bold mb-2">Ayushman Bharat (PM-JAY)</h5>
                <p className="text-muted small">
                  Free cashless medical hospitalization up to ₹5,00,000 per family per year.
                </p>
                <div className="text-secondary small mb-3">
                  <strong>Eligibility:</strong> Low income & BPL families as per SECC database.
                </div>
              </div>
              <button 
                className="btn btn-sm btn-gov-primary w-100 mt-2"
                onClick={() => onNavigate('form', 'ayushman_bharat')}
              >
                <Mic size={16} /> Fill with Voice
              </button>
            </div>
          </div>

          <div className="col-md-4">
            <div className="vf-card p-4 h-100 d-flex flex-column justify-content-between scheme-card">
              <div>
                <span className="badge bg-warning-subtle text-dark border border-warning-subtle mb-2">
                  Revenue Certificate
                </span>
                <h5 className="fw-bold mb-2">Income Certificate</h5>
                <p className="text-muted small">
                  Official certificate of family annual income issued by Tahsildar for scholarships and concessions.
                </p>
                <div className="text-secondary small mb-3">
                  <strong>Eligibility:</strong> All residents needing proof of annual family income.
                </div>
              </div>
              <button 
                className="btn btn-sm btn-gov-primary w-100 mt-2"
                onClick={() => onNavigate('form', 'income_certificate')}
              >
                <Mic size={16} /> Fill with Voice
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Official AI Disclaimer Alert */}
      <section className="container my-4">
        <div className="gov-disclaimer-box d-flex align-items-center gap-3">
          <HelpCircle size={28} className="text-warning flex-shrink-0" />
          <div>
            <strong>Notice to Citizens:</strong> {t('disclaimerText')}
          </div>
        </div>
      </section>
    </div>
  );
};
