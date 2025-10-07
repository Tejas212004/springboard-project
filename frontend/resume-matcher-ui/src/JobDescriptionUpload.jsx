import { useState } from "react";
import axios from "axios";

function JobDescriptionUpload({ onJobParsed }) {
  const [file, setFile] = useState(null);
  const [rawText, setRawText] = useState("");
  const [response, setResponse] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload-job", formData);
      setResponse(res.data);
      onJobParsed(res.data); // pass to parent
    } catch (err) {
      console.error("Job upload failed:", err);
    }
  };

  const handleRawSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:8000/upload-job-text", {
        text: rawText,
      });
      setResponse(res.data);
      onJobParsed(res.data);
    } catch (err) {
      console.error("Raw job text failed:", err);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-bold text-blue-700 mb-4">Upload Job Description</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
                   file:rounded-full file:border-0 file:text-sm file:font-semibold
                   file:bg-blue-600 file:text-white hover:file:bg-blue-700"
      />
      <button
        onClick={handleUpload}
        className="w-full py-2 px-4 bg-green-600 hover:bg-green-700 text-white font-semibold rounded mb-6"
      >
        Upload Job File
      </button>

      <textarea
        rows={6}
        placeholder="Or paste job description here..."
        value={rawText}
        onChange={(e) => setRawText(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded mb-4"
      />
      <button
        onClick={handleRawSubmit}
        className="w-full py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded"
      >
        Submit Raw Text
      </button>

      {response && (
        <div className="mt-6 bg-indigo-50 border border-indigo-200 rounded p-4">
          <h3 className="text-lg font-bold text-indigo-700 mb-2">Job Preview:</h3>
          <p className="text-sm text-gray-700">{response.preview}</p>
        </div>
      )}
    </div>
  );
}

export default JobDescriptionUpload;