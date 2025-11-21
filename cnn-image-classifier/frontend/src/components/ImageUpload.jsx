import React, { useState, useRef } from 'react';
import { Upload, X, Loader2 } from 'lucide-react';

const ImageUpload = ({ onPredict, loading }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      alert('Iltimos, rasm faylini tanlang!');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handlePredict = () => {
    if (selectedFile) {
      onPredict(selectedFile);
    }
  };

  return (
    <div className="image-upload-container">
      <div
        className={`upload-area ${dragActive ? 'drag-active' : ''} ${previewUrl ? 'has-image' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !previewUrl && fileInputRef.current?.click()}
      >
        {!previewUrl ? (
          <div className="upload-prompt">
            <Upload size={48} className="upload-icon" />
            <p className="upload-text">
              Rasmni bu yerga sudrab keling yoki
            </p>
            <button className="upload-button" type="button">
              Fayl tanlash
            </button>
            <p className="upload-hint">PNG, JPG, JPEG (max. 10MB)</p>
          </div>
        ) : (
          <div className="preview-container">
            <img src={previewUrl} alt="Preview" className="preview-image" />
            <button
              className="remove-button"
              onClick={(e) => {
                e.stopPropagation();
                handleRemove();
              }}
            >
              <X size={20} />
            </button>
          </div>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
      </div>

      {selectedFile && (
        <div className="file-info">
          <p><strong>Fayl nomi:</strong> {selectedFile.name}</p>
          <p><strong>O'lchami:</strong> {(selectedFile.size / 1024).toFixed(2)} KB</p>
        </div>
      )}

      <button
        className="predict-button"
        onClick={handlePredict}
        disabled={!selectedFile || loading}
      >
        {loading ? (
          <>
            <Loader2 size={20} className="spinner" />
            Qayta ishlanmoqda...
          </>
        ) : (
          <>
            <Upload size={20} />
            Klassifikatsiya qilish
          </>
        )}
      </button>
    </div>
  );
};

export default ImageUpload;
