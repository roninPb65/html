// Dummy product data with images
const products = [
    {
      name: "Smartphone",
      description: "A smartphone with the latest features.",
      image: "https://via.placeholder.com/250x200?text=Smartphone"
    },
    {
      name: "Headphones",
      description: "High-quality wireless headphones.",
      image: "https://via.placeholder.com/250x200?text=Headphones"
    },
    {
      name: "Tablet",
      description: "A tablet for entertainment and work.",
      image: "https://via.placeholder.com/250x200?text=Tablet"
    },
    {
      name: "Smartwatch",
      description: "A smartwatch with health tracking features.",
      image: "https://via.placeholder.com/250x200?text=Smartwatch"
    },
    {
      name: "Charger",
      description: "A fast charger for all your devices.",
      image: "https://via.placeholder.com/250x200?text=Charger"
    }
  ];
  
  // Render product items on the page
  function renderProducts(filteredProducts) {
    const productList = document.getElementById("productList");
    productList.innerHTML = "";
    filteredProducts.forEach(product => {
      const productItem = document.createElement("div");
      productItem.classList.add("product-item");
      productItem.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <h3>${product.name}</h3>
        <p>${product.description}</p>
      `;
      productItem.onclick = () => showDescription(product);
      productList.appendChild(productItem);
    });
  }
  
  // Show description of a selected item in the modal
  function showDescription(product) {
    const modal = document.getElementById("itemDescriptionModal");
    document.getElementById("itemModalTitle").innerText = product.name;
    document.getElementById("itemModalDescription").innerText = product.description;
    modal.style.display = "block";
  }
  
  // Close the description modal
  function closeModal() {
    const modal = document.getElementById("itemDescriptionModal");
    modal.style.display = "none";
  }
  
  // Search Item Function
  function searchItem() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filteredProducts = products.filter(product => product.name.toLowerCase().includes(query));
    renderProducts(filteredProducts);
    document.getElementById('searchMessage').innerText = filteredProducts.length > 0 ? `${filteredProducts.length} item(s) found` : "No items found!";
  }
  
  // Initialize the page with all products
  window.addEventListener('load', () => {
    renderProducts(products);
  });
  
  // Toggle theme (light/dark mode)
  function toggleTheme() {
    const body = document.body;
    const themeButton = document.getElementById("themeButton");
    const themeIcon = document.getElementById("themeIcon");
  
    body.classList.toggle("dark-mode");
  
    if (body.classList.contains("dark-mode")) {
      themeIcon.classList.remove("fa-sun");
      themeIcon.classList.add("fa-moon");
    } else {
      themeIcon.classList.remove("fa-moon");
      themeIcon.classList.add("fa-sun");
    }
  }
  
  // Initialize theme based on user preference
  window.addEventListener('load', () => {
    const body = document.body;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      body.classList.add("dark-mode");
      document.getElementById("themeIcon").classList.remove("fa-sun");
      document.getElementById("themeIcon").classList.add("fa-moon");
    }
  });
  