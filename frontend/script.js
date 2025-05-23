const uploadInput = document.getElementById("audio-upload");
const filenameDisplay = document.getElementById("filename");
const loader = document.getElementById("loader");
const audioPlayer = document.getElementById("audio-player");

uploadInput.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // ✅ Afficher le nom du fichier
  filenameDisplay.textContent = `🎵 ${file.name}`;

  // ✅ Préparer le lecteur audio
  const audioURL = URL.createObjectURL(file);
  audioPlayer.src = audioURL;

  // ✅ Forcer le lecteur à apparaître
  if (audioPlayer.classList.contains("hidden")) {
    audioPlayer.classList.remove("hidden");

  }

  // ✅ Afficher le loader
  loader.classList.remove("hidden");

  const formData = new FormData();
  formData.append("audio", file);

  try {
    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData
    });

    if (!response.ok) throw new Error("Erreur serveur");

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "converted.mid";
    a.click();
  } catch (error) {
    loader.textContent = "❌ Erreur serveur";
    loader.classList.remove("animate-pulse");
    console.error("❌ Erreur :", error);
  } finally {
    loader.classList.add("hidden");

    // 🔁 NE cache surtout pas le lecteur ici
    // donc on ne touche PAS à audioPlayer.classList ici
  }
});
