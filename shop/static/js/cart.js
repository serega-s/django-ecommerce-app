const updateBtns = document.getElementsByClassName("update-cart")

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function (e) {
    const productId = this.dataset.product
    const action = this.dataset.action

    console.log("productId:", productId, "Action:", action)
    console.log("USER:", user)

    user === "AnonymousUser"
      ? addCookieItem(productId, action)
      : updateUserOrder(productId, action)
  })
}

function updateUserOrder(productId, action) {
  console.log("User is authenticated. Sending data...")

  const url = "/update_item/"

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
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

function addCookieItem(productId, action) {
  const inputQuantity = document.querySelector("#inputQuantity")
  let value = 0
  inputQuantity ? (value = parseInt(inputQuantity.value)) : (value = 1)

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: value }
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
