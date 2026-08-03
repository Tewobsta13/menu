const sortByPrice = function(arr){
 return [...arr].sort((a, b) => a.price - b.price);
}




const foods = [
  {
    name: "Burger",
    price: 250,
    description: "Juicy beef burger with cheese, lettuce, and tomato."
  },
  {
    name: "Pizza",
    price: 450,
    description: "Delicious cheese pizza topped with fresh vegetables."
  },
  {
    name: "Pasta",
    price: 320,
    description: "Creamy Alfredo pasta served with grilled chicken."
  },
  {
    name: "Fried Chicken",
    price: 300,
    description: "Crispy fried chicken served with French fries."
  },
  {
    name: "Caesar Salad",
    price: 180,
    description: "Fresh lettuce with Caesar dressing, croutons, and parmesan cheese."
  },
  {
    name: "Sandwich",
    price: 150,
    description: "Freshly prepared sandwich with vegetables and grilled chicken."
  }
];


const sorted = sortByPrice(foods);

console.log(sorted);