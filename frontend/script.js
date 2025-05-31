const uploadInput = document.getElementById("audio-upload");
const loader = document.getElementById("loader");

uploadInput.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  loader.classList.remove("hidden");

  const formData = new FormData();
  formData.append("audio", file);

  try {
    console.log("📡 Envoi vers backend principal...");
    const res = await fetch("http://localhost:5002/upload-audio", {
      method: "POST",
      body: formData
    });

    if (!res.ok) throw new Error("❌ Échec upload");

    const data = await res.json();
    console.log("✅ Backend a traité le fichier :", data.message);

  } catch (err) {
    console.error("❌ Erreur:", err);
  } finally {
    loader.classList.add("hidden");
  }
});
