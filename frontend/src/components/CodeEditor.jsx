import React, { useState } from 'react';

/**
 * CodeEditor Component
 * Textarea-based code editor with syntax highlighting support
 */
const CodeEditor = ({ value, onChange, placeholder, language = 'python' }) => {
    const [lineCount, setLineCount] = useState(1);

    const handleChange = (e) => {
        const text = e.target.value;
        onChange(text);

        // Update line count
        const lines = text.split('\n').length;
        setLineCount(lines);
    };

    return (
        <div className="relative">
            <div className="absolute left-0 top-0 bottom-0 w-12 bg-slate-900 border-r border-slate-700 rounded-l-lg overflow-hidden">
                <div className="text-slate-500 text-xs font-mono text-right pr-2 pt-3 select-none">
                    {Array.from({ length: lineCount }, (_, i) => (
                        <div key={i + 1} className="leading-6">
                            {i + 1}
                        </div>
                    ))}
                </div>
            </div>
            <textarea
                value={value}
                onChange={handleChange}
                placeholder={placeholder}
                className="textarea-field pl-14 min-h-[400px]"
                spellCheck="false"
            />

        </div>
    );
};

export default CodeEditor;
