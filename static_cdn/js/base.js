$('.formset_row').formset({
    addText: 'Add item',
    deleteText: 'remove',
    prefix: 'invoicelineitem_set'
});

$(document).ready(function() {
  $('[data-behavior="calculate-price-item"]').each(function(index) {
    priceItemChange(this);
  });
});

$(document).on('focusout', '[data-behavior="calculate-quantity-item"]', function(e) {
  quantityItemChange(this);
});

$(document).on('focusout', '[data-behavior="calculate-price-item"]', function(e) {
  priceItemChange(this);
});

function quantityItemChange(element) {
  var qty = $(element).val();
  var price = $(element).closest('.line-item-row').find('[data-behavior="calculate-price-item"]').val();
  var amount = qty * price;
  $(element).closest('.line-item-row').find('[data-behavior="item-amount"]').html('$' + amount);
}

function priceItemChange(element) {
  var qty = $(element).closest('.line-item-row').find('[data-behavior="calculate-quantity-item"]').val();
  var price = $(element).val();
  var amount = qty * price;
  $(element).closest('.line-item-row').find('[data-behavior="item-amount"]').html('$' + amount);
}
