document.getElementById("audio-upload").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append("audio", file);

  const response = await fetch("http://localhost:5000/upload", {
    method: "POST",
    body: formData
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "converted.mid";
  a.click();
});
