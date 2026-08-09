const cartBtn = document.getElementById("cart-btn");
const cartDialog = document.getElementById("cart-dialog");
const closeCartBtn = document.getElementById("close-cart");
const closeSummeryBtn = document.getElementById("close-summery");
const cancelOrderBtn=document.getElementById("cancel");
const cartPopup=document.getElementById("cart");
const confirmDialog=document.getElementById("confirm-dialog");

const ordersBtn = document.getElementById("orders-btn");
const ordersPopup = document.getElementById("orders-popup");
const closeOrders = document.getElementById("close-orders");



cartBtn.addEventListener("click", () => {
  renderCart();
  cartDialog.classList.add("open");
  cartPopup.classList.add("open")
});

closeCartBtn.addEventListener("click", () => {
  cartDialog.classList.remove("open");
  cartPopup.classList.remove("open");
  confirmDialog.classList.remove("open");
});

closeSummeryBtn.addEventListener("click", () => {
  cartDialog.classList.remove("open");
  cartPopup.classList.remove("open");
  confirmDialog.classList.remove("open");
});

cancelOrderBtn.addEventListener("click",()=>{
  cartDialog.classList.remove("open");
  cartPopup.classList.remove("open");
  confirmDialog.classList.remove("open");
})




ordersBtn.addEventListener("click", () => {
    ordersPopup.style.display = "flex";
    loadOrders();
});

closeOrders.addEventListener("click", () => {
    ordersPopup.style.display = "none";
});