function createCartItem(title, price, quantity = 1) {

  const addToCart = {
    title: title,
    price: price,
    quantity: quantity,
  };

 
  const existingItem = added.find(
    (item) => item.title === addToCart.title && item.price === addToCart.price,
  );

  if (existingItem) {
    
    existingItem.quantity += addToCart.quantity;
  } else {

    added.push(addToCart);
  }

  return added;
}
