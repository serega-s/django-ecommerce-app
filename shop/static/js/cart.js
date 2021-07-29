const updateBtns = document.getElementsByClassName("update-cart")
const inputQuantity = document.querySelector("#inputQuantity")

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function (e) {
    const productId = this.dataset.product
    const action = this.dataset.action

    let quantity = 0
    inputQuantity ? (quantity = parseInt(inputQuantity.value)) : (quantity = 1)

    console.log("productId:", productId, "Action:", action)
    console.log("USER:", user)

    user === "AnonymousUser"
      ? addCookieItem(productId, action, quantity)
      : updateUserOrder(productId, action, quantity)
  })
}

function updateUserOrder(productId, action, quantity) {
  console.log("User is authenticated. Sending data...")

  const url = "/update_item/"

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
      quantity: quantity
    }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      location.reload()
    })
    .catch((error) => {
      console.log(error)
    })
}

function addCookieItem(productId, action, quantity) {

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: quantity }
    } else {
      inputQuantity
        ? (cart[productId]["quantity"] += parseInt(inputQuantity.value))
        : (cart[productId]["quantity"] += 1)
    }
  }
  if (action === "remove") {
    cart[productId]["quantity"] -= 1

    if (cart[productId]["quantity"] <= 0) {
      console.log("Item deleted")
      delete cart[productId]
    }
  }
  console.log("CART:", cart)

  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}
