const checkoutBtn = document.getElementById("checkout-btn");
const order = document.getElementById("order");

// sort method
const sortByPrice = function (arr) {
  return [...arr].sort((a, b) => a.price - b.price);
};

let cart = [];
let foods = [];

//  CART LOGIC

function addToCart(foodId) {
  let food = null;
  for (let i = 0; i < foods.length; i++) {
    if (foods[i].id == foodId) {
      food = foods[i];
    }
  }
  if (!food) return;
  let found = false;
  for (let j = 0; j < cart.length; j++) {
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

  let btn = document.querySelector(
    `.add-section button[onclick="addToCart(${food.id})"]`,
  );
  if (btn) {
    let original = btn.textContent;
    btn.textContent = "✓ Added!";
    handleNotificationTrigger(`${food.name} added to your cart`, true);
    btn.style.background = "var(--green)";
    setTimeout(function () {
      btn.textContent = original;
      btn.style.background = "";
    }, 800);
  }
}

function changeQuantity(foodId, delta) {
  for (let i = 0; i < cart.length; i++) {
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
  cart = cart.filter((item) => {
    return item.id !== foodId;
  });
  updateCartBadge();
  renderCart();
}

function updateCartBadge() {
  let badge = document.getElementById("cart-count");
  let total = cart.reduce(function (sum, item) {
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
  let container = document.getElementById("cart-items");
  let totalEl = document.getElementById("cart-total");

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

  let grandTotal = 0;
  let html = "";

  cart.map((item) => {
    let subtotal = item.price * item.quantity;
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

function renderMenu(category = "All") {
  const container = document.getElementById("menu-container");

  container.innerHTML = "";

  const categories =
    category === "All"
      ? [...new Set(foods.map((f) => f.category))]
      : [category];

  const categoryTitles = {
    Ethiopian: "Ethiopian Favorites",
    International: "International Cuisine",
    Drinks: "Drinks",
  };

  categories.forEach((category) => {
    const items = foods.filter((food) => food.category === category);

    const section = document.createElement("section");

    section.className = "menu-section";

    section.innerHTML = `
      <h2>${categoryTitles[category]}</h2>

      <div class="food-grid">
        ${items.map(createFoodCard).join("")}
      </div>
    `;

    container.appendChild(section);
  });
}
function filterMenu(category) {
  renderMenu(category);
}

//Confierm Dialog
const renderSummery = () => {
  const summery = document.getElementById("checkout-list");
  const totalSummery = document.getElementById("summery-total");
  let totalPrice = 0;
  totalSummery.innerHTML = "0 ETB";

  summery.innerHTML = "";
  cart.forEach((item) => {
    const summeryItem = document.createElement("div");
    summeryItem.classList.add("summery-item");
    summeryItem.innerHTML = `
    <h5>${item.name}</h5>
    <p>${item.price + " "}<i class="fa-solid fa-xmark"></i>${" " + item.quantity}</p>
    <p>${item.price * item.quantity} ETB</p>
    `;
    totalPrice += item.price * item.quantity;
    console.log(totalPrice);

    summery.appendChild(summeryItem);
  });
  console.log(totalPrice);

  totalSummery.innerHTML = totalPrice + " ETB";
};

checkoutBtn.addEventListener("click", () => {
  cartPopup.classList.remove("open");
  confirmDialog.classList.add("open");
  renderSummery();
});
order.addEventListener("click", async () => {
  cartDialog.classList.remove("open");
  cartPopup.classList.remove("open");
  confirmDialog.classList.remove("open");
  if (cart.length <= 0) {
    handleNotificationTrigger("You have zero items in the cart", false);
    return;
  }
  try {
    const response = await fetch("/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(cart),
    });
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    const savedOrder = await response.json();
    console.log("Order saved:", savedOrder);
    cart = [];
    updateCartBadge();
    renderCart();
    handleNotificationTrigger(`Your order was placed! ID: ${savedOrder.order_id}`, true);
  } catch (error) {
    console.error("Could not place order:", error);
    handleNotificationTrigger("Could not place your order", false);
  }

  // else {
  //   cart = [];
  //   handleNotificationTrigger("Your ordered successfully", true);
  // }
});

//NOtification trigger

function handleNotificationTrigger(message, isSuccess) {
  const notification = document.getElementById("notification");

  notification.innerHTML = "";
  notification.innerHTML = message;
  if (isSuccess) {
    notification.classList.add("success");
  } else {
    notification.classList.add("error");
  }
  notification.classList.add("open");

  setTimeout(() => {
    notification.classList.remove("open");
    notification.classList.remove("error");
    notification.classList.remove("success");
  }, 2000);
}

const searchOrderBtn = document.getElementById("search-order-btn");
if (searchOrderBtn) {
  searchOrderBtn.addEventListener("click", async () => {
    const orderIdInput = document.getElementById("order-id-input").value.trim();
    if (!orderIdInput) {
        handleNotificationTrigger("Please enter an Order ID", false);
        return;
    }

    const container = document.getElementById("orders-container");
    container.innerHTML = "<p>Loading...</p>";

    try {
      const response = await fetch(`/orders/${orderIdInput}`);

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status}`);
      }

      const order = await response.json();
      console.log("Order:", order);

      container.innerHTML = `
        <div class="summery-item" style="display:flex; flex-direction:column; gap: 10px; align-items: stretch; border: 1px solid #eee; padding: 15px; border-radius: 15px; background: #fafafa;">
            <div style="display:flex; justify-content: space-between; align-items: center;">
                <h5 style="font-size: 1.1rem; margin: 0;">Order #${order.order_id}</h5>
                <span style="background: var(--dark); color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.8rem;">${order.status}</span>
            </div>
            <p style="text-align: left; margin: 0; font-size: 0.85rem; color: #666;">Date: ${order.date_time}</p>
            
            <div style="margin-top: 10px;">
                ${order.order_items.map(item => `
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.95rem;">
                        <span>${item.quantity}x ${item.item}</span>
                        <span style="font-weight: 600;">${item.total_price} ETB</span>
                    </div>
                `).join('')}
            </div>
            
            <hr style="border: 0; border-top: 1px solid #ddd; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong style="font-size: 1.1rem;">Total</strong>
                <strong style="font-size: 1.1rem; color: var(--green);">${order.order_total} ETB</strong>
            </div>
        </div>
      `;
    } catch (error) {
      console.error("Could not load order:", error);
      container.innerHTML = `<p style="color:var(--red);">Order not found or an error occurred.</p>`;
    }
  });
}

fetch("/foods")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`http Error : ${response.status}`);
    }

    return response.json();
  })
  .then((data) => {
    foods = data;
    renderMenu();
  })
  .catch((error) => {
    console.error("can not load the food ", error);
  });
