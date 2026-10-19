import React, { useState, useEffect } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { VoiceRecorder } from '../components/VoiceRecorder';
import { getForms, getFormById, extractFromText, validateFormData, downloadDraftPdf } from '../services/api';
import { 
  FileText, 
  Sparkles, 
  CheckCircle, 
  AlertCircle, 
  HelpCircle, 
  ArrowRight, 
  Lightbulb, 
  RefreshCw,
  Edit3,
  Download
} from 'lucide-react';


export const VoiceForm = ({ initialFormId, onProceedToReview, onExplainField }) => {
  const { lang, t } = useLanguage();
  
  const [formList, setFormList] = useState([]);
  const [selectedFormId, setSelectedFormId] = useState(initialFormId || 'income_certificate');
  const [activeFormDef, setActiveFormDef] = useState(null);
  
  const [formData, setFormData] = useState({});
  const [transcribedText, setTranscribedText] = useState('');
  const [extractedEntities, setExtractedEntities] = useState({});
  const [mappedFieldsInfo, setMappedFieldsInfo] = useState({});
  
  const [activeSectionTab, setActiveSectionTab] = useState(0);
  const [validationResult, setValidationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [applyAnimation, setApplyAnimation] = useState(false);

  // Fetch all forms on load
  useEffect(() => {
    loadForms();
  }, []);

  // Fetch active form definition when selectedFormId changes
  useEffect(() => {
    if (selectedFormId) {
      loadFormDefinition(selectedFormId);
    }
  }, [selectedFormId]);

  const loadForms = async () => {
    try {
      const forms = await getForms();
      setFormList(forms);
    } catch (e) {
      console.error("Failed to load forms list:", e);
    }
  };

  const loadFormDefinition = async (id) => {
    setLoading(true);
    try {
      const def = await getFormById(id);
      setActiveFormDef(def);
      // Reset form data if different form
      setFormData({});
      setValidationResult(null);
    } catch (e) {
      console.error("Failed to load form definition:", e);
    } finally {
      setLoading(false);
    }
  };

  // Callback when voice is transcribed & extracted
  const handleExtractionComplete = (result) => {
    if (result.transcribed_text) {
      setTranscribedText(result.transcribed_text);
    }
    if (result.extracted_entities) {
      setExtractedEntities(result.extracted_entities);
    }
    if (result.mapped_form_data) {
      setFormData((prev) => ({
        ...prev,
        ...result.mapped_form_data
      }));
    }
    if (result.mapped_fields) {
      setMappedFieldsInfo(result.mapped_fields);
    }

    // Trigger visual feedback animation
    setApplyAnimation(true);
    setTimeout(() => setApplyAnimation(false), 2000);
  };

  // Re-extract from edited transcript text
  const handleManualReExtract = async () => {
    if (!transcribedText.trim()) return;
    setLoading(true);
    try {
      const res = await extractFromText(transcribedText, selectedFormId, formData);
      handleExtractionComplete(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Handle manual input change on any field
  const handleFieldChange = (fieldId, value) => {
    setFormData((prev) => ({
      ...prev,
      [fieldId]: value
    }));
  };

  // Download draft PDF preview
  const [downloadingDraft, setDownloadingDraft] = useState(false);
  const handleDownloadDraft = async () => {
    setDownloadingDraft(true);
    try {
      const blob = await downloadDraftPdf(selectedFormId, formData);
      const url = window.URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `VoiceForm_Draft_${selectedFormId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (e) {
      console.error("Draft PDF download failed:", e);
      alert("Failed to generate draft PDF preview.");
    } finally {
      setDownloadingDraft(false);
    }
  };

  // Run validation
  const handleValidateAndProceed = async () => {
    if (!activeFormDef) return;
    try {
      const valRes = await validateFormData(selectedFormId, formData);
      setValidationResult(valRes);
      
      // Proceed to review
      if (onProceedToReview) {
        onProceedToReview({
          formId: selectedFormId,
          formDef: activeFormDef,
          formData: formData,
          extractedEntities: extractedEntities,
          rawTranscript: transcribedText,
          validation: valRes
        });
      }
    } catch (e) {
      console.error("Validation error:", e);
    }
  };


  return (
    <div className="container py-4">
      {/* Header and Form Selector */}
      <div className="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h2 className="fw-bold mb-1 d-flex align-items-center gap-2">
            <FileText className="text-primary" size={28} />
            {t('navVoiceForm')}
          </h2>
          <p className="text-muted mb-0">
            Select an official citizen service form and speak your particulars.
          </p>
        </div>

        {/* Form Selector Dropdown */}
        <div className="d-flex align-items-center gap-2">
          <label htmlFor="formSelect" className="small fw-semibold text-secondary text-nowrap">
            Select Form:
          </label>
          <select
            id="formSelect"
            className="form-select form-select-lg fw-medium shadow-sm border-primary"
            value={selectedFormId}
            onChange={(e) => setSelectedFormId(e.target.value)}
          >
            {formList.map((f) => (
              <option key={f.id} value={f.id}>
                {lang === 'hi' ? f.title_hi || f.title : lang === 'mr' ? f.title_mr || f.title : f.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Form Details Card */}
      {activeFormDef && (
        <div className="vf-card p-3 mb-4 bg-light border-0 shadow-sm">
          <div className="d-flex flex-wrap align-items-center justify-content-between gap-2">
            <div>
              <span className="badge bg-primary me-2">{activeFormDef.category}</span>
              <strong className="text-dark fs-5">{activeFormDef.title}</strong>
              <div className="text-muted small mt-1">{activeFormDef.description}</div>
            </div>
            <div className="text-end text-muted small">
              <div>Dept: <strong>{activeFormDef.department}</strong></div>
              <div>Timeline: <span className="text-success fw-bold">{activeFormDef.processing_days}</span></div>
            </div>
          </div>
        </div>
      )}

      {/* Grid: Left Column (Voice Interaction Center) & Right Column (Live Form) */}
      <div className="row g-4">
        {/* Left: Voice Control & AI Extraction */}
        <div className="col-lg-5">
          <VoiceRecorder
            activeFormId={selectedFormId}
            onExtractionComplete={handleExtractionComplete}
            onTranscriptReady={(text) => setTranscribedText(text)}
          />

          {/* Recognized Raw Text Box & Extractor */}
          <div className="vf-card p-3 mt-3">
            <div className="d-flex align-items-center justify-content-between mb-2">
              <label htmlFor="transcriptBox" className="fw-bold small text-secondary d-flex align-items-center gap-1 mb-0">
                <Edit3 size={15} />
                {t('rawTranscript')}
              </label>
              {transcribedText && (
                <span className="badge bg-light text-dark border small">
                  {transcribedText.split(/\s+/).filter(Boolean).length} words
                </span>
              )}
            </div>

            <textarea
              id="transcriptBox"
              className="form-control small mb-2"
              rows="3"
              placeholder="Your spoken words will appear here. You can edit any transcription typos before extracting form fields."
              value={transcribedText}
              onChange={(e) => setTranscribedText(e.target.value)}
            ></textarea>

            <button
              type="button"
              className="btn btn-primary btn-sm w-100 d-flex align-items-center justify-content-center gap-1 shadow-sm py-2"
              onClick={handleManualReExtract}
              disabled={loading || !transcribedText.trim()}
              title="Parse and extract form fields from the transcript above"
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-1" role="status"></span>
                  Extracting Form Information...
                </>
              ) : (
                <>
                  <Sparkles size={16} />
                  <strong>Extract Information into Form Fields</strong>
                </>
              )}
            </button>
          </div>

          {/* Extracted Entities Tag Cloud */}
          {Object.keys(extractedEntities).length > 0 && (
            <div className="vf-card p-3 mt-3">
              <div className="fw-bold small text-secondary mb-2 d-flex align-items-center gap-1">
                <Sparkles size={16} className="text-warning" />
                {t('extractedEntities')} ({Object.keys(extractedEntities).length})
              </div>
              <div className="d-flex flex-wrap">
                {Object.entries(extractedEntities).map(([key, data]) => (
                  <div key={key} className="entity-chip shadow-sm">
                    <span className="text-secondary small">{key}:</span>
                    <strong className="text-dark">{data.formatted || String(data.value)}</strong>
                    <span className="entity-chip-confidence">
                      {Math.round(data.confidence * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right: Live Interactive Form */}
        <div className="col-lg-7">
          <div className={`vf-card p-4 h-100 ${applyAnimation ? 'border-success shadow-lg' : ''}`}>
            <div className="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3 border-bottom pb-3">
              <div>
                <h4 className="fw-bold mb-0">Application Form Fields</h4>
                <small className="text-muted">
                  Information auto-filled from speech is marked with a green check. You can edit any field.
                </small>
              </div>

              <div className="d-flex align-items-center gap-2">
                <button
                  type="button"
                  className="btn btn-outline-secondary btn-sm d-flex align-items-center gap-1 shadow-sm"
                  onClick={handleDownloadDraft}
                  disabled={downloadingDraft}
                  title="Export a draft preview PDF before final submission"
                >
                  <Download size={15} />
                  <span>{downloadingDraft ? "Generating..." : "Download Draft PDF"}</span>
                </button>

                {Object.keys(mappedFieldsInfo).length > 0 && (
                  <span className="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 rounded-pill">
                    ✓ {Object.keys(mappedFieldsInfo).length} Fields Auto-Filled
                  </span>
                )}
              </div>
            </div>

            {/* Section Tabs */}
            {activeFormDef && activeFormDef.sections && (
              <>
                <ul className="nav nav-pills mb-4 nav-fill bg-light p-1 rounded-3">
                  {activeFormDef.sections.map((section, idx) => (
                    <li className="nav-item" key={section.section_id}>
                      <button
                        type="button"
                        className={`nav-link rounded-3 fw-semibold small ${activeSectionTab === idx ? 'active' : ''}`}
                        onClick={() => setActiveSectionTab(idx)}
                      >
                        <span className={`form-step-badge ${activeSectionTab === idx ? 'active' : ''}`}>
                          {idx + 1}
                        </span>
                        {lang === 'hi' ? section.title_hi || section.title : lang === 'mr' ? section.title_mr || section.title : section.title}
                      </button>
                    </li>
                  ))}
                </ul>

                {/* Section Content Fields */}
                {activeFormDef.sections[activeSectionTab] && (
                  <div className="mb-4">
                    <h5 className="fw-bold text-primary mb-3">
                      {activeFormDef.sections[activeSectionTab].title}
                    </h5>

                    <div className="row g-3">
                      {activeFormDef.sections[activeSectionTab].fields.map((field) => {
                        const isAutoFilled = mappedFieldsInfo[field.id];
                        const val = formData[field.id] !== undefined ? formData[field.id] : '';

                        return (
                          <div
                            key={field.id}
                            className={field.type === 'textarea' ? 'col-12' : 'col-md-6'}
                          >
                            <div className="d-flex align-items-center justify-content-between mb-1">
                              <label htmlFor={`field-${field.id}`} className="form-label small fw-semibold mb-0">
                                {lang === 'hi' ? field.label_hi || field.label : lang === 'mr' ? field.label_mr || field.label : field.label}
                                {field.required && <span className="text-danger ms-1">*</span>}
                              </label>

                              {/* Ask AI explainer lightbulb */}
                              <button
                                type="button"
                                className="btn btn-link btn-sm text-decoration-none p-0 text-primary small d-flex align-items-center gap-1"
                                onClick={() => onExplainField(field.id)}
                                title="Explain this field in simple language"
                              >
                                <Lightbulb size={14} className="text-warning" />
                                <span style={{ fontSize: '0.75rem' }}>Ask AI</span>
                              </button>
                            </div>

                            {/* Input Element */}
                            <div className="input-group">
                              {field.type === 'select' ? (
                                <select
                                  id={`field-${field.id}`}
                                  className={`form-select ${isAutoFilled ? 'border-success bg-success-subtle bg-opacity-10' : ''}`}
                                  value={val}
                                  onChange={(e) => handleFieldChange(field.id, e.target.value)}
                                  required={field.required}
                                >
                                  <option value="">-- Select --</option>
                                  {field.options?.map((opt) => (
                                    <option key={opt} value={opt}>
                                      {opt}
                                    </option>
                                  ))}
                                </select>
                              ) : field.type === 'textarea' ? (
                                <textarea
                                  id={`field-${field.id}`}
                                  className={`form-control ${isAutoFilled ? 'border-success bg-success-subtle bg-opacity-10' : ''}`}
                                  rows="2"
                                  placeholder={field.placeholder}
                                  value={val}
                                  onChange={(e) => handleFieldChange(field.id, e.target.value)}
                                  required={field.required}
                                ></textarea>
                              ) : (
                                <input
                                  id={`field-${field.id}`}
                                  type={field.type || 'text'}
                                  className={`form-control ${isAutoFilled ? 'border-success bg-success-subtle bg-opacity-10' : ''}`}
                                  placeholder={field.placeholder}
                                  value={val}
                                  onChange={(e) => handleFieldChange(field.id, e.target.value)}
                                  required={field.required}
                                />
                              )}

                              {isAutoFilled && (
                                <span className="input-group-text bg-success text-white px-2" title="Auto-filled from voice">
                                  <CheckCircle size={16} />
                                </span>
                              )}
                            </div>

                            {field.help && (
                              <div className="form-text text-muted" style={{ fontSize: '0.74rem' }}>
                                {field.help}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Section Navigation & Submission Action */}
                <div className="d-flex justify-content-between align-items-center pt-3 border-top mt-4">
                  {activeSectionTab > 0 ? (
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={() => setActiveSectionTab((prev) => prev - 1)}
                    >
                      ← Back
                    </button>
                  ) : <div></div>}

                  {activeSectionTab < activeFormDef.sections.length - 1 ? (
                    <button
                      type="button"
                      className="btn btn-primary px-4"
                      onClick={() => setActiveSectionTab((prev) => prev + 1)}
                    >
                      Next Section →
                    </button>
                  ) : (
                    <button
                      type="button"
                      className="btn btn-gov-primary px-4 shadow"
                      onClick={handleValidateAndProceed}
                    >
                      <span>{t('saveAndProceed')}</span>
                      <ArrowRight size={18} className="ms-1" />
                    </button>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
