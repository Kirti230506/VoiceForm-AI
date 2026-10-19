import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { checkSchemeEligibility, getSchemes } from '../services/api';
import { VoiceRecorder } from '../components/VoiceRecorder';
import { 
  ShieldCheck, 
  Sparkles, 
  CheckCircle2, 
  XCircle, 
  HelpCircle, 
  FileText, 
  ArrowRight, 
  Filter, 
  Briefcase, 
  DollarSign, 
  User, 
  MapPin,
  Mic
} from 'lucide-react';

export const SchemeEligibility = ({ onSelectSchemeForm }) => {
  const { lang, t } = useLanguage();

  const [profile, setProfile] = useState({
    age: 42,
    gender: 'Male',
    annualIncome: 150000,
    occupation: 'Farmer / Shetkari / Kisan',
    socialCategory: 'OBC (Other Backward Class)',
    state: 'Maharashtra',
    landHolding: '2.5 Acres'
  });

  const [categoryFilter, setCategoryFilter] = useState('All');
  const [eligibilityResult, setEligibilityResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showVoiceRecorder, setShowVoiceRecorder] = useState(false);

  const CATEGORIES = [
    'All',
    'Agriculture',
    'Healthcare',
    'Housing',
    'Education',
    'Women & Child Welfare',
    'Social Welfare & Pensions',
    'Employment & Entrepreneurship'
  ];

  // Evaluate eligibility on mount and when profile changes
  useEffect(() => {
    runEligibilityCheck();
  }, []);

  const runEligibilityCheck = async (customProfile = null) => {
    setLoading(true);
    try {
      const data = await checkSchemeEligibility(customProfile || profile);
      setEligibilityResult(data);
    } catch (e) {
      console.error("Eligibility check error:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    const updated = {
      ...profile,
      [field]: field === 'age' || field === 'annualIncome' ? (value ? Number(value) : '') : value
    };
    setProfile(updated);
  };

  // When speech is transcribed from voice recorder
  const handleVoiceExtraction = (res) => {
    if (res.extracted_entities) {
      const ent = res.extracted_entities;
      const updated = { ...profile };

      if (ent.age?.value) updated.age = Number(ent.age.value);
      if (ent.gender?.value) updated.gender = ent.gender.value;
      if (ent.annualIncome?.value) updated.annualIncome = Number(ent.annualIncome.value);
      if (ent.occupation?.value) updated.occupation = ent.occupation.value;
      if (ent.socialCategory?.value) updated.socialCategory = ent.socialCategory.value;
      if (ent.state?.value) updated.state = ent.state.value;
      if (ent.landHolding?.value) updated.landHolding = ent.landHolding.value;

      setProfile(updated);
      runEligibilityCheck(updated);
      setShowVoiceRecorder(false);
    }
  };

  // Filter schemes
  const displayedSchemes = eligibilityResult?.recommended_schemes?.filter((s) => {
    if (categoryFilter === 'All') return true;
    return s.category.toLowerCase().includes(categoryFilter.toLowerCase());
  }) || [];

  return (
    <div className="container py-4">
      {/* Page Header */}
      <div className="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h2 className="fw-bold mb-1 d-flex align-items-center gap-2">
            <ShieldCheck className="text-primary" size={28} />
            {t('eligibilityCheck')}
          </h2>
          <p className="text-muted mb-0">{t('enterDetails')}</p>
        </div>

        <button
          type="button"
          className="btn btn-outline-danger d-flex align-items-center gap-2 rounded-pill px-3 py-2 shadow-sm"
          onClick={() => setShowVoiceRecorder(!showVoiceRecorder)}
        >
          <Mic size={18} />
          <span>{showVoiceRecorder ? "Hide Voice Input" : "Speak Your Profile"}</span>
        </button>
      </div>

      {/* Optional Voice Input Collapse */}
      {showVoiceRecorder && (
        <div className="mb-4">
          <VoiceRecorder
            onExtractionComplete={handleVoiceExtraction}
          />
        </div>
      )}

      {/* Prominent Official Disclaimer Box */}
      <div className="gov-disclaimer-box mb-4 d-flex align-items-start gap-2 shadow-sm">
        <HelpCircle size={22} className="text-warning flex-shrink-0 mt-1" />
        <div>
          <strong className="d-block mb-1">{t('disclaimerTitle')}:</strong>
          <span>{eligibilityResult?.disclaimer || t('disclaimerText')}</span>
        </div>
      </div>

      {/* Profile Form Bar */}
      <div className="vf-card p-4 mb-4">
        <h5 className="fw-bold mb-3 d-flex align-items-center gap-2">
          <User size={20} className="text-primary" />
          Applicant Socio-Economic Profile
        </h5>

        <div className="row g-3">
          <div className="col-md-2 col-6">
            <label className="form-label small fw-semibold">{t('ageLabel')}</label>
            <input
              type="number"
              className="form-control"
              value={profile.age}
              onChange={(e) => handleInputChange('age', e.target.value)}
              min="1"
              max="120"
            />
          </div>

          <div className="col-md-2 col-6">
            <label className="form-label small fw-semibold">{t('genderLabel')}</label>
            <select
              className="form-select"
              value={profile.gender}
              onChange={(e) => handleInputChange('gender', e.target.value)}
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Transgender">Transgender</option>
            </select>
          </div>

          <div className="col-md-3 col-6">
            <label className="form-label small fw-semibold">{t('incomeLabel')}</label>
            <input
              type="number"
              className="form-control"
              value={profile.annualIncome}
              onChange={(e) => handleInputChange('annualIncome', e.target.value)}
              step="10000"
            />
          </div>

          <div className="col-md-3 col-6">
            <label className="form-label small fw-semibold">{t('occupationLabel')}</label>
            <input
              type="text"
              className="form-control"
              value={profile.occupation}
              onChange={(e) => handleInputChange('occupation', e.target.value)}
              placeholder="Farmer, Student, Worker"
            />
          </div>

          <div className="col-md-2 col-12">
            <label className="form-label small fw-semibold">&nbsp;</label>
            <button
              type="button"
              className="btn btn-gov-primary w-100 py-2 d-flex justify-content-center"
              onClick={() => runEligibilityCheck()}
              disabled={loading}
            >
              {loading ? (
                <span className="spinner-border spinner-border-sm" role="status"></span>
              ) : (
                <>
                  <Sparkles size={16} />
                  <span>Check AI</span>
                </>
              )}
            </button>
          </div>

          <div className="col-md-4 col-6">
            <label className="form-label small fw-semibold">{t('categoryLabel')}</label>
            <select
              className="form-select"
              value={profile.socialCategory}
              onChange={(e) => handleInputChange('socialCategory', e.target.value)}
            >
              <option value="General / Open">General / Open</option>
              <option value="OBC (Other Backward Class)">OBC (Other Backward Class)</option>
              <option value="SC (Scheduled Caste)">SC (Scheduled Caste)</option>
              <option value="ST (Scheduled Tribe)">ST (Scheduled Tribe)</option>
              <option value="EWS">EWS</option>
            </select>
          </div>

          <div className="col-md-4 col-6">
            <label className="form-label small fw-semibold">{t('stateLabel')}</label>
            <input
              type="text"
              className="form-control"
              value={profile.state}
              onChange={(e) => handleInputChange('state', e.target.value)}
            />
          </div>

          <div className="col-md-4 col-12">
            <label className="form-label small fw-semibold">{t('landLabel')}</label>
            <input
              type="text"
              className="form-control"
              value={profile.landHolding}
              onChange={(e) => handleInputChange('landHolding', e.target.value)}
              placeholder="e.g. 2.5 Acres or Landless"
            />
          </div>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="d-flex flex-wrap gap-2 mb-4 align-items-center">
        <span className="small text-muted fw-semibold me-1 d-flex align-items-center gap-1">
          <Filter size={15} /> Sector:
        </span>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            type="button"
            className={`btn btn-sm rounded-pill px-3 ${categoryFilter === cat ? 'btn-primary' : 'btn-outline-secondary'}`}
            onClick={() => setCategoryFilter(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Results Count Banner */}
      <div className="d-flex align-items-center justify-content-between mb-3">
        <h4 className="fw-bold mb-0">
          {t('eligibleSchemesFound')} ({displayedSchemes.length})
        </h4>
        {eligibilityResult && (
          <span className="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 rounded-pill">
            ✓ {eligibilityResult.eligible_schemes_count} Verified Matches
          </span>
        )}
      </div>

      {/* Recommended Schemes Grid */}
      <div className="row g-4">
        {displayedSchemes.map((scheme) => {
          const isHighlyEligible = scheme.eligibility_score >= 80;
          const isLikely = scheme.eligibility_score >= 60 && scheme.eligibility_score < 80;

          return (
            <div key={scheme.scheme_id} className="col-lg-6">
              <div className={`vf-card p-4 h-100 d-flex flex-column justify-content-between scheme-card ${isHighlyEligible ? 'eligible' : ''}`}>
                <div>
                  {/* Top Badges */}
                  <div className="d-flex align-items-center justify-content-between gap-2 mb-2">
                    <span className="badge bg-secondary-subtle text-dark border">
                      {scheme.category}
                    </span>
                    <span className={`scheme-match-badge ${
                      isHighlyEligible
                        ? 'bg-success text-white'
                        : isLikely
                        ? 'bg-warning text-dark'
                        : 'bg-secondary text-white'
                    }`}>
                      {scheme.eligibility_score}% Match • {scheme.status}
                    </span>
                  </div>

                  {/* Title & Ministry */}
                  <h5 className="fw-bold mb-1 text-primary">
                    {lang === 'hi' ? scheme.title_hi || scheme.title : lang === 'mr' ? scheme.title_mr || scheme.title : scheme.title}
                  </h5>
                  <div className="small text-muted mb-3">{scheme.ministry}</div>

                  <p className="text-secondary small mb-3">
                    {lang === 'hi' ? scheme.description_hi || scheme.description : lang === 'mr' ? scheme.description_mr || scheme.description : scheme.description}
                  </p>

                  {/* Why You Are Eligible / Criteria Check */}
                  <div className="mb-3 p-3 bg-light rounded-3">
                    <div className="fw-bold small text-dark mb-2">AI Eligibility Assessment:</div>
                    <ul className="list-unstyled mb-0 small d-flex flex-column gap-1">
                      {scheme.reasons_eligible.map((reason, idx) => (
                        <li key={idx} className="d-flex align-items-start gap-2 text-success">
                          <CheckCircle2 size={16} className="flex-shrink-0 mt-0.5" />
                          <span>{reason}</span>
                        </li>
                      ))}
                      {scheme.criteria_unmet.map((unmet, idx) => (
                        <li key={idx} className="d-flex align-items-start gap-2 text-danger">
                          <XCircle size={16} className="flex-shrink-0 mt-0.5" />
                          <span>{unmet}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Key Benefits */}
                  <div className="mb-3">
                    <div className="fw-bold small text-dark mb-1">{t('benefits')}:</div>
                    <ul className="mb-0 small text-muted ps-3">
                      {scheme.benefits.slice(0, 3).map((b, idx) => (
                        <li key={idx}>{b}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Mandatory Documents */}
                  <div className="mb-3">
                    <div className="fw-bold small text-dark mb-1">{t('documents')}:</div>
                    <div className="d-flex flex-wrap gap-1">
                      {scheme.documents_required.map((doc, idx) => (
                        <span key={idx} className="badge bg-light text-dark border small" style={{ fontSize: '0.72rem' }}>
                          📄 {doc}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Bottom Action: Direct Apply */}
                <div className="pt-3 border-top mt-3">
                  <button
                    type="button"
                    className="btn btn-gov-primary w-100 justify-content-center"
                    onClick={() => {
                      const formTarget = scheme.application_info?.associated_form_id || 'income_certificate';
                      if (onSelectSchemeForm) {
                        onSelectSchemeForm(formTarget);
                      }
                    }}
                  >
                    <FileText size={16} />
                    <span>{t('applyNow')}</span>
                    <ArrowRight size={16} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
