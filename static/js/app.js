// State management
let stores = [];
let categories = [];
let items = [];

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
    // Set current date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date-input').value = today;
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Setup tabs
    setupTabs();

    // Load initial data
    await loadData();

    // Setup forms
    setupForms();

    // Load today's summary
    loadTodaySummary();
});

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;

            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab
            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            // Load data for specific tabs
            if (tabId === 'view-prices') {
                loadRecentPrices();
            } else if (tabId === 'comparison') {
                loadComparison();
            } else if (tabId === 'manage') {
                loadItemsList();
            }
        });
    });
}

async function loadData() {
    try {
        // Load stores
        const storesRes = await fetch('/api/stores');
        stores = await storesRes.json();
        populateStoreSelect();

        // Load categories
        const categoriesRes = await fetch('/api/categories');
        categories = await categoriesRes.json();
        populateCategorySelect();

        // Load items
        const itemsRes = await fetch('/api/items');
        items = await itemsRes.json();
        populateItemSelects();
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification('Error loading data', 'error');
    }
}

function populateStoreSelect() {
    const select = document.getElementById('store-select');
    select.innerHTML = '<option value="">Select a store...</option>';
    stores.forEach(store => {
        const option = document.createElement('option');
        option.value = store.id;
        option.textContent = store.name;
        select.appendChild(option);
    });
}

function populateCategorySelect() {
    const select = document.getElementById('category-select');
    select.innerHTML = '<option value="">Select category...</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.name;
        select.appendChild(option);
    });
}

function populateItemSelects() {
    // Populate main item select
    const itemSelect = document.getElementById('item-select');
    itemSelect.innerHTML = '<option value="">Select an item...</option>';
    
    // Group by category
    const grouped = {};
    items.forEach(item => {
        const category = item.category_name || 'Other';
        if (!grouped[category]) grouped[category] = [];
        grouped[category].push(item);
    });

    Object.keys(grouped).sort().forEach(category => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = category;
        grouped[category].forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            option.textContent = `${item.name} (${item.unit})`;
            optgroup.appendChild(option);
        });
        itemSelect.appendChild(optgroup);
    });

    // Populate trend item select
    const trendSelect = document.getElementById('trend-item-select');
    trendSelect.innerHTML = '<option value="">Choose an item to see trends...</option>';
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = `${item.name} (${item.unit})`;
        trendSelect.appendChild(option);
    });
}

function setupForms() {
    // Add price form
    document.getElementById('add-price-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            item_id: parseInt(document.getElementById('item-select').value),
            store_id: parseInt(document.getElementById('store-select').value),
            price: parseFloat(document.getElementById('price-input').value),
            date: document.getElementById('date-input').value,
            notes: document.getElementById('notes-input').value
        };

        try {
            const res = await fetch('/api/prices', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                showNotification('Price added successfully!', 'success');
                e.target.reset();
                document.getElementById('date-input').value = new Date().toISOString().split('T')[0];
                loadTodaySummary();
            } else {
                showNotification('Error adding price', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error adding price', 'error');
        }
    });

    // Add item form
    document.getElementById('add-item-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            name: document.getElementById('item-name').value,
            category_id: parseInt(document.getElementById('category-select').value),
            unit: document.getElementById('unit-input').value || 'each'
        };

        try {
            const res = await fetch('/api/items', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                showNotification('Item added successfully!', 'success');
                e.target.reset();
                document.getElementById('unit-input').value = 'each';
                await loadData();
                loadItemsList();
            } else {
                showNotification('Error adding item', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error adding item', 'error');
        }
    });

    // Add store form
    document.getElementById('add-store-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            name: document.getElementById('store-name').value,
            location: document.getElementById('store-location').value
        };

        try {
            const res = await fetch('/api/stores', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                showNotification('Store added successfully!', 'success');
                e.target.reset();
                document.getElementById('store-location').value = 'Yellowknife, NT';
                await loadData();
            } else {
                const error = await res.json();
                showNotification(error.error || 'Error adding store', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('Error adding store', 'error');
        }
    });

    // Days filter
    document.getElementById('days-filter').addEventListener('change', loadRecentPrices);

    // Trend item select
    document.getElementById('trend-item-select').addEventListener('change', async (e) => {
        const itemId = e.target.value;
        if (itemId) {
            await loadPriceTrends(itemId);
        } else {
            document.getElementById('trend-chart').innerHTML = '';
        }
    });
}

