import React, { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';
import { submitApplication, downloadDraftPdf } from '../services/api';
import { 
  FileCheck, 
  AlertTriangle, 
  Edit3, 
  CheckCircle, 
  ArrowLeft, 
  Send, 
  ShieldAlert, 
  HelpCircle,
  Download
} from 'lucide-react';


export const ReviewSubmit = ({ reviewData, onBackToEdit, onSubmitSuccess }) => {
  const { lang, t } = useLanguage();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [declarationChecked, setDeclarationChecked] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [downloadingDraft, setDownloadingDraft] = useState(false);

  const handleDownloadDraft = async () => {
    if (!reviewData?.formId) return;
    setDownloadingDraft(true);
    try {
      const blob = await downloadDraftPdf(reviewData.formId, reviewData.formData);
      const url = window.URL.createObjectURL(new Blob([blob], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `VoiceForm_Draft_${reviewData.formId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (e) {
      console.error("Draft PDF download failed:", e);
      alert("Failed to download draft PDF.");
    } finally {
      setDownloadingDraft(false);
    }
  };


  if (!reviewData || !reviewData.formDef) {
    return (
      <div className="container py-5 text-center">
        <h4>No application data available for review.</h4>
        <button className="btn btn-primary mt-3" onClick={onBackToEdit}>
          Return to Voice Form
        </button>
      </div>
    );
  }

  const { formId, formDef, formData, extractedEntities, rawTranscript, validation } = reviewData;
  const missingFields = validation?.missing_fields || [];
  const formatWarnings = validation?.format_warnings || [];

  const handleSubmit = async () => {
    if (!declarationChecked) {
      alert("Please confirm the applicant declaration checkbox before submitting.");
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const payload = {
        form_id: formId,
        form_data: formData,
        extracted_entities: extractedEntities,
        raw_transcript: rawTranscript,
        language: lang
      };

      const result = await submitApplication(payload);
      if (onSubmitSuccess) {
        onSubmitSuccess(result);
      }
    } catch (err) {
      console.error("Submission failed:", err);
      setSubmitError(err.response?.data?.detail || "Failed to submit application. Please check backend connection.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container py-4">
      {/* Header */}
      <div className="d-flex align-items-center justify-content-between mb-4">
        <div>
          <button
            type="button"
            className="btn btn-link text-decoration-none p-0 text-secondary small d-flex align-items-center gap-1 mb-2"
            onClick={onBackToEdit}
          >
            <ArrowLeft size={16} /> Back to Voice Form
          </button>
          <h2 className="fw-bold mb-0 d-flex align-items-center gap-2">
            <FileCheck className="text-primary" size={28} />
            Review & Finalize Application
          </h2>
          <p className="text-muted mb-0">
            Form: <strong>{formDef.title}</strong>
          </p>
        </div>

        <div className="d-flex align-items-center gap-2">
          <button
            type="button"
            className="btn btn-outline-secondary rounded-pill px-3 py-2 d-flex align-items-center gap-1 shadow-sm"
            onClick={handleDownloadDraft}
            disabled={downloadingDraft}
            title="Download draft application PDF receipt before final submission"
          >
            <Download size={16} />
            <span>{downloadingDraft ? "Generating..." : "Download Draft PDF"}</span>
          </button>

          <button
            type="button"
            className="btn btn-outline-primary rounded-pill px-3 py-2 d-flex align-items-center gap-1"
            onClick={onBackToEdit}
          >
            <Edit3 size={16} />
            <span>Edit Form Fields</span>
          </button>
        </div>
      </div>

      {submitError && (
        <div className="alert alert-danger mb-4 shadow-sm" role="alert">
          <strong>Submission Error:</strong> {submitError}
        </div>
      )}

      {/* Missing Fields Warning Banner */}
      {missingFields.length > 0 && (
        <div className="alert alert-warning border-warning border-2 rounded-3 mb-4 shadow-sm">
          <div className="d-flex align-items-start gap-2">
            <AlertTriangle size={24} className="text-warning flex-shrink-0 mt-1" />
            <div>
              <h6 className="fw-bold mb-1">Attention: {missingFields.length} Mandatory Fields Are Missing</h6>
              <p className="small mb-2">
                Please complete the following required fields before official submission:
              </p>
              <div className="d-flex flex-wrap gap-2">
                {missingFields.map((f, idx) => (
                  <span key={idx} className="badge bg-warning text-dark border">
                    ⚠️ {f.field_label} ({f.section_title})
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Format Warnings */}
      {formatWarnings.length > 0 && (
        <div className="alert alert-info border-info border-2 rounded-3 mb-4 shadow-sm">
          <h6 className="fw-bold mb-2">Format Advisory:</h6>
          <ul className="mb-0 small">
            {formatWarnings.map((w, idx) => (
              <li key={idx}><strong>{w.field_label}:</strong> {w.message}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Information Summary Cards */}
      <div className="row g-4 mb-4">
        {formDef.sections?.map((section) => (
          <div key={section.section_id} className="col-lg-6">
            <div className="vf-card p-4 h-100">
              <div className="d-flex align-items-center justify-content-between mb-3 border-bottom pb-2">
                <h5 className="fw-bold text-primary mb-0">{section.title}</h5>
                <button
                  type="button"
                  className="btn btn-link btn-sm text-decoration-none p-0 text-primary small"
                  onClick={onBackToEdit}
                >
                  <Edit3 size={14} className="me-1 inline" /> Edit
                </button>
              </div>

              <div className="table-responsive">
                <table className="table table-sm table-borderless mb-0">
                  <tbody>
                    {section.fields.map((field) => {
                      const val = formData[field.id];
                      const hasVal = val !== undefined && val !== null && String(val).trim() !== '';

                      return (
                        <tr key={field.id} className="border-bottom">
                          <td className="text-muted small fw-medium py-2" style={{ width: '45%' }}>
                            {field.label}:
                          </td>
                          <td className="py-2">
                            {hasVal ? (
                              <strong className="text-dark small">{String(val)}</strong>
                            ) : (
                              <span className="badge bg-danger-subtle text-danger">Not Provided</span>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Spoken Audio Reference Card */}
      {rawTranscript && (
        <div className="vf-card p-3 mb-4 bg-light">
          <div className="fw-bold small text-secondary mb-1">Original Voice Transcript Recorded:</div>
          <div className="fst-italic text-dark small bg-white p-2 rounded border">
            "{rawTranscript}"
          </div>
        </div>
      )}

      {/* Declaration & Consent Box */}
      <div className="vf-card p-4 mb-4 border-2 border-primary border-opacity-25 bg-white">
        <div className="form-check">
          <input
            className="form-check-input"
            type="checkbox"
            id="applicantDeclaration"
            checked={declarationChecked}
            onChange={(e) => setDeclarationChecked(e.target.checked)}
          />
          <label className="form-check-label small text-dark ms-2" htmlFor="applicantDeclaration">
            <strong>Applicant Self-Declaration:</strong> I solemnly declare and affirm that all the statements and details filled in this application form are true, complete, and correct to the best of my knowledge and belief. I understand that any false declaration will lead to summary rejection and legal action under the relevant Government Acts.
          </label>
        </div>
      </div>

      {/* Submission CTA */}
      <div className="d-flex flex-wrap align-items-center justify-content-between gap-3 pt-2">
        <button
          type="button"
          className="btn btn-outline-secondary px-4 py-2"
          onClick={onBackToEdit}
          disabled={isSubmitting}
        >
          ← Edit Details
        </button>

        <button
          type="button"
          className="btn btn-gov-primary btn-lg px-5 py-3 shadow"
          onClick={handleSubmit}
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status"></span>
              Submitting Application...
            </>
          ) : (
            <>
              <Send size={20} />
              <span>{t('submitForm')}</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
