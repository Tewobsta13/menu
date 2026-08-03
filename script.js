// sort method
const sortByPrice = function (arr) {
  return [...arr].sort((a, b) => a.price - b.price);
};

var cart = [];

// =====================
//  CART LOGIC
// =====================

function addToCart(foodId) {
  var food = null;
  for (var i = 0; i < foods.length; i++) {
    if (foods[i].id == foodId) {
      food = foods[i];
    }
  }
  if (!food) return;

  var found = false;
  for (var j = 0; j < cart.length; j++) {
    if (cart[j].id == foodId) {
      cart[j].quantity += 1;
      found = true;
      break;
    }
  }

  if (!found) {
    cart.push({
      id: food.id,
      name: food.name,
      price: food.price,
      quantity: 1,
    });
  }

  updateCartBadge();
  renderCart();

  
  var btn = document.querySelector(
    `.add-section button[onclick="addToCart(${food.id})"]`
  );
  if (btn) {
    var original = btn.textContent;
    btn.textContent = "✓ Added!";
    alert("Order Added!");
    btn.style.background = "var(--green)";
    setTimeout(function () {
      btn.textContent = original;
      btn.style.background = "";
    }, 800);
  }
}

function changeQuantity(foodId, delta) {
  for (var i = 0; i < cart.length; i++) {
    if (cart[i].id == foodId) {
      cart[i].quantity += delta;
      if (cart[i].quantity <= 0) {
        cart.splice(i, 1);
      }
      break;
    }
  }
  updateCartBadge();
  renderCart();
}

function removeFromCart(foodId) {
  cart = cart.filter(function (item) {
    return item.id !== foodId;
  });
  updateCartBadge();
  renderCart();
}

function updateCartBadge() {
  var badge = document.getElementById("cart-count");
  var total = cart.reduce(function (sum, item) {
    return sum + item.quantity;
  }, 0);

  badge.textContent = total;
  if (total > 0) {
    badge.classList.remove("hidden");
  } else {
    badge.classList.add("hidden");
  }
}

function renderCart() {
  var container = document.getElementById("cart-items");
  var totalEl = document.getElementById("cart-total");

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="cart-empty">
        <p>Your cart is empty</p>
        <small>Add a food from the menu!</small>
      </div>
    `;
    totalEl.innerHTML = "Total: <strong>0 ETB</strong>";
    return;
  }

  var grandTotal = 0;
  var html = "";

  cart.map( (item)=> {
    var subtotal = item.price * item.quantity;
    grandTotal += subtotal;
    html += `
      <div class="cart-item-row">
        <div class="cart-item-name">
          <h3>${item.name}</h3>
          <p class="cart-item-subtotal">${subtotal} ETB</p>
        </div>
        <div class="cart-item-price">${item.price} ETB</div>
        <div class="item-quantity">
          <button onclick="changeQuantity(${item.id}, -1)">−</button>
          <span class="qty-display">${item.quantity}</span>
          <button onclick="changeQuantity(${item.id}, 1)">+</button>
        </div>
        <button class="delete-btn" onclick="removeFromCart(${item.id})">
          <i class="fa-solid fa-trash-can"></i>
        </button>
      </div>
    `;
  });

  container.innerHTML = html;
  totalEl.innerHTML = `Total: <strong>${grandTotal} ETB</strong>`;
}

// rendering menu

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
          <button onclick="addToCart(${food.id})">Add Order</button>
        </div>
      </div>
    </div>
  `;
}

function renderMenu() {
  const container = document.getElementById("menu-container");

  const categories = [...new Set(foods.map((f) => f.category))];

  // category names
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