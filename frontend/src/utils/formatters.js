export const formatPrice = (price) => {
  return parseFloat(price).toFixed(2)
}

export const formatCurrency = (amount) => {
  return `S/ ${formatPrice(amount)}`
}

export const formatProductName = (name) => {
  if (!name) return ''
  return name.charAt(0).toUpperCase() + name.slice(1)
}

export const truncateText = (text, maxLength = 50) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}