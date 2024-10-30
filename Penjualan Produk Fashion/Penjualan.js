function submitOrder() {
    
    const name = document.getElementById('name').value;
    const product = document.getElementById('product').value;
    const quantity = document.getElementById('quantity').value;

    document.getElementById('popup-name').innerText = name;
    document.getElementById('popup-product').innerText = product;
    document.getElementById('popup-quantity').innerText = quantity;

    document.getElementById('popup').style.display = 'block';
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
}

function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    if (username === "untag" && password === "1234") {
        document.getElementById("loginMessage").innerText = "Login successful!";
        document.getElementById("loginMessage").style.color = "green";
        window.location.href = "http://127.0.0.1:3000/Penjualan.html";
    } else {
        document.getElementById("loginMessage").innerText = "Invalid username or password!";
    }

    return false;
}
