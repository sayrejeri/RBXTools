(async function () {
  const owner = "sayrejeri";
  const repo = "RBXTools";
  const api = `https://api.github.com/repos/${owner}/${repo}/releases/latest`;

  const versionPill = document.getElementById("versionPill");
  const releaseMeta = document.getElementById("releaseMeta");
  const releaseNotes = document.getElementById("releaseNotes");
  const downloadBtn = document.getElementById("downloadBtn");

  function escapeHtml(str) {
    return str
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  try {
    const res = await fetch(api, { headers: { "Accept": "application/vnd.github+json" } });
    if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);

    const rel = await res.json();
    const tag = rel.tag_name || "Unknown";
    const published = rel.published_at ? new Date(rel.published_at) : null;
    const prettyDate = published
      ? published.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })
      : "Unknown date";

    // Update version pill
    versionPill.innerHTML = `Current version: <strong>${escapeHtml(tag)}</strong>`;

    // Update changelog meta
    releaseMeta.textContent = `Latest release: ${tag} • Published ${prettyDate}`;

    // Update download button to point at the release page
    if (rel.html_url) downloadBtn.href = rel.html_url;

    // Show release notes (body)
    const body = (rel.body || "").trim();
    if (!body) {
      releaseNotes.innerHTML = `<p class="muted">No release notes provided for ${escapeHtml(tag)}.</p>`;
    } else {
      // Keep formatting readable without trying to render markdown
      releaseNotes.innerHTML = `<pre>${escapeHtml(body)}</pre>`;
    }
  } catch (err) {
    // Fallbacks if GitHub API rate-limits anonymous requests
    versionPill.innerHTML = `Current version: <strong>See Releases</strong>`;
    releaseMeta.textContent = "Could not load latest release (GitHub API rate limit or offline).";
    releaseNotes.innerHTML = `<p class="muted">Please check the Releases page for the latest version and notes.</p>`;
  }
})();
