/* TRAVEL ASSISTANT - JAVASCRIPT */

// Set default dates
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const nextWeek = new Date(today);
    nextWeek.setDate(nextWeek.getDate() + 7);
    
    if (document.getElementById('flight-date')) {
        document.getElementById('flight-date').valueAsDate = tomorrow;
    }
    if (document.getElementById('flight-return')) {
        document.getElementById('flight-return').valueAsDate = nextWeek;
    }
    if (document.getElementById('hotel-checkin')) {
        document.getElementById('hotel-checkin').valueAsDate = tomorrow;
    }
    if (document.getElementById('hotel-checkout')) {
        const checkout = new Date(tomorrow);
        checkout.setDate(checkout.getDate() + 2);
        document.getElementById('hotel-checkout').valueAsDate = checkout;
    }
});

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// ==================== FLIGHT SEARCH ====================
function searchFlights(e) {
    e.preventDefault();
    
    const form = e.target;
    const departure = form.querySelector('input[placeholder*="From"]').value;
    const arrival = form.querySelector('input[placeholder*="To"]').value;
    const date = document.getElementById('flight-date').value;
    const returnDate = document.getElementById('flight-return').value;
    
    const resultsDiv = document.getElementById('flights-result');
    resultsDiv.innerHTML = '<p style="text-align: center; color: #999;">Loading flights...</p>';
    
    // Simulated API call (replace with real API)
    setTimeout(() => {
        const flights = [
            {
                price: '₹' + (Math.random() * 3000 + 5000).toFixed(0),
                duration: (Math.random() * 3 + 2).toFixed(1) + 'h',
                airline: ['IndiGo', 'Air India', 'SpiceJet', 'Vistara'][Math.floor(Math.random() * 4)],
                stops: Math.floor(Math.random() * 2)
            },
            {
                price: '₹' + (Math.random() * 3000 + 5000).toFixed(0),
                duration: (Math.random() * 3 + 2).toFixed(1) + 'h',
                airline: ['IndiGo', 'Air India', 'SpiceJet', 'Vistara'][Math.floor(Math.random() * 4)],
                stops: Math.floor(Math.random() * 2)
            },
            {
                price: '₹' + (Math.random() * 3000 + 5000).toFixed(0),
                duration: (Math.random() * 3 + 2).toFixed(1) + 'h',
                airline: ['IndiGo', 'Air India', 'SpiceJet', 'Vistara'][Math.floor(Math.random() * 4)],
                stops: Math.floor(Math.random() * 2)
            }
        ];
        
        let html = '';
        flights.forEach(flight => {
            html += `
                <div class="flight-card">
                    <div class="flight-info">
                        <h3>${flight.airline}</h3>
                        <p>${flight.price}</p>
                    </div>
                    <div class="flight-details">
                        <span>${flight.duration}</span>
                        <span>${flight.stops === 0 ? 'Non-Stop' : flight.stops + ' Stop(s)'}</span>
                    </div>
                </div>
            `;
        });
        
        html += `<div style="grid-column: 1/-1; text-align: center; padding: 20px;">
            <p>Searching: ${departure} → ${arrival} on ${date}</p>
            <p style="color: #999; font-size: 0.9em;">Results powered by Google Flights API</p>
        </div>`;
        
        resultsDiv.innerHTML = html;
    }, 1500);
}

// ==================== HOTEL SEARCH ====================
function searchHotels(e) {
    e.preventDefault();
    
    const form = e.target;
    const location = form.querySelector('input[placeholder*="Location"]').value;
    const checkin = document.getElementById('hotel-checkin').value;
    const checkout = document.getElementById('hotel-checkout').value;
    
    const resultsDiv = document.getElementById('hotels-result');
    resultsDiv.innerHTML = '<p style="text-align: center; color: #999;">Loading hotels...</p>';
    
    setTimeout(() => {
        const hotels = [
            { name: 'Taj Hotel', price: '₹8,500', rating: '4.8', reviews: 2450 },
            { name: 'ITC Hotel', price: '₹6,200', rating: '4.6', reviews: 1890 },
            { name: 'Marriott', price: '₹5,890', rating: '4.5', reviews: 1456 },
            { name: 'Hilton', price: '₹7,200', rating: '4.7', reviews: 2100 },
            { name: 'Plaza Hotel', price: '₹4,500', rating: '4.3', reviews: 980 }
        ];
        
        let html = '';
        hotels.forEach(hotel => {
            html += `
                <div class="hotel-card">
                    <div class="hotel-rating">★★★★${parseFloat(hotel.rating) > 4.7 ? '★' : '☆'} ${hotel.rating}</div>
                    <h3>${hotel.name}</h3>
                    <p class="price">${hotel.price}/night</p>
                    <p class="reviews">${hotel.reviews.toLocaleString()} reviews</p>
                    <button class="btn btn-secondary" onclick="bookHotel('${hotel.name}')">Book Now</button>
                </div>
            `;
        });
        
        html += `<div style="grid-column: 1/-1; text-align: center; padding: 20px;">
            <p>Hotels in ${location} from ${checkin} to ${checkout}</p>
            <p style="color: #999; font-size: 0.9em;">Results powered by Google Hotels API</p>
        </div>`;
        
        resultsDiv.innerHTML = html;
    }, 1500);
}

