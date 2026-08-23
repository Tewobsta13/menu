
document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("admin_token");
  if (!token) {
    window.location.href = "/admin/login";
    return;
  }

  // Logout Action
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      localStorage.removeItem("admin_token");
      document.cookie =
        "admin_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      window.location.href = "/admin/login";
    });
  }

  // 1. Cancel Order Action
  const cancelButtons = document.querySelectorAll(".btn-cancel");
  cancelButtons.forEach((button) => {
    button.addEventListener("click", async (e) => {
      const orderId = e.target.getAttribute("data-id");

      if (!confirm(`Are you sure you want to cancel Order #${orderId}?`)) {
        return;
      }

      try {
        const response = await fetch(`/admin/orders/${orderId}/cancel`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message || "Order cancelled successfully!");
          // Update status text in UI or refresh page
          window.location.reload();
        } else {
          alert(result.error || "Failed to cancel order.");
        }
      } catch (error) {
        console.error("Error cancelling order:", error);
        alert("Server error occurred while cancelling order.");
      }
    });
  });

  // 2. Delete Order Action
  const deleteButtons = document.querySelectorAll(".btn-delete");
  deleteButtons.forEach((button) => {
    button.addEventListener("click", async (e) => {
      const orderId = e.target.getAttribute("data-id");

      if (
        !confirm(
          `Are you sure you want to permanently delete Order #${orderId}?`,
        )
      ) {
        return;
      }

      try {
        const response = await fetch(`/admin/orders/${orderId}/delete`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        const result = await response.json();

        if (response.ok) {
          alert(result.message || "Order deleted successfully!");
          // Remove row from table directly
          const row = document.getElementById(`order-row-${orderId}`);
          if (row) {
            row.remove();
          } else {
            window.location.reload();
          }
        } else {
          alert(result.error || "Failed to delete order.");
        }
      } catch (error) {
        console.error("Error deleting order:", error);
        alert("Server error occurred while deleting order.");
      }
    });
  });

  // 3. Admin Add Order Form Submission (/admin/add)
  const adminAddForm = document.getElementById("admin-add-order-form");
  if (adminAddForm) {
    adminAddForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const customer = document.getElementById("customer_name").value.trim();
      const items = document.getElementById("order_items").value.trim();
      const quantity = parseInt(
        document.getElementById("order_quantity").value,
        10,
      );
      const totalPrice = parseFloat(
        document.getElementById("total_price").value,
      );

      if (
        !customer ||
        !items ||
        isNaN(quantity) ||
        quantity <= 0 ||
        isNaN(totalPrice) ||
        totalPrice <= 0
      ) {
        alert("Please fill in all fields with valid data.");
        return;
      }

      const payload = {
        customer: customer,
        items: items,
        quantity: quantity,
        total_price: totalPrice,
      };

      try {
        const response = await fetch("/admin/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (response.ok) {
          alert("New order added successfully!");
          window.location.href = "/admin/orders";
        } else {
          alert(result.error || "Failed to add order.");
        }
      } catch (error) {
        console.error("Error adding order:", error);
        alert("Server error occurred while saving order.");
      }
    });
  }
});
