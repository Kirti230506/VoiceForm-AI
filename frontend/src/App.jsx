import React, { useState } from 'react';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { LanguageProvider } from './context/LanguageContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { SmartAssistantModal } from './components/SmartAssistantModal';
import { Home } from './pages/Home';
import { VoiceForm } from './pages/VoiceForm';
import { SchemeEligibility } from './pages/SchemeEligibility';
import { ReviewSubmit } from './pages/ReviewSubmit';
import { Result } from './pages/Result';
import { DatasetManagement } from './pages/DatasetManagement';


export function AppContent() {
  const [currentPage, setCurrentPage] = useState('home');
  const [activeFormId, setActiveFormId] = useState('income_certificate');
  const [reviewData, setReviewData] = useState(null);
  const [resultData, setResultData] = useState(null);
  const [fieldToExplain, setFieldToExplain] = useState(null);

  // Navigation handlers
  const handleNavigate = (page, formId = null) => {
    if (formId) setActiveFormId(formId);
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleProceedToReview = (data) => {
    setReviewData(data);
    setCurrentPage('review');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmitSuccess = (result) => {
    setResultData(result);
    setCurrentPage('result');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSelectSchemeForm = (formId) => {
    setActiveFormId(formId);
    setCurrentPage('form');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar
        activePage={currentPage}
        setActivePage={(page) => handleNavigate(page)}
      />

      <main className="flex-grow-1">
        {currentPage === 'home' && (
          <Home onNavigate={handleNavigate} />
        )}

        {currentPage === 'form' && (
          <VoiceForm
            initialFormId={activeFormId}
            onProceedToReview={handleProceedToReview}
            onExplainField={(fid) => setFieldToExplain(fid)}
          />
        )}

        {currentPage === 'schemes' && (
          <SchemeEligibility
            onSelectSchemeForm={handleSelectSchemeForm}
          />
        )}

        {currentPage === 'review' && (
          <ReviewSubmit
            reviewData={reviewData}
            onBackToEdit={() => setCurrentPage('form')}
            onSubmitSuccess={handleSubmitSuccess}
          />
        )}

        {currentPage === 'result' && (
          <Result
            resultData={resultData}
            onNavigateHome={() => handleNavigate('home')}
            onCheckSchemes={() => handleNavigate('schemes')}
          />
        )}

        {currentPage === 'dataset' && (
          <DatasetManagement />
        )}
      </main>


      {/* Floating Smart Assistant Modal */}
      <SmartAssistantModal
        activeFieldToExplain={fieldToExplain}
        onCloseFieldExplain={() => setFieldToExplain(null)}
      />

      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  );
}
