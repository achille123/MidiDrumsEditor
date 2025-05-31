import { useState } from 'react';

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('audio', file);

    try {
      const res = await fetch('http://localhost:5000/upload-audio', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Upload failed', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept="audio/*" onChange={handleFileChange} />
      <button type="submit">Upload Audio</button>
      {response && (
        <div>
          <h3>Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </form>
  );
}
