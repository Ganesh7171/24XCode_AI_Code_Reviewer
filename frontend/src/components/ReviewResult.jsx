import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

/**
 * ReviewResult Component
 * Displays the AI code review results
 */
const ReviewResult = ({ result }) => {
    if (!result) {
        return null;
    }

    const { issues, risks, improvements, refactored_code, explanation } = result;

    return (
        <div className="space-y-6 animate-fade-in">
            {/* Issues Section */}
            {issues && issues.length > 0 && (
                <div className="card">
                    <h3 className="text-xl font-bold text-red-400 mb-4 flex items-center">
                        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                        Issues Found ({issues.length})
                    </h3>
                    <ul className="space-y-2">
                        {issues.map((issue, index) => (
                            <li key={index} className="flex items-start">
                                <span className="text-red-400 mr-2">•</span>
                                <span className="text-slate-300">{issue}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Risks Section */}
            {risks && risks.length > 0 && (
                <div className="card">
                    <h3 className="text-xl font-bold text-orange-400 mb-4 flex items-center">
                        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Potential Risks ({risks.length})
                    </h3>
                    <ul className="space-y-2">
                        {risks.map((risk, index) => (
                            <li key={index} className="flex items-start">
                                <span className="text-orange-400 mr-2">•</span>
                                <span className="text-slate-300">{risk}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Improvements Section */}
            {improvements && improvements.length > 0 && (
                <div className="card">
                    <h3 className="text-xl font-bold text-green-400 mb-4 flex items-center">
                        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Suggested Improvements ({improvements.length})
                    </h3>
                    <ul className="space-y-2">
                        {improvements.map((improvement, index) => (
                            <li key={index} className="flex items-start">
                                <span className="text-green-400 mr-2">•</span>
                                <span className="text-slate-300">{improvement}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Refactored Code Section */}
            {refactored_code && (
                <div className="card">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-xl font-bold text-primary-400 flex items-center">
                            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                            </svg>
                            Refactored Code
                        </h3>
                        <button
                            onClick={() => {
                                navigator.clipboard.writeText(refactored_code);
                                // Optional: simple alert or state change for feedback
                                const btn = document.getElementById('copy-btn');
                                if (btn) {
                                    const originalText = btn.innerHTML;
                                    btn.innerHTML = '<svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Copied!';
                                    btn.classList.add('text-green-400');
                                    setTimeout(() => {
                                        btn.innerHTML = originalText;
                                        btn.classList.remove('text-green-400');
                                    }, 2000);
                                }
                            }}
                            id="copy-btn"
                            className="bg-slate-700/50 hover:bg-slate-600/50 text-slate-300 px-3 py-1.5 rounded-lg text-sm flex items-center transition-all duration-200 border border-slate-600/50"
                        >
                            <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m-3 8.5V17l.5-1m-.5 1l-.5-1" />
                            </svg>
                            Copy Code
                        </button>
                    </div>
                    <div className="rounded-lg overflow-hidden">
                        <SyntaxHighlighter
                            language="python"
                            style={vscDarkPlus}
                            customStyle={{
                                margin: 0,
                                borderRadius: '0.5rem',
                                fontSize: '0.875rem',
                            }}
                            showLineNumbers
                        >
                            {refactored_code}
                        </SyntaxHighlighter>
                    </div>
                </div>
            )}

            {/* Explanation Section */}
            {explanation && (
                <div className="card">
                    <h3 className="text-xl font-bold text-purple-400 mb-4 flex items-center">
                        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                        Explanation
                    </h3>
                    <p className="text-slate-300 leading-relaxed whitespace-pre-wrap">{explanation}</p>
                </div>
            )}
        </div>
    );
};

export default ReviewResult;
