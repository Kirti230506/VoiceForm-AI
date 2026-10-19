import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, RefreshCw, Volume2, Sparkles, AlertCircle, Trash2, Send, CheckCircle2, VolumeX, ShieldAlert } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { transcribeAudio, extractAndFillVoice, fetchSampleAudio, extractFromText } from '../services/api';

export const VoiceRecorder = ({ activeFormId, onExtractionComplete, onTranscriptReady, compact = false }) => {
  const { lang, t } = useLanguage();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);
  const [warningMsg, setWarningMsg] = useState(null);
  const [permissionDenied, setPermissionDenied] = useState(false);
  const [transcribeSuccess, setTranscribeSuccess] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0); // 0 to 100 live volume level
  const [selectedDemoText, setSelectedDemoText] = useState('');

  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerIntervalRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const animFrameRef = useRef(null);
  const hasSpokenRef = useRef(false);
  const detectedMimeRef = useRef('audio/webm');
  const fileExtRef = useRef('webm');

  // Sample demonstration profiles for instant testing without mic
  const DEMO_SAMPLES = [
    {
      label: "Ramesh (Farmer, Maharashtra, OBC)",
      text: "My name is Ramesh Kumar. I am 42 years old. My mobile number is 9876543210 and Aadhaar is 5432 8765 1290. I am a farmer living in Pune, Maharashtra. My annual income is 1.5 lakh rupees and category is OBC.",
      form: "pm_kisan"
    },
    {
      label: "Priya (Student, SC Scholarship)",
      text: "My name is Priya Sharma. I am 20 years old and a female college student residing in Lucknow, Uttar Pradesh. My father's name is Suresh Sharma. My phone number is 9123456780. Our annual household income is 80000 rupees and category is SC.",
      form: "income_certificate"
    },
    {
      label: "Yashoda (Senior Citizen Pension)",
      text: "My name is Yashodabai Patil. I am 65 years old widow living in Nagpur, Maharashtra. My mobile is 9988776655. My annual income is 35000 rupees. I need old age assistance.",
      form: "senior_pension"
    }
  ];

  // Helper to detect best audio format supported by current browser
  const getSupportedAudioConfig = () => {
    const candidates = [
      { mime: 'audio/webm;codecs=opus', ext: 'webm' },
      { mime: 'audio/webm', ext: 'webm' },
      { mime: 'audio/ogg;codecs=opus', ext: 'ogg' },
      { mime: 'audio/ogg', ext: 'ogg' },
      { mime: 'audio/mp4', ext: 'm4a' },
      { mime: 'audio/wav', ext: 'wav' }
    ];
    for (const c of candidates) {
      if (typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(c.mime)) {
        return c;
      }
    }
    return { mime: '', ext: 'webm' };
  };

  // Start live microphone recording
  const startRecording = async () => {
    setErrorMsg(null);
    setWarningMsg(null);
    setPermissionDenied(false);
    setTranscribeSuccess(false);
    setAudioLevel(0);
    hasSpokenRef.current = false;

    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setErrorMsg("Your browser does not support audio recording. Please use Chrome, Edge, or Firefox, or use the quick demo samples below.");
        return;
      }

      // Request stream with high-quality speech constraints (Windows / laptop friendly)
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
            channelCount: { ideal: 1 },
            sampleRate: { ideal: 16000 }
          }
        });
      } catch (constraintErr) {
        // Fallback to basic audio constraint if strict parameters fail
        console.warn("Retrying with basic audio constraints:", constraintErr);
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      }

      streamRef.current = stream;

      // Detect optimal MIME container
      const config = getSupportedAudioConfig();
      detectedMimeRef.current = config.mime;
      fileExtRef.current = config.ext;

      // Setup live AudioContext volume visualizer
      try {
        const AudioCtxClass = window.AudioContext || window.webkitAudioContext;
        if (AudioCtxClass) {
          const audioCtx = new AudioCtxClass();
          audioContextRef.current = audioCtx;
          const source = audioCtx.createMediaStreamSource(stream);
          const analyser = audioCtx.createAnalyser();
          analyser.fftSize = 256;
          analyser.smoothingTimeConstant = 0.4;
          source.connect(analyser);
          analyserRef.current = analyser;

          const dataArray = new Uint8Array(analyser.frequencyBinCount);
          const checkVolume = () => {
            if (!analyserRef.current) return;
            analyserRef.current.getByteFrequencyData(dataArray);
            let sum = 0;
            for (let i = 0; i < dataArray.length; i++) {
              sum += dataArray[i];
            }
            const avg = sum / dataArray.length;
            if (avg > 8) {
              hasSpokenRef.current = true;
            }
            // Scale to 0-100%
            const level = Math.min(100, Math.round((avg / 90) * 100));
            setAudioLevel(level);
            animFrameRef.current = requestAnimationFrame(checkVolume);
          };
          checkVolume();
        }
      } catch (audioCtxErr) {
        console.warn("AudioContext visualizer not available:", audioCtxErr);
      }

      // Setup MediaRecorder
      audioChunksRef.current = [];
      const recorderOptions = config.mime ? { mimeType: config.mime } : undefined;
      const mediaRecorder = new MediaRecorder(stream, recorderOptions);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const finalMime = detectedMimeRef.current || mediaRecorder.mimeType || 'audio/webm';
        const blob = new Blob(audioChunksRef.current, { type: finalMime });

        if (blob.size < 250) {
          setErrorMsg("Recording was too short or no audio was captured. Please hold the mic closer, speak clearly, and try again.");
          setAudioBlob(null);
          setAudioUrl(null);
        } else {
          setAudioBlob(blob);
          const url = URL.createObjectURL(blob);
          setAudioUrl(url);

          if (!hasSpokenRef.current) {
            setWarningMsg("Low or silent audio detected. If transcription returns empty text, please check that your microphone is unmuted in Windows Sound Settings.");
          }
        }
      };

      // Deliver chunks every 250ms so data is continuously buffered
      mediaRecorder.start(250);
      setIsRecording(true);
      setRecordingTime(0);

      // Start duration counter
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);

    } catch (err) {
      console.warn("Microphone access error:", err);
      setPermissionDenied(true);
      setIsRecording(false);
      setErrorMsg("Microphone access was denied or device not found. Please click the lock icon in your browser address bar to allow microphone access, or use the quick demo samples below.");
    }
  };

  // Stop recording - 100% fail-safe and guaranteed to stop
  const stopRecording = () => {
    try {
      // 1. Immediately stop recording timer
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }

      // 2. Stop audio visualizer loop and close AudioContext
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
        animFrameRef.current = null;
      }
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        try {
          audioContextRef.current.close();
        } catch (e) {
          console.warn("AudioContext close error:", e);
        }
        audioContextRef.current = null;
      }
      setAudioLevel(0);

      // 3. Stop MediaRecorder safely
      const recorder = mediaRecorderRef.current;
      if (recorder) {
        try {
          if (recorder.state === 'recording' || recorder.state === 'paused') {
            // Request any remaining buffered data
            try {
              recorder.requestData();
            } catch (e) {}
            recorder.stop();
          }
        } catch (recErr) {
          console.warn("MediaRecorder stop error:", recErr);
        }
      }

      // 4. Stop all MediaStream audio tracks immediately to shut off the browser red dot
      if (streamRef.current) {
        try {
          streamRef.current.getTracks().forEach((track) => {
            track.stop();
            track.enabled = false;
          });
        } catch (streamErr) {
          console.warn("Stream track stop error:", streamErr);
        }
        streamRef.current = null;
      }

    } catch (outerErr) {
      console.error("Critical error in stopRecording:", outerErr);
    } finally {
      // 5. Unconditionally reset recording state so button and UI always stop!
      setIsRecording(false);
    }
  };

  // Delete recording and clean up
  const deleteRecording = () => {
    if (isRecording) {
      stopRecording();
    }
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl);
    }
    setAudioBlob(null);
    setAudioUrl(null);
    setRecordingTime(0);
    setErrorMsg(null);
    setWarningMsg(null);
    setTranscribeSuccess(false);
    setAudioLevel(0);
  };

  // Record Again (delete current and start fresh)
  const recordAgain = () => {
    deleteRecording();
    setTimeout(() => {
      startRecording();
    }, 200);
  };

  // Step 1: Submit audio for transcription only (enables user editing before extraction)
  const handleTranscribeAudioOnly = async () => {
    if (!audioBlob) return;
    setIsLoading(true);
    setErrorMsg(null);
    setWarningMsg(null);
    setTranscribeSuccess(false);

    const ext = fileExtRef.current || 'webm';
    const uploadFilename = `recording.${ext}`;

    try {
      const data = await transcribeAudio(audioBlob, uploadFilename, lang);
      if (data.text) {
        setTranscribeSuccess(true);
        if (onTranscriptReady) {
          onTranscriptReady(data.text);
        }
        if (onExtractionComplete) {
          onExtractionComplete({
            transcribed_text: data.text,
            detected_language: data.detected_language
          });
        }
      } else {
        setErrorMsg(data.message || "No speech could be recognized. Please hold your microphone closer, speak clearly, and try again.");
      }
    } catch (err) {
      console.error("Transcription failed:", err);
      setErrorMsg(err.response?.data?.detail || "Transcription failed. Please check that your backend server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  // Direct 1-click Transcribe & Extract
  const handleProcessAudio = async () => {
    if (!audioBlob) return;
    setIsLoading(true);
    setErrorMsg(null);
    setWarningMsg(null);
    setTranscribeSuccess(false);

    const ext = fileExtRef.current || 'webm';
    const uploadFilename = `recording.${ext}`;

    try {
      const data = await extractAndFillVoice(audioBlob, activeFormId, uploadFilename, lang);
      setTranscribeSuccess(true);
      if (onExtractionComplete) {
        onExtractionComplete(data);
      }
    } catch (err) {
      console.error("Audio processing failed:", err);
      setErrorMsg(err.response?.data?.detail || "Whisper transcription failed. Please check that backend server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  // Process sample audio file from backend
  const handleUseSampleAudioFile = async () => {
    setIsLoading(true);
    setErrorMsg(null);
    setWarningMsg(null);
    setTranscribeSuccess(false);
    try {
      const blob = await fetchSampleAudio();
      setAudioBlob(blob);
      setAudioUrl(URL.createObjectURL(blob));

      const data = await extractAndFillVoice(blob, activeFormId, 'voiceform_test.wav', lang);
      setTranscribeSuccess(true);
      if (onExtractionComplete) {
        onExtractionComplete(data);
      }
    } catch (err) {
      console.error("Sample audio processing error:", err);
      setErrorMsg("Failed to load sample audio from server.");
    } finally {
      setIsLoading(false);
    }
  };

  // Format seconds to mm:ss
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Component cleanup
  useEffect(() => {
    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
        try {
          audioContextRef.current.close();
        } catch (e) {}
      }
      if (streamRef.current) {
        try {
          streamRef.current.getTracks().forEach((track) => track.stop());
        } catch (e) {}
      }
    };
  }, []);

  return (
    <div className={`vf-card p-4 ${compact ? 'shadow-none border-0' : ''}`}>
      <div className="d-flex align-items-center justify-content-between mb-3">
        <div className="d-flex align-items-center gap-2">
          <span className="p-2 bg-primary bg-opacity-10 text-primary rounded-circle">
            <Mic size={20} />
          </span>
          <h5 className="mb-0 fw-bold">{t('voiceAssistant')}</h5>
        </div>
        <span className="badge bg-secondary-subtle text-dark border">
          OpenAI Whisper Powered
        </span>
      </div>

      <p className="text-muted small mb-3">
        {t('speakDesc')}
      </p>

      {errorMsg && (
        <div className="alert alert-warning py-2 px-3 small d-flex align-items-start gap-2 mb-3" role="alert">
          <AlertCircle size={18} className="text-warning flex-shrink-0 mt-1" />
          <div>{errorMsg}</div>
        </div>
      )}

      {warningMsg && (
        <div className="alert alert-info py-2 px-3 small d-flex align-items-start gap-2 mb-3" role="alert">
          <ShieldAlert size={18} className="text-info flex-shrink-0 mt-1" />
          <div>{warningMsg}</div>
        </div>
      )}

      {/* Main Microphone Interaction Area */}
      <div className="d-flex flex-column align-items-center justify-content-center py-4 bg-light rounded-4 border mb-3">
        {!isRecording ? (
          <button
            type="button"
            className="btn btn-danger rounded-circle p-4 shadow-lg d-flex align-items-center justify-content-center transition-all hover-scale"
            style={{ width: 84, height: 84 }}
            onClick={startRecording}
            disabled={isLoading}
            aria-label="Start Voice Recording"
            title="Click to start recording your voice"
          >
            <Mic size={36} className="text-white" />
          </button>
        ) : (
          <div className="d-flex flex-column align-items-center recording-pulse">
            <button
              type="button"
              className="btn btn-outline-danger bg-danger text-white rounded-circle p-4 shadow-lg d-flex align-items-center justify-content-center"
              style={{ width: 84, height: 84 }}
              onClick={stopRecording}
              aria-label="Stop Voice Recording"
              title="Click to STOP recording"
            >
              <Square size={32} />
            </button>
          </div>
        )}

        <div className="mt-3 text-center w-100 px-3">
          {isRecording ? (
            <div>
              {/* Live Audio Level Meter */}
              <div className="d-flex align-items-center justify-content-center gap-1 my-2" style={{ height: 36 }}>
                {[0.4, 0.7, 1.0, 0.8, 0.5, 0.9, 0.6].map((multiplier, idx) => {
                  const barHeight = Math.max(6, Math.min(36, Math.round((audioLevel * multiplier) * 0.36 + 6)));
                  const isActive = audioLevel > 5;
                  return (
                    <div
                      key={idx}
                      style={{
                        width: 5,
                        height: `${barHeight}px`,
                        backgroundColor: isActive ? '#059669' : '#dc2626',
                        borderRadius: 3,
                        transition: 'height 0.1s ease-out'
                      }}
                    />
                  );
                })}
              </div>

              <div className="d-flex align-items-center justify-content-center gap-2 mb-1">
                <span className="badge bg-danger px-3 py-2 fs-6">
                  Recording... {formatTime(recordingTime)}
                </span>
                <button
                  type="button"
                  className="btn btn-sm btn-dark px-3 py-1 fw-bold"
                  onClick={stopRecording}
                  title="Click to stop recording"
                >
                  ⏹ Stop Now
                </button>
              </div>

              {audioLevel > 5 ? (
                <div className="text-success small fw-medium mt-1">
                  🟢 Microphone receiving voice (Volume: {audioLevel}%)
                </div>
              ) : (
                <div className="text-secondary small mt-1">
                  🟡 Listening... Please speak clearly into your microphone
                </div>
              )}
            </div>
          ) : (
            <span className="text-muted fw-medium">
              {audioBlob ? "Voice recorded! Click 'Submit Audio' or 'Direct Auto-Fill' below." : "Click microphone button to speak your details"}
            </span>
          )}
        </div>

        {/* Audio playback if recorded */}
        {audioUrl && !isRecording && (
          <div className="mt-3 w-75">
            <audio src={audioUrl} controls className="w-100" style={{ height: 38 }} />
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="d-flex flex-wrap gap-2 justify-content-center mb-3">
        {audioBlob && !isRecording && (
          <>
            {/* Submit Audio Button */}
            <button
              type="button"
              className="btn btn-gov-primary shadow-sm"
              onClick={handleTranscribeAudioOnly}
              disabled={isLoading}
              title="Transcribe speech to text with Whisper"
            >
              {isLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Processing Audio...
                </>
              ) : (
                <>
                  <Send size={16} className="me-1" />
                  Submit Audio (Whisper)
                </>
              )}
            </button>

            {/* Direct 1-Click Auto-Fill */}
            <button
              type="button"
              className="btn btn-outline-primary"
              onClick={handleProcessAudio}
              disabled={isLoading}
              title="Transcribe and directly extract form fields"
            >
              <Sparkles size={16} className="me-1" />
              Direct Auto-Fill
            </button>

            {/* Record Again Button */}
            <button
              type="button"
              className="btn btn-outline-secondary"
              onClick={recordAgain}
              disabled={isLoading}
              title="Record voice again"
            >
              <RefreshCw size={15} className="me-1" />
              Record Again
            </button>

            {/* Delete Recording Button */}
            <button
              type="button"
              className="btn btn-outline-danger"
              onClick={deleteRecording}
              disabled={isLoading}
              title="Delete this recording"
            >
              <Trash2 size={15} className="me-1" />
              Delete Recording
            </button>
          </>
        )}
      </div>

      {transcribeSuccess && (
        <div className="alert alert-success py-2 px-3 small d-flex align-items-center gap-2 mb-3" role="status">
          <CheckCircle2 size={16} className="text-success flex-shrink-0" />
          <span>Audio transcribed! You can review or edit the recognized text below, then click <strong>Extract Information</strong>.</span>
        </div>
      )}

      {/* Pre-recorded Sample & Demonstration Tools */}
      <div className="border-top pt-3 mt-3">
        <div className="d-flex align-items-center justify-content-between mb-2">
          <span className="fw-semibold small text-secondary">
            ⚡ Quick Demo Samples (Instant Test Without Mic)
          </span>
          <button
            type="button"
            className="btn btn-link btn-sm text-decoration-none p-0 text-primary small"
            onClick={handleUseSampleAudioFile}
            disabled={isLoading}
          >
            <Volume2 size={14} className="me-1 inline" />
            Test with voiceform_test.wav
          </button>
        </div>

        <div className="d-flex flex-wrap gap-2">
          {DEMO_SAMPLES.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              className="btn btn-outline-secondary btn-sm rounded-pill text-truncate"
              style={{ maxWidth: '100%', fontSize: '0.78rem' }}
              onClick={async () => {
                setSelectedDemoText(sample.text);
                setIsLoading(true);
                try {
                  const res = await extractFromText(sample.text, activeFormId || sample.form);
                  if (onExtractionComplete) {
                    onExtractionComplete({
                      ...res,
                      transcribed_text: sample.text
                    });
                  }
                } catch (e) {
                  setErrorMsg("Sample processing error: " + e.message);
                } finally {
                  setIsLoading(false);
                }
              }}
              disabled={isLoading}
            >
              🎤 {sample.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
