const API_BASE_URL = 'http://localhost:8000';
const carsContainer = document.getElementById('cars-container');
const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const carCardTemplate = document.getElementById('car-card-template');

async function fetchCars(endpoint = '/cars') {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);
    if (!response.ok) {
      throw new Error('Erro ao buscar carros');
    }
    return await response.json();
  } catch (error) {
    console.error(error);
    showErrorMessage('Não foi possível carregar os carros.');
    return [];
  }
}

function renderCars(cars) {
  carsContainer.innerHTML = '';

  if (!cars.length) {
    carsContainer.innerHTML = '<p class="empty-state">Nenhum carro encontrado.</p>';
    return;
  }

  cars.forEach(car => {
    const card = carCardTemplate.content.cloneNode(true);
    const image = card.querySelector('.car-image');
    image.src = car.imagem || 'https://via.placeholder.com/300x180?text=Carro';
    image.alt = `Imagem do ${car.modelo}`;

    card.querySelector('.car-model').textContent = `${car.modelo}`;
    card.querySelector('.car-brand').textContent = `Marca: ${car.marca}`;
    card.querySelector('.car-year').textContent = `Ano: ${car.ano}`;
    const precoFormatado = Number(car.preco || 0).toLocaleString('pt-BR', {
      minimumFractionDigits: 2
    });
    card.querySelector('.car-price').textContent = `Preço: R$ ${precoFormatado}`;
    card.querySelector('.car-description').textContent = car.descricao || 'Sem descrição disponível.';

    carsContainer.appendChild(card);
  });
}

function showErrorMessage(message) {
  carsContainer.innerHTML = `<p class="error-message">${message}</p>`;
}

async function handleSearch() {
  const query = searchInput.value.trim();
  const endpoint = query ? `/cars/search?query=${encodeURIComponent(query)}` : '/cars';
  const cars = await fetchCars(endpoint);
  renderCars(cars);
}

searchButton.addEventListener('click', handleSearch);
searchInput.addEventListener('keypress', event => {
  if (event.key === 'Enter') {
    handleSearch();
  }
});

window.addEventListener('DOMContentLoaded', handleSearch);
