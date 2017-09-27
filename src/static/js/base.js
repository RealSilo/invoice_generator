$('.formset_row').formset({
    addText: 'Add item',
    deleteText: 'remove',
    prefix: 'invoicelineitem_set'
});

$(function () {
  $('.datepicker-date').datepicker({
    format: "yyyy-mm-dd",
    startDate: "0",
    autoclose: 'True',
    onSelect: function(selected) {
      $(".datepicker-due-date").datepicker("option", "minDate", selected)
    }
  });

  $('.datepicker-due-date').datepicker({
    format: "yyyy-mm-dd",
    startDate: "0",
    autoclose: 'True',
    onSelect: function(selected) {
      $(".datepicker-date").datepicker("option", "maxDate", selected)
    }
  });
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

$(document).on('focusout', '[data-behavior="calculate-shipping-price"]', function(e) {
  calculateTotal();
});

$(document).on('focusout', '[data-behavior="calculate-tax"]', function(e) {
  calculateTotal();
});

$(document).on('change', '[data-behavior="calculate-tax-type"]', function(e) {
  calculateTotal();
});

$(document).on('focusout', '[data-behavior="calculate-discount"]', function(e) {
  calculateTotal();
});

$(document).on('change', '[data-behavior="calculate-discount-type"]', function(e) {
  calculateTotal();
});

function quantityItemChange(element) {
  var qty = $(element).val();
  var price = $(element).closest('.line-item-row').find('[data-behavior="calculate-price-item"]').val();
  var amount = qty * price;
  $(element).closest('.line-item-row').find('[data-behavior="item-amount"]').html(amount);
  calculateTotal();
}

function priceItemChange(element) {
  var qty = $(element).closest('.line-item-row').find('[data-behavior="calculate-quantity-item"]').val();
  var price = $(element).val();
  var amount = qty * price;
  $(element).closest('.line-item-row').find('[data-behavior="item-amount"]').html(amount);
  calculateTotal();
}

function calculateSubtotal() {
  var subtotal = 0;
  $('[data-behavior="item-amount"]').each(function(index) {
    subtotal += parseInt($(this).html());
  });
  $('.subtotal-price').html(subtotal);
}

function calculateTotal() {
  calculateSubtotal();
  var total = $('.subtotal-price').html();
  var discount = parseInt($('.discount-value').val());
  var discountType = $('.discount-type').val();
  var tax = parseInt($('.tax-value').val());
  var taxType = $('.tax-type').val();
  var shippingPrice = parseInt($('.shipping-price').val());

  if (discountType === '%') {
    total = Math.round(total - total * discount / 100)
  } else if (discountType === '$') {
    total -= discount
  }

  if (taxType === '%') {
    total = Math.round(total + total * tax / 100)
  } else if (discountType === '$') {
    total += discount
  }

  if (shippingPrice > 0) {
    total += shippingPrice
  }

  $('.total-price').html(total);
}
