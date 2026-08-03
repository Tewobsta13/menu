
let cart = [];
const cartBtn = document.getElementById("cart-btn");
const cartDialog = document.getElementById("cart-dialog");
const closeCartBtn = document.getElementById("close-cart");

cartBtn.addEventListener("click", () => {
  cartDialog.classList.add("open");
});

closeCartBtn.addEventListener("click", () => {
  cartDialog.classList.remove("open");
});
