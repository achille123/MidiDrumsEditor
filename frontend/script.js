const uploadInput = document.getElementById("audio-upload");
const filenameDisplay = document.getElementById("filename");
const loader = document.getElementById("loader");
const audioPlayer = document.getElementById("audio-player");

uploadInput.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  filenameDisplay.textContent = `🎵 ${file.name}`;
  audioPlayer.src = URL.createObjectURL(file);
  if (audioPlayer.classList.contains("hidden")) {
    audioPlayer.classList.remove("hidden");
  }

  loader.classList.remove("hidden");

  const formData = new FormData();
  formData.append("audio", file);

  try {
    // 1. Upload audio vers upload_service (port 5002)
    const uploadRes = await fetch("http://localhost:5002/upload-audio", {
      method: "POST",
      body: formData
    });

    if (!uploadRes.ok) throw new Error("Erreur upload");
    const uploadData = await uploadRes.json();
    const filename = uploadData.filename;

    // 2. Appel vers midi_service (port 5000)
    const midiRes = await fetch("http://localhost:5000/generate-midi", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename })
    });

    if (!midiRes.ok) throw new Error("Erreur MIDI");
    const midiBlob = await midiRes.blob();
    const midiUrl = URL.createObjectURL(midiBlob);

    // 3. Téléchargement du fichier MIDI
    const a = document.createElement("a");
    a.href = midiUrl;
    a.download = filename.replace(/\.[^/.]+$/, "") + ".mid";
    a.click();

  } catch (error) {
    loader.textContent = "❌ Erreur serveur";
    loader.classList.remove("animate-pulse");
    console.error("❌ Erreur :", error);
  } finally {
    loader.classList.add("hidden");
  }
});
