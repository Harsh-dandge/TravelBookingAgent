document.addEventListener("DOMContentLoaded", () => {
    const asLocalDate = (value) => [
        value.getFullYear(),
        String(value.getMonth() + 1).padStart(2, "0"),
        String(value.getDate()).padStart(2, "0")
    ].join("-");
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const returnDate = new Date(tomorrow);
    returnDate.setDate(returnDate.getDate() + 7);
    const checkoutDate = new Date(tomorrow);
    checkoutDate.setDate(checkoutDate.getDate() + 2);

    for (const id of ["flight-date", "hotel-checkin"]) {
        const field = document.getElementById(id);
        if (field) field.value = asLocalDate(tomorrow);
    }
    const returnField = document.getElementById("flight-return");
    if (returnField) returnField.value = asLocalDate(returnDate);
    const checkout = document.getElementById("hotel-checkout");
    if (checkout) checkout.value = asLocalDate(checkoutDate);
});

function switchTab(tabName) {
    document.querySelectorAll(".tab-content").forEach((tab) => {
        tab.classList.toggle("active", tab.id === tabName);
    });
    document.querySelectorAll(".tab-btn").forEach((button) => {
        button.classList.toggle(
            "active",
            button.getAttribute("onclick") === `switchTab('${tabName}')`
        );
    });
}

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

async function postSearch(url, payload, resultsDiv, render) {
    resultsDiv.textContent = "Searching...";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.error || `Search failed (${response.status})`);
        }
        resultsDiv.innerHTML = render(data);
    } catch (error) {
        resultsDiv.innerHTML = `<p class="search-error" role="alert">${escapeHtml(error.message || "Search failed")}</p>`;
    }
}

function searchFlights(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        departure: form.elements.departure.value,
        arrival: form.elements.arrival.value,
        date: form.elements.date.value,
        return_date: form.elements.return_date.value || null,
        adults: Number(form.elements.adults.value),
        children: Number(form.elements.children.value)
    };
    const results = document.getElementById("flights-result");
    postSearch("/api/flights", payload, results, (data) => {
        if (!data.flights.length) return "<p>No flights found for these dates.</p>";
        return data.flights.map((flight) => `
            <article class="flight-card">
                <div class="flight-info">
                    <h3>${escapeHtml(flight.airline)}</h3>
                    <p>${escapeHtml(flight.price ?? "Price unavailable")}</p>
                </div>
                <div class="flight-details">
                    <span>${escapeHtml(flight.duration ?? "Duration unavailable")} min</span>
                    <span>${flight.stops === 0 ? "Non-stop" : `${escapeHtml(flight.stops)} stop(s)`}</span>
                    <span>${escapeHtml(flight.departure_time)} – ${escapeHtml(flight.arrival_time)}</span>
                </div>
            </article>`).join("");
    });
}

function searchHotels(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        location: form.elements.location.value,
        check_in: form.elements.check_in.value,
        check_out: form.elements.check_out.value,
        guests: Number(form.elements.guests.value)
    };
    const results = document.getElementById("hotels-result");
    postSearch("/api/hotels", payload, results, (data) => {
        if (!data.hotels.length) return "<p>No hotels found for these dates.</p>";
        return data.hotels.map((hotel) => `
            <article class="hotel-card">
                <h3>${escapeHtml(hotel.name)}</h3>
                <p class="price">${escapeHtml(hotel.price)} / night</p>
                <p class="hotel-rating">Rating: ${escapeHtml(hotel.rating)}</p>
                <p class="reviews">${escapeHtml(hotel.reviews)} reviews</p>
                <p>${escapeHtml(hotel.address)}</p>
            </article>`).join("");
    });
}

function searchEvents(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        event_type: form.elements.event_type.value,
        location: form.elements.location.value
    };
    const results = document.getElementById("events-result");
    postSearch("/api/events", payload, results, (data) => {
        if (!data.events.length) return "<p>No events found for this search.</p>";
        return data.events.map((item) => {
            let link = "";
            try {
                const url = new URL(item.event_link);
                if (["https:", "http:"].includes(url.protocol)) {
                    link = `<a href="${escapeHtml(url.href)}" target="_blank" rel="noopener noreferrer">Event details</a>`;
                }
            } catch {
                link = "";
            }
            return `<article class="event-card">
                <h3>${escapeHtml(item.title)}</h3>
                <p class="event-date">${escapeHtml(item.date)}</p>
                <p class="event-location">${escapeHtml(item.location)}</p>
                <p>${escapeHtml(item.ticket_price)}</p>${link}
            </article>`;
        }).join("");
    });
}

const weatherDescriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm"
};

function searchWeather(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const results = document.getElementById("weather-result");
    postSearch("/api/weather", { location: form.elements.location.value }, results, (data) => {
        if (!data.weather.length) return "<p>No forecast available for this location.</p>";
        return `<p class="forecast-location">Five-day forecast for ${escapeHtml(data.location)}</p>` +
            data.weather.map((day) => `
                <article class="weather-card">
                    <p class="weather-date">${escapeHtml(day.date)}</p>
                    <p class="weather-temp">${escapeHtml(day.temp_max)}° / ${escapeHtml(day.temp_min)}°C</p>
                    <p class="weather-desc">${escapeHtml(weatherDescriptions[day.weather_code] || "Forecast available")}</p>
                    <p>Precipitation: ${escapeHtml(day.precipitation)} mm</p>
                </article>`).join("");
    });
}
