(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const defaultCenter = [11.0168, 76.9558];
  let selected = null;
  let marker = null;
  let lastRequest = 0;

  const status = (message, kind = "") => {
    $("status").textContent = message;
    $("status").className = "status" + (kind ? " " + kind : "");
  };
  const safe = value => String(value ?? "").replace(/[&<>"']/g, char => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  }[char]));
  const setBusy = busy => {
    $("assess").disabled = busy;
    $("assess").innerHTML = busy ? "Assessing conditions…" : 'Assess selected location <span aria-hidden="true">→</span>';
  };

  if (!window.L) {
    status("The map library could not load. Check your internet connection and refresh the page.", "error");
    $("map-help").textContent = "Map unavailable — check your connection and reload.";
    $("locate").disabled = true;
    $("assess").disabled = true;
    return;
  }

  const map = L.map("map", { scrollWheelZoom: true }).setView(defaultCenter, 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);
  map.on("click", event => chooseLocation(event.latlng.lat, event.latlng.lng, true));

  function chooseLocation(lat, lon, pan = false) {
    selected = { lat: Number(lat), lon: Number(lon) };
    if (marker) marker.remove();
    marker = L.marker([selected.lat, selected.lon]).addTo(map);
    if (pan) map.panTo([selected.lat, selected.lon]);
    $("coords").textContent = selected.lat.toFixed(5) + ", " + selected.lon.toFixed(5);
    $("place").textContent = "Selected map location";
    $("map-help").textContent = "Location selected. Review conditions and assess the risk.";
    $("result-state").textContent = "Ready to assess";
    status("Location selected. Add any known road conditions, then assess.", "success");
    assess();
  }

  $("locate").addEventListener("click", () => {
    if (!navigator.geolocation) {
      status("This browser does not support GPS location. Select a point on the map instead.", "error");
      return;
    }
    $("locate").disabled = true;
    $("locate").textContent = "Finding location…";
    status("Waiting for your device to provide location permission…");
    navigator.geolocation.getCurrentPosition(position => {
      const { latitude, longitude } = position.coords;
      map.setView([latitude, longitude], 16);
      chooseLocation(latitude, longitude);
      $("place").textContent = "Your current location";
      $("locate").textContent = "◎ Use my location";
      $("locate").disabled = false;
    }, error => {
      const messages = {
        1: "Location permission was denied. Allow location access in your browser or select a map point.",
        2: "Your device could not determine a location. Try again or select a map point.",
        3: "Location lookup timed out. Try again or select a map point."
      };
      status(messages[error.code] || "Could not get your location. Select a point on the map instead.", "error");
      $("locate").textContent = "◎ Use my location";
      $("locate").disabled = false;
    }, { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 });
  });

  $("assess").addEventListener("click", assess);
  $("reset").addEventListener("click", () => {
    selected = null;
    if (marker) marker.remove();
    marker = null;
    $("place").textContent = "No location selected";
    $("coords").textContent = "Choose a point on the map or use GPS";
    $("map-help").textContent = "Click the map to choose a road location.";
    $("score").textContent = "—";
    $("score-ring").style.setProperty("--score-angle", "0deg");
    $("level").textContent = "NOT ASSESSED";
    $("level").className = "badge badge-neutral";
    $("result-title").textContent = "Your assessment will appear here";
    $("weather").textContent = "Weather data has not been loaded.";
    $("score-note").textContent = "The score is a relative baseline index, not an accident probability.";
    $("factors").innerHTML = '<li class="empty-item">Complete an assessment to see the factors considered.</li>';
    $("recommendations").innerHTML = '<li class="empty-item">General guidance will appear after assessment.</li>';
    $("result-state").textContent = "Awaiting assessment";
    status("Selection cleared. Choose a location to start again.");
  });

  async function assess() {
    if (!selected) {
      status("Choose a point on the map or use your current location first.", "error");
      $("place").textContent = "Location required";
      return;
    }
    const requestId = ++lastRequest;
    setBusy(true);
    $("result-state").textContent = "Assessing…";
    status("Fetching available weather and location context…");
    const body = {
      lat: selected.lat,
      lon: selected.lon,
      traffic_level: $("traffic").value || null,
      road_type: $("road").value || null,
      visibility_m: $("visibility").value ? Number($("visibility").value) : null,
      is_night: $("night").checked
    };
    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      if (!response.ok) {
        let detail = "Server returned HTTP " + response.status;
        try { const error = await response.json(); if (error.detail) detail = typeof error.detail === "string" ? error.detail : JSON.stringify(error.detail); } catch {}
        throw new Error(detail);
      }
      const data = await response.json();
      if (requestId !== lastRequest) return;
      renderResult(data);
      status("Assessment completed. Review the contributing factors and data limitations.", "success");
      $("result-state").textContent = "Assessment complete";
    } catch (error) {
      if (requestId !== lastRequest) return;
      status("Assessment failed: " + error.message + ". Check that the server is running, then try again.", "error");
      $("result-state").textContent = "Request failed";
    } finally {
      if (requestId === lastRequest) setBusy(false);
    }
  }

  function renderResult(data) {
    const score = Math.max(0, Math.min(100, Number(data.risk_score) || 0));
    const level = String(data.risk_level || "UNKNOWN").toUpperCase();
    $("score").textContent = String(score);
    $("score-ring").style.setProperty("--score-angle", (score * 3.6) + "deg");
    $("level").textContent = level + " BASELINE";
    $("level").className = "badge " + (level === "LOW" ? "badge-low" : level === "MEDIUM" ? "badge-medium" : level === "HIGH" ? "badge-high" : "badge-neutral");
    $("result-title").textContent = level === "LOW" ? "Fewer risk signals detected" : level === "MEDIUM" ? "Use additional caution" : level === "HIGH" ? "Several risk signals detected" : "Assessment returned";
    $("place").textContent = data.location_label || "Selected map location";
    $("weather").textContent = data.weather_summary || "Current weather information is unavailable.";
    $("score-note").textContent = data.disclaimer || "Relative baseline index only; not a calibrated accident probability.";
    const factors = Array.isArray(data.factors) ? data.factors : [];
    $("factors").innerHTML = factors.length
      ? factors.map(f => '<li><b>' + safe(f.name) + '</b> — ' + safe(f.detail) + '</li>').join("")
      : '<li class="empty-item">No additional risk factors were reported for the supplied inputs. This does not mean the road is hazard-free.</li>';
    const recommendations = Array.isArray(data.recommendations) ? data.recommendations : [];
    $("recommendations").innerHTML = recommendations.length
      ? recommendations.map(item => "<li>" + safe(item) + "</li>").join("")
      : "<li>Follow posted road signs and adjust driving to actual conditions.</li>";
  }
})();