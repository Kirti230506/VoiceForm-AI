import React, { useEffect } from 'react';
import confetti from 'canvas-confetti';
import { useLanguage } from '../context/LanguageContext';
import { getPdfDownloadUrl } from '../services/api';
import { 
  CheckCircle, 
  Download, 
  FileText, 
  ArrowRight, 
  Printer, 
  Clock, 
  ShieldCheck, 
  Home,
  MessageSquare
} from 'lucide-react';

export const Result = ({ resultData, onNavigateHome, onCheckSchemes }) => {
  const { lang, t } = useLanguage();

  useEffect(() => {
    // Trigger celebratory confetti on success mount
    try {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
    } catch (e) {
      // safe fallback if confetti blocked
    }
  }, []);

  if (!resultData) {
    return (
      <div className="container py-5 text-center">
        <h4>No submission details available.</h4>
        <button className="btn btn-primary mt-3" onClick={onNavigateHome}>
          Go to Home
        </button>
      </div>
    );
  }

  const {
    application_id,
    form_name,
    applicant_name,
    submitted_at,
    status,
    next_steps
  } = resultData;

  const pdfUrl = getPdfDownloadUrl(application_id);

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="vf-card p-5 text-center shadow-lg border-top border-4 border-success">
            {/* Success Icon */}
            <div className="p-3 bg-success bg-opacity-10 text-success rounded-circle d-inline-flex mb-3">
              <CheckCircle size={56} className="text-success" />
            </div>

            <h2 className="fw-bold mb-2 text-dark">{t('submissionSuccess')}</h2>
            <p className="text-muted mb-4">
              Your application has been digitally registered and assigned an official tracking reference.
            </p>

            {/* Application Reference ID Box */}
            <div className="p-4 bg-light rounded-4 border mb-4">
              <span className="small text-secondary text-uppercase fw-bold d-block mb-1">
                {t('referenceNumber')}
              </span>
              <div className="display-6 fw-bold text-primary font-monospace tracking-wide">
                {application_id}
              </div>
              <div className="mt-2 text-muted small">
                Status: <span className="badge bg-success px-3 py-1">{status || "SUBMITTED"}</span>
              </div>
            </div>

            {/* Submission Metadata */}
            <div className="table-responsive mb-4 text-start">
              <table className="table table-bordered mb-0 small">
                <tbody>
                  <tr>
                    <td className="bg-light fw-bold" style={{ width: '40%' }}>Form Applied:</td>
                    <td>{form_name}</td>
                  </tr>
                  {applicant_name && (
                    <tr>
                      <td className="bg-light fw-bold">Applicant Name:</td>
                      <td>{applicant_name}</td>
                    </tr>
                  )}
                  <tr>
                    <td className="bg-light fw-bold">Submitted At:</td>
                    <td>{submitted_at ? new Date(submitted_at).toLocaleString() : 'Just Now'}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Primary Action: Download PDF Receipt */}
            <div className="mb-4">
              <a
                href={pdfUrl}
                download
                className="btn btn-gov-primary btn-lg px-4 py-3 shadow d-inline-flex align-items-center gap-2"
              >
                <Download size={20} />
                <span>{t('downloadPdf')}</span>
              </a>
              <div className="text-muted small mt-2">
                Official computer-generated e-Receipt for status verification & physical records.
              </div>
            </div>

            {/* Next Steps Box */}
            <div className="p-4 bg-light rounded-4 border text-start mb-4">
              <h6 className="fw-bold text-dark mb-3 d-flex align-items-center gap-2">
                <Clock size={18} className="text-primary" />
                Recommended Next Steps & Timeline
              </h6>
              <ul className="mb-0 small text-muted d-flex flex-column gap-2">
                {next_steps ? (
                  next_steps.map((step, idx) => (
                    <li key={idx} className="d-flex align-items-start gap-2">
                      <span className="badge bg-primary rounded-circle" style={{ width: 20, height: 20, padding: 3 }}>
                        {idx + 1}
                      </span>
                      <span>{step}</span>
                    </li>
                  ))
                ) : (
                  <>
                    <li>Your application will be verified by the designated Tahsildar / Officer.</li>
                    <li>You will receive SMS alerts on your registered phone number.</li>
                    <li>Download and retain your PDF receipt for document verification.</li>
                  </>
                )}
              </ul>
            </div>

            {/* Bottom Navigation */}
            <div className="d-flex flex-wrap gap-2 justify-content-center pt-3 border-top">
              <button
                type="button"
                className="btn btn-outline-primary"
                onClick={onCheckSchemes}
              >
                <ShieldCheck size={16} className="me-1 inline" /> Check Other Schemes
              </button>

              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={onNavigateHome}
              >
                <Home size={16} className="me-1 inline" /> Return to Home
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