async function loadTodaySummary() {
    try {
        const res = await fetch('/api/daily-summary');
        const summary = await res.json();
        
        const container = document.getElementById('today-summary');
        
        if (summary.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No prices entered today yet.</p></div>';
            return;
        }

        const html = `
            <table>
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Store</th>
                        <th>Price</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    ${summary.map(entry => `
                        <tr>
                            <td>${entry.item_name} <span class="category-badge">${entry.category_name || 'Other'}</span></td>
                            <td><span class="store-badge">${entry.store_name}</span></td>
                            <td><span class="price-badge">$${entry.price.toFixed(2)}</span></td>
                            <td>${entry.notes || '-'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading today summary:', error);
    }
}

async function loadRecentPrices() {
    const days = document.getElementById('days-filter').value;
    
    try {
        const res = await fetch(`/api/prices?days=${days}`);
        const prices = await res.json();
        
        const container = document.getElementById('recent-prices');
        
        if (prices.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No price entries found.</p></div>';
            return;
        }

        const html = `
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Item</th>
                        <th>Store</th>
                        <th>Price</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
                    ${prices.map(entry => `
                        <tr>
                            <td>${new Date(entry.date).toLocaleDateString()}</td>
                            <td>${entry.item_name} <span class="category-badge">${entry.category_name || 'Other'}</span></td>
                            <td><span class="store-badge">${entry.store_name}</span></td>
                            <td><span class="price-badge">$${entry.price.toFixed(2)}</span></td>
                            <td>${entry.notes || '-'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading recent prices:', error);
    }
}

async function loadPriceTrends(itemId) {
    try {
        const res = await fetch(`/api/price-trends/${itemId}?days=90`);
        const trends = await res.json();
        
        const container = document.getElementById('trend-chart');
        
        if (trends.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No price history found for this item.</p></div>';
            return;
        }

        // Find min and max prices
        const prices = trends.map(t => t.price);
        const minPrice = Math.min(...prices);
        const maxPrice = Math.max(...prices);
        const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length;

        const html = `
            <div style="margin-bottom: 20px;">
                <h3>Price Statistics</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-top: 15px;">
                    <div class="item-card">
                        <p style="font-size: 0.85rem; margin-bottom: 5px;">Lowest Price</p>
                        <h4 style="color: var(--secondary-color); font-size: 1.5rem;">$${minPrice.toFixed(2)}</h4>
                    </div>
                    <div class="item-card">
                        <p style="font-size: 0.85rem; margin-bottom: 5px;">Highest Price</p>
                        <h4 style="color: var(--danger); font-size: 1.5rem;">$${maxPrice.toFixed(2)}</h4>
                    </div>
                    <div class="item-card">
                        <p style="font-size: 0.85rem; margin-bottom: 5px;">Average Price</p>
                        <h4 style="color: var(--primary-color); font-size: 1.5rem;">$${avgPrice.toFixed(2)}</h4>
                    </div>
                </div>
            </div>
            <h3>Price History</h3>
            <div style="margin-top: 15px;">
                ${trends.map(trend => `
                    <div class="price-trend-item">
                        <div>
                            <div class="trend-date">${new Date(trend.date).toLocaleDateString()}</div>
                            <div class="trend-store">${trend.store_name}</div>
                            ${trend.notes ? `<div style="font-size: 0.85rem; color: var(--text-secondary);">${trend.notes}</div>` : ''}
                        </div>
                        <div>
                            <span class="price-badge" style="font-size: 1.1rem;">$${trend.price.toFixed(2)}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading price trends:', error);
    }
}

async function loadComparison() {
    try {
        const res = await fetch('/api/price-comparison');
        const data = await res.json();
        
        const container = document.getElementById('comparison-table');
        
        if (data.length === 0) {
            container.innerHTML = '<div class="empty-state"><p>No price data available for comparison.</p></div>';
            return;
        }

        // Group by item
        const grouped = {};
        data.forEach(row => {
            if (!grouped[row.item_name]) {
                grouped[row.item_name] = {
                    name: row.item_name,
                    unit: row.unit,
                    category: row.category_name,
                    stores: []
                };
            }
            grouped[row.item_name].stores.push({
                store: row.store_name,
                price: row.price,
                date: row.date
            });
        });

        let html = '<div class="comparison-grid">';
        
        Object.values(grouped).forEach(item => {
            if (item.stores.length === 0) return;
            
            // Find best price
            const minPrice = Math.min(...item.stores.map(s => s.price));
            
            html += `
                <div class="comparison-item">
                    <h4>${item.name} (${item.unit}) <span class="category-badge">${item.category || 'Other'}</span></h4>
                    <div class="store-prices">
                        ${item.stores.map(store => `
                            <div class="store-price-card ${store.price === minPrice ? 'best-price' : ''}">
                                <div class="store">${store.store}</div>
                                <div class="price">$${store.price.toFixed(2)}</div>
                                <div class="date">${new Date(store.date).toLocaleDateString()}</div>
                                ${store.price === minPrice ? '<div style="color: var(--secondary-color); font-weight: 600; font-size: 0.85rem; margin-top: 5px;">Best Price!</div>' : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    } catch (error) {
        console.error('Error loading comparison:', error);
    }
}

async function loadItemsList() {
    const container = document.getElementById('items-list');
    
    if (items.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No items added yet.</p></div>';
        return;
    }

    // Group by category
    const grouped = {};
    items.forEach(item => {
        const category = item.category_name || 'Other';
        if (!grouped[category]) grouped[category] = [];
        grouped[category].push(item);
    });

    let html = '';
    Object.keys(grouped).sort().forEach(category => {
        html += `
            <h4 style="margin-top: 20px; margin-bottom: 10px; color: var(--primary-color);">${category}</h4>
            <div class="items-grid">
                ${grouped[category].map(item => `
                    <div class="item-card">
                        <h4>${item.name}</h4>
                        <p>Unit: ${item.unit}</p>
                    </div>
                `).join('')}
            </div>
        `;
    });

    container.innerHTML = html;
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
