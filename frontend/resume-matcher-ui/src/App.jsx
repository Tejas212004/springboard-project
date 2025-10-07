import React, { useState } from 'react';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobText, setJobText] = useState('');
  const [matchResult, setMatchResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleResumeUpload = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleJobTextChange = (e) => {
    setJobText(e.target.value);
  };

  const handleMatch = async () => {
    if (!resumeFile || !jobText) {
      alert("Please upload a resume and paste a job description.");
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_text", jobText);

    try {
      const response = await fetch("http://localhost:8000/match-resume-job", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.error) {
        alert("Error: " + data.error);
        setMatchResult(null);
      } else {
        setMatchResult(data);
      }
    } catch (error) {
      console.error("Error matching resume:", error);
      alert("Something went wrong. Check your backend.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-blue-100 p-6">
      <div className="max-w-5xl mx-auto space-y-10">

        {/* Header */}
        <header className="text-center">
          <h1 className="text-4xl md:text-5xl font-extrabold text-indigo-700 mb-2">Skill Resume Matcher</h1>
          <p className="text-gray-600 text-lg">AI-powered resume screening and skill gap analysis</p>
        </header>

        {/* Upload Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Resume Upload */}
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
            <h2 className="text-2xl font-bold text-blue-700">Upload Resume</h2>
            <input
              type="file"
              onChange={handleResumeUpload}
              className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
            />
            <button
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition"
              onClick={() => alert("Resume uploaded!")}
            >
              Upload
            </button>
          </div>

          {/* Job Description Upload */}
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
            <h2 className="text-2xl font-bold text-green-700">Paste Job Description</h2>
            <textarea
              value={jobText}
              onChange={handleJobTextChange}
              className="w-full h-40 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400"
              placeholder="Paste job description here..."
            ></textarea>
            <button
              className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition"
              onClick={() => alert("Job description submitted!")}
            >
              Submit
            </button>
          </div>
        </div>

        {/* Match Button */}
        <div className="text-center">
          <button
            className={`mt-6 py-3 px-6 font-bold rounded-lg shadow-md transition duration-300 ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-purple-600 hover:bg-purple-700 text-white'
            }`}
            onClick={handleMatch}
            disabled={isLoading}
          >
            {isLoading ? 'Matching...' : 'Match Resume with Job Description'}
          </button>
        </div>

        {/* Loading Spinner */}
        {isLoading && (
          <div className="flex justify-center items-center py-6">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-600 border-opacity-50"></div>
          </div>
        )}

        {/* Results Section */}
        {matchResult && (
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-4">
            <h2 className="text-2xl font-bold text-purple-700">Match Results</h2>
            <p className="text-lg text-gray-700">
              Match Score: <span className="font-bold text-purple-600">{matchResult.match_score}%</span>
            </p>

            <div>
              <h3 className="text-xl font-semibold text-green-600">Matched Skills</h3>
              <ul className="list-disc list-inside text-gray-700">
                {matchResult.matched_skills.map((skill, idx) => (
                  <li key={idx}>{skill}</li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-red-600">Missing Skills</h3>
              <ul className="list-disc list-inside text-gray-700">
                {matchResult.missing_skills.map((skill, idx) => (
                  <li key={idx}>{skill}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;