import React, { useState, useEffect } from 'react';
import CodeEditor from './components/CodeEditor';
import ReviewResult from './components/ReviewResult';
import FileUpload from './components/FileUpload';
import { reviewCode, checkHealth } from './api';

function App() {
    const [code, setCode] = useState('');
    const [description, setDescription] = useState('');
    const [language, setLanguage] = useState('python'); // Keep for API compatibility but remove UI control if needed, or just hardcode it in the call.
    // User specifically asked to remove language selection dropdown. 
    // I'll keep the state for now to avoid breaking the API call but remove the UI part.
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [healthStatus, setHealthStatus] = useState(null);
    const [showUpload, setShowUpload] = useState(false);

    // Check API health on mount
    useEffect(() => {
        const checkApiHealth = async () => {
            try {
                const health = await checkHealth();
                setHealthStatus(health);
            } catch (err) {
                console.error('Health check failed:', err);
                setHealthStatus({ status: 'error', message: 'API unavailable' });
            }
        };

        checkApiHealth();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!code.trim()) {
            setError('Please enter some code to review');
            return;
        }

        if (!description.trim()) {
            setError('Please provide a description of the code');
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const reviewResult = await reviewCode(code, description, language);
            setResult(reviewResult);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to review code. Please try again.');
            console.error('Review error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleClear = () => {
        setCode('');
        setDescription('');
        setResult(null);
        setError(null);
    };

    const exampleCode = `def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price']
    return total

def process_order(order_data):
    items = order_data['items']
    total = calculate_total(items)
    print("Total: " + str(total))
    return total`;

    const handleLoadExample = () => {
        setCode(exampleCode);
        setDescription('A simple function to calculate order total from a list of items');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
            {/* Header */}
            <header className="bg-slate-900/50 backdrop-blur-sm border-b border-slate-700 sticky top-0 z-10">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-2 rounded-lg">
                                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                                </svg>
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-white">AI Code Reviewer</h1>
                                <p className="text-sm text-slate-400">Powered by RAG & AWS Bedrock</p>
                            </div>
                        </div>

                        <div className="flex items-center space-x-4">
                            {healthStatus && (
                                <div className="flex items-center space-x-2">
                                    <div className={`w-2 h-2 rounded-full ${healthStatus.status === 'healthy' ? 'bg-green-500' :
                                        healthStatus.status === 'degraded' ? 'bg-yellow-500' :
                                            'bg-red-500'
                                        } animate-pulse`}></div>
                                    <span className="text-sm text-slate-400">
                                        {healthStatus.status === 'healthy' ? 'Online' :
                                            healthStatus.status === 'degraded' ? 'Degraded' : 'Offline'}
                                    </span>
                                </div>
                            )}

                            <button
                                onClick={() => setShowUpload(!showUpload)}
                                className="btn-secondary text-sm py-2 px-4"
                            >
                                {showUpload ? 'Hide Upload' : 'Upload Standards'}
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-4 py-8">
                {/* Upload Section */}
                {showUpload && (
                    <div className="mb-8 animate-fade-in">
                        <FileUpload onUploadSuccess={() => {
                            setTimeout(() => setShowUpload(false), 2000);
                        }} />
                    </div>
                )}

                {/* Input Section */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                    <div className="card">
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="text-xl font-bold text-white">Code Input</h2>
                            <div className="flex space-x-2">
                                <button
                                    onClick={handleLoadExample}
                                    className="text-sm text-primary-400 hover:text-primary-300 transition-colors"
                                >
                                    Load Example
                                </button>
                                <button
                                    onClick={handleClear}
                                    className="text-sm text-slate-400 hover:text-slate-300 transition-colors"
                                >
                                    Clear
                                </button>
                            </div>
                        </div>

                        {/* Language selection removed based on user request */}

                        <div className="mb-4">
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Description *
                            </label>
                            <input
                                type="text"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                placeholder="Describe what this code does..."
                                className="input-field"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-300 mb-2">
                                Code *
                            </label>
                            <CodeEditor
                                value={code}
                                onChange={setCode}
                                placeholder="Paste your code here..."
                                language="python" // Hardcoded since dropdown is removed
                            />
                        </div>
                    </div>

                    {/* Info Panel */}
                    <div className="space-y-6">
                        <div className="card">
                            <h2 className="text-xl font-bold text-white mb-4">How It Works</h2>
                            <div className="space-y-4">
                                <div className="flex items-start space-x-3">
                                    <div className="bg-primary-500/20 text-primary-400 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">
                                        1
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-white mb-1">Enter Your Code</h3>
                                        <p className="text-sm text-slate-400">
                                            Paste the code you want to review and provide a brief description.
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-start space-x-3">
                                    <div className="bg-primary-500/20 text-primary-400 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">
                                        2
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-white mb-1">RAG Retrieval</h3>
                                        <p className="text-sm text-slate-400">
                                            Relevant coding standards are retrieved from the knowledge base.
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-start space-x-3">
                                    <div className="bg-primary-500/20 text-primary-400 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">
                                        3
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-white mb-1">AI Analysis</h3>
                                        <p className="text-sm text-slate-400">
                                            AWS Bedrock analyzes your code against the standards.
                                        </p>
                                    </div>
                                </div>

                                <div className="flex items-start space-x-3">
                                    <div className="bg-primary-500/20 text-primary-400 rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-bold">
                                        4
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-white mb-1">Get Results</h3>
                                        <p className="text-sm text-slate-400">
                                            Receive detailed feedback, improvements, and refactored code.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="card bg-gradient-to-br from-primary-500/10 to-purple-500/10 border-primary-500/30">
                            <h3 className="font-semibold text-white mb-2">💡 Pro Tips</h3>
                            <ul className="text-sm text-slate-300 space-y-2">
                                <li>• Provide clear descriptions for better context</li>
                                <li>• Upload your company's coding standards</li>
                                <li>• Review one function or module at a time</li>
                                <li>• Use the refactored code as a learning resource</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* Submit Button */}
                <div className="flex justify-center mb-8">
                    <button
                        onClick={handleSubmit}
                        disabled={loading || !code.trim() || !description.trim()}
                        className="btn-primary text-lg px-12 py-4 flex items-center space-x-3"
                    >
                        {loading ? (
                            <>
                                <svg className="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <span>Analyzing Code...</span>
                            </>
                        ) : (
                            <>
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                                </svg>
                                <span>Review Code</span>
                            </>
                        )}
                    </button>
                </div>

                {/* Error Message */}
                {error && (
                    <div className="mb-8 animate-fade-in">
                        <div className="card bg-red-500/10 border-red-500/50">
                            <div className="flex items-center space-x-3">
                                <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                <p className="text-red-400">{error}</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Results Section */}
                {result && (
                    <div>
                        <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
                            <svg className="w-8 h-8 mr-3 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                            </svg>
                            Review Results
                        </h2>
                        <ReviewResult result={result} />
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="bg-slate-900/50 border-t border-slate-700 mt-16 py-6">
                <div className="container mx-auto px-4 text-center text-slate-400 text-sm">
                    <p>AI Code Reviewer - Powered by RAG & AWS Bedrock</p>
                    <p className="mt-2">Built with FastAPI, React, LangChain & FAISS</p>
                </div>
            </footer>
        </div>
    );
}

export default App;
