import React, { useState } from 'react';
import { uploadStandardsFile } from '../api';

/**
 * FileUpload Component
 * Handles file upload for coding standards
 */
const FileUpload = ({ onUploadSuccess }) => {
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [message, setMessage] = useState(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            await handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = async (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            await handleFile(e.target.files[0]);
        }
    };

    const handleFile = async (file) => {
        // Validate file type
        const validTypes = ['.md', '.txt'];
        const fileExtension = file.name.substring(file.name.lastIndexOf('.'));

        if (!validTypes.includes(fileExtension)) {
            setMessage({ type: 'error', text: 'Please upload a .md or .txt file' });
            return;
        }

        setUploading(true);
        setMessage(null);

        try {
            const result = await uploadStandardsFile(file);
            setMessage({ type: 'success', text: `Successfully uploaded: ${file.name}` });
            if (onUploadSuccess) {
                onUploadSuccess(result);
            }
        } catch (error) {
            setMessage({
                type: 'error',
                text: error.response?.data?.detail || 'Failed to upload file'
            });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="card">
            <h3 className="text-lg font-semibold text-white mb-4">Upload Coding Standards</h3>

            <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all ${dragActive
                    ? 'border-primary-500 bg-primary-500/10'
                    : 'border-slate-600 hover:border-slate-500'
                    }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    onChange={handleChange}
                    accept=".md,.txt"
                    disabled={uploading}
                />

                <label
                    htmlFor="file-upload"
                    className="cursor-pointer flex flex-col items-center"
                >
                    <svg
                        className="w-12 h-12 text-slate-400 mb-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                        />
                    </svg>

                    <p className="text-slate-300 mb-2">
                        {uploading ? 'Uploading...' : 'Click to upload or drag and drop'}
                    </p>
                    <p className="text-sm text-slate-500">
                        Markdown (.md) or Text (.txt) files
                    </p>
                </label>
            </div>

            {message && (
                <div
                    className={`mt-4 p-4 rounded-lg ${message.type === 'success'
                        ? 'bg-green-500/20 text-green-400 border border-green-500/50'
                        : 'bg-red-500/20 text-red-400 border border-red-500/50'
                        }`}
                >
                    {message.text}
                </div>
            )}
        </div>
    );
};

export default FileUpload;
