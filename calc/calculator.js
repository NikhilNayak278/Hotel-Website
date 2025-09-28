// Load items.json and populate calculator
let itemsData = null;
let allItems = []; // Flattened array of all items

const totalDisplay = document.getElementById('total-cost');

async function loadItems() {
    try {
        console.log('Attempting to fetch items.json...');
        const response = await fetch('../items.json');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        itemsData = await response.json();
        console.log('Items loaded successfully:', itemsData);
        
        // Flatten all items from all categories into a single array
        allItems = [];
        Object.keys(itemsData).forEach(category => {
            itemsData[category].forEach(item => {
                allItems.push({
                    ...item,
                    category: category
                });
            });
        });
        
        console.log('Flattened items:', allItems);
        
        // Now create the first item row after data is loaded
        if (container) {
            container.appendChild(createItemRow());
        }
        
    } catch (error) {
        console.error('Error loading items:', error);
        console.error('Make sure items.json exists at the correct path');
        
        // Fallback: create empty row even if loading fails
        if (container) {
            container.appendChild(createItemRow());
        }
    }
}

const container = document.getElementById('items');
const newItemBtn = document.getElementById('new-item');
const calculateBtn = document.getElementById('calculate');

function createItemRow() {
    const row = document.createElement('div');
    row.className = 'item-row';
    
    let optionsHTML = '<option disabled selected>Select an item</option>';
    
    if (allItems.length > 0) {
        // Group items by category
        const categories = {};
        allItems.forEach(item => {
            if (!categories[item.category]) {
                categories[item.category] = [];
            }
            categories[item.category].push(item);
        });
        
        // Create optgroups for each category
        Object.keys(categories).forEach(category => {
            optionsHTML += `<optgroup label="${category.replace('_', ' ').toUpperCase()}">`;
            categories[category].forEach(item => {
                optionsHTML += `<option value="${item.id}" data-price="${item.cost}">${item.name} - ₹${item.cost}</option>`;
            });
            optionsHTML += '</optgroup>';
        });
    }
    
    row.innerHTML = `
        <select class="item-selection-menu">
            ${optionsHTML}
        </select>
        <input type="number" class="item-quantity" value="1" min="1">
        <span class="item-price">₹0</span>
        <button type="button" class="remove-item">Remove</button>
    `;
    
    // Add event listeners
    const selector = row.querySelector('.item-selection-menu');
    const quantity = row.querySelector('.item-quantity');
    const priceSpan = row.querySelector('.item-price');
    const removeBtn = row.querySelector('.remove-item');
    
    function updatePrice() {
        const selectedOption = selector.selectedOptions[0];
        if (selectedOption && selectedOption.dataset.price) {
            const price = parseFloat(selectedOption.dataset.price);
            const qty = parseInt(quantity.value) || 1;
            const total = price * qty;
            priceSpan.textContent = `₹${total}`;
        } else {
            priceSpan.textContent = '₹0';
        }
    }
    
    selector.addEventListener('change', updatePrice);
    quantity.addEventListener('input', updatePrice);
    removeBtn.addEventListener('click', () => {
        row.remove();
    });
    
    return row;
}

// Wait for DOM to be ready, then load items
document.addEventListener('DOMContentLoaded', () => {
    loadItems();
    
    // Add event listeners for buttons
    if (newItemBtn) {
        newItemBtn.addEventListener('click', () => {
            container.appendChild(createItemRow());
        });
    }
    
    if (calculateBtn) {
        calculateBtn.addEventListener('click', calculateTotal);
    }
});

function calculateTotal() {
    const itemRows = container.querySelectorAll('.item-row');
    let total = 0;
    
    itemRows.forEach(row => {
        const selector = row.querySelector('.item-selection-menu');
        const quantity = row.querySelector('.item-quantity');
        const selectedOption = selector.selectedOptions[0];
        
        if (selectedOption && selectedOption.dataset.price) {
            const price = parseFloat(selectedOption.dataset.price);
            const qty = parseInt(quantity.value) || 1;
            total += price * qty;
        }
    });
    
    console.log('Total cost:', total);
    
    // Update the total display
    const totalCostElement = document.getElementById('total-cost');
    if (totalCostElement) {
        totalCostElement.textContent = total.toFixed(2);
    }
    
    // Show breakdown if there are items
    if (total > 0) {
        const gst = total * 0.18;
        const totalWithGst = total + gst;
        console.log(`Subtotal: ₹${total.toFixed(2)}`);
        console.log(`GST (18%): ₹${gst.toFixed(2)}`);
        console.log(`Total with GST: ₹${totalWithGst.toFixed(2)}`);
    }
}