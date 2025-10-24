const API = "http://127.0.0.1:5000";

async function loadW2() {
  const out = document.getElementById("w2");
  const res = await fetch(`${API}/w2`);
  const data = await res.json();
  out.textContent = JSON.stringify(data, null, 2);
}

async function estimate() {
  const filing_status = document.getElementById("status").value;
  const wages = Number(document.getElementById("wages").value);
  const withheld_federal = Number(document.getElementById("withheld").value);

  const res = await fetch(`${API}/estimate`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ filing_status, wages, withheld_federal })
  });
  const data = await res.json();
  document.getElementById("result").textContent =
    JSON.stringify(data, null, 2);
}
