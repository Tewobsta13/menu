// ── Helpers ────────────────────────────────────────────────────────────────

// sort method
const sortByPrice = function (arr) {
  return [...arr].sort((a, b) => a.price - b.price);
};

function buildStars(rating) {
  const full = "★".repeat(rating);
  const empty = "☆".repeat(5 - rating);
  return full + empty;
}

// card template
function createFoodCard(food) {
  return `
    <div class="food-card">
      <img src="${food.image}" alt="${food.name}" />

      <div class="food-info">
        <div class="card-header">
          <h3>${food.name}</h3>
          <p class="price">${food.price} ETB</p>
          <span>${food.type}</span>
        </div>

        <span class="stars">${buildStars(food.rating)}</span>

        <p>${food.description}</p>

        <div class="add-section">
          <div class="item-quantity">
            <button class="dec-qty">-</button>
            <div class="qty-display">0</div>
            <button class="inc-qty">+</button>
          </div>
          <button onclick="alert('Order Added')">Add Order</button>
        </div>
      </div>
    </div>
  `;
}

// ── Render ─────────────────────────────────────────────────────────────────

function renderMenu() {
  const container = document.getElementById("menu-container");

  // Get unique categories in the order they appear in the array
  const categories = [...new Set(foods.map((f) => f.category))];

  // Category display names
  const categoryTitles = {
    Ethiopian: "Ethiopian Favorites",
    International: "International Cuisine",
    Drinks: "Drinks",
  };

  categories.forEach((category) => {
    const items = foods.filter((f) => f.category === category);

    const section = document.createElement("section");
    section.className = "menu-section";

    section.innerHTML = `
      <h2>${categoryTitles[category] || category}</h2>
      <div class="food-grid">
        ${items.map(createFoodCard).join("")}
      </div>
    `;

    container.appendChild(section);
  });
}

renderMenu();