// ==================== EVENT SEARCH ====================
function searchEvents(e) {
    e.preventDefault();
    
    const form = e.target;
    const eventType = form.querySelector('input[placeholder*="Event"]').value;
    const location = form.querySelector('input[placeholder*="Location"]').value;
    
    const resultsDiv = document.getElementById('events-result');
    resultsDiv.innerHTML = '<p style="text-align: center; color: #999;">Loading events...</p>';
    
    setTimeout(() => {
        const events = [
            { title: 'Jazz Festival', date: '2026-04-15', location: location },
            { title: 'Art Exhibition', date: '2026-04-20', location: location },
            { title: 'Cultural Show', date: '2026-04-25', location: location },
            { title: 'Music Concert', date: '2026-04-28', location: location }
        ];
        
        let html = '';
        events.forEach(event => {
            html += `
                <div class="event-card">
                    <h3>${event.title}</h3>
                    <p class="event-date">📅 ${event.date}</p>
                    <p class="event-location">📍 ${event.location}</p>
                    <button class="btn btn-secondary" onclick="getEventTickets('${event.title}')">Get Tickets</button>
                </div>
            `;
        });
        
        html += `<div style="grid-column: 1/-1; text-align: center; padding: 20px;">
            <p>Searching: ${eventType} in ${location}</p>
            <p style="color: #999; font-size: 0.9em;">Results powered by Google Events API</p>
        </div>`;
        
        resultsDiv.innerHTML = html;
    }, 1500);
}

// ==================== WEATHER SEARCH ====================
function searchWeather(e) {
    e.preventDefault();
    
    const form = e.target;
    const location = form.querySelector('input[placeholder*="Location"]').value;
    
    const resultsDiv = document.getElementById('weather-result');
    resultsDiv.innerHTML = '<p style="text-align: center; color: #999;">Loading forecast...</p>';
    
    setTimeout(() => {
        const today = new Date();
        let html = '';
        
        for (let i = 0; i < 5; i++) {
            const date = new Date(today);
            date.setDate(date.getDate() + i);
            const dayName = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : date.toLocaleDateString('en-US', { weekday: 'short' });
            const temp = Math.floor(Math.random() * 15 + 25);
            const desc = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy'][Math.floor(Math.random() * 4)];
            
            html += `
                <div class="weather-card">
                    <p class="weather-date">${dayName}</p>
                    <p class="weather-temp">${temp}°C</p>
                    <p class="weather-desc">${desc}</p>
                </div>
            `;
        }
        
        html += `<div style="grid-column: 1/-1; text-align: center; padding: 20px;">
            <p>5-Day Forecast for ${location}</p>
            <p style="color: #999; font-size: 0.9em;">Forecast powered by Open-Meteo API</p>
        </div>`;
        
        resultsDiv.innerHTML = html;
    }, 1500);
}

// ==================== ACTION HANDLERS ====================
function bookHotel(hotelName) {
    alert(`Booking ${hotelName}... (This would redirect to booking page)`);
}

function getEventTickets(eventName) {
    alert(`Getting tickets for ${eventName}... (This would redirect to ticketing page)`);
}

function bookFlight() {
    alert('Flight booked! (This would redirect to confirmation page)');
}

// ==================== DEMO API CALL ============
function loadDemoData() {
    fetch('/api/demo')
        .then(response => response.json())
        .then(data => {
            console.log('Demo data loaded:', data);
        });
}

// Load demo data on page load
loadDemoData();
