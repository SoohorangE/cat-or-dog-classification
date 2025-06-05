let uploadedImage = "";

document.getElementById("upload").addEventListener("change", function (e) {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = function () {
    uploadedImage = reader.result.split(",")[1];
  };
  reader.readAsDataURL(file);
});

async function sendImage() {
  if (!uploadedImage) {
    alert("이미지를 먼저 선택하세요!");
    return;
  }

  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: uploadedImage }),
  });

  const data = await response.json();
  document.getElementById("result").src = "data:image/png;base64," + data.image;
}