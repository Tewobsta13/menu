const cartBtn = document.getElementById("cart-btn");
const cartDialog = document.getElementById("cart-dialog");
const closeCartBtn = document.getElementById("close-cart");
const closeSummeryBtn = document.getElementById("close-summery");
const cancelOrderBtn=document.getElementById("cancel");
const cartPopup=document.getElementById("cart");
const confirmDialog=document.getElementById("confirm-dialog");

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
