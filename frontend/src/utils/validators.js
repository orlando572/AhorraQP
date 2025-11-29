export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validateSearchQuery = (query) => {
  return query && query.trim().length >= 2
}

export const validateQuantity = (quantity) => {
  return Number.isInteger(quantity) && quantity > 0
}

export const validatePrice = (price) => {
  const numPrice = parseFloat(price)
  return !isNaN(numPrice) && numPrice >= 0
}