let urlCount = 0;

function addUrlRow(value = "") {
  if (urlCount >= 5) return;
  urlCount++;
  const list = document.getElementById("urlList");
  const row = document.createElement("div");
  row.className = "url-row";
  row.id = `urlrow-${urlCount}`;
  row.innerHTML = `
    <input type="text" placeholder="https://competitor-site.com" value="${value}" id="url-${urlCount}" />
    <button type="button" onclick="removeUrl(${urlCount})" title="Remove">×</button>
  `;
  list.appendChild(row);

  if (urlCount >= 5) {
    document.getElementById("addUrlBtn").disabled = true;
    document.getElementById("addUrlBtn").textContent = "Max 5 URLs reached";
  }
}

function removeUrl(n) {
  const el = document.getElementById(`urlrow-${n}`);
  if (el) el.remove();
  document.getElementById("addUrlBtn").disabled = false;
  document.getElementById("addUrlBtn").textContent = "+ Add URL";
}

function getUrls() {
  return Array.from(document.querySelectorAll("#urlList input"))
    .map(i => i.value.trim())
    .filter(Boolean);
}

document.getElementById("addUrlBtn").addEventListener("click", () => addUrlRow());

document.getElementById("seoForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const btn = document.getElementById("genBtn");
  btn.disabled = true;
  btn.textContent = "Scraping & generating...";

  document.getElementById("logWrap").classList.add("hidden");
  document.getElementById("outputWrap").classList.add("hidden");

  const payload = {
    bizName:        document.getElementById("bizName").value.trim(),
    bizDesc:        document.getElementById("bizDesc").value.trim(),
    industry:       document.getElementById("industry").value.trim(),
    location:       document.getElementById("location").value.trim(),
    schemaType:     document.getElementById("schemaType").value,
    competitorUrls: getUrls(),
  };

  try {
    const res = await fetch("http://localhost:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    // Show scrape log
    const logList = document.getElementById("logList");
    logList.innerHTML = "";
    data.log.forEach(entry => {
      const li = document.createElement("li");
      li.className = entry.status;
      if (entry.status === "ok") {
        li.innerHTML = `<span>🔗</span><span class="log-url">${entry.url}</span><span class="log-title">${entry.title}</span>`;
      } else {
        li.innerHTML = `<span>⚠</span><span class="log-url">${entry.url}</span><span class="log-title">${entry.msg}</span>`;
      }
      logList.appendChild(li);
    });
    document.getElementById("logWrap").classList.remove("hidden");

    // Show output
    document.getElementById("outputBox").textContent = data.seo;
    document.getElementById("outputWrap").classList.remove("hidden");
    document.getElementById("outputWrap").scrollIntoView({ behavior: "smooth" });

  } catch (err) {
    alert("Error: Could not connect to server.\nMake sure server.py is running on port 8000.");
    console.error(err);
  }

  btn.disabled = false;
  btn.textContent = "Generate SEO Code";
});

function copyCode() {
  const text = document.getElementById("outputBox").textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = event.target;
    btn.textContent = "Copied!";
    setTimeout(() => btn.textContent = "Copy", 2000);
  });
}

function downloadCode() {
  const text = document.getElementById("outputBox").textContent;
  const name = document.getElementById("bizName").value.trim().toLowerCase().replace(/\s+/g, "_") || "seo";
  const blob = new Blob([text], { type: "text/html" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `${name}_seo.html`;
  a.click();
}

addUrlRow();
addUrlRow();