

const cartBtnContainer = document.getElementById("cart-btn-container");
const cartDialog = document.getElementById("cart-dialog");
const closeCartBtn = document.getElementById("close-cart");

cartBtnContainer.addEventListener("click", () => {
  cartDialog.classList.add("open");
});

closeCartBtn.addEventListener("click", () => {
  cartDialog.classList.remove("open");
});
