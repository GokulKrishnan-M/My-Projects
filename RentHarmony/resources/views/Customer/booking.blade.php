@extends('Layouts.CustomerMaster')

@section('content')
<style>
    
  body {
    background: #f6f8fb; /* Soft light background */
  }
  .booking-card, .payment-card {
    background: #f7f8f8ff;
    border-radius: 15px;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.08);
    transition: transform 0.2s ease-in-out;
  }
  .booking-card:hover, .payment-card:hover {
    transform: translateY(-3px);
  }
  .form-control {
    border-radius: 10px;
    padding: 10px;
    font-size: 0.95rem;
  }
  label {
    font-weight: 600;
    color: #444;
    margin-bottom: 4px;
  }
  .card-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #222;
  }
  .btn-primary {
    background: #4e73df;
    border: none;
    font-weight: bold;
    transition: background 0.2s;
  }
  .btn-primary:hover {
    background: #3756c0;
  }
  .total-section {
    font-size: 1.1rem;
    font-weight: bold;
    color: #333;
  }
</style>

<div class="container py-4">
  <div class="row g-4 justify-content-center">
    
    <!-- Left: Product Booking -->
    <div class="col-md-6">
      <div class="card booking-card p-3">
        <img src="{{ asset('uploads/'.$products->image) }}" 
             class="card-img-top rounded-3" 
             alt="Product Image" 
             style="height:250px;width:800px; object-fit:cover;">
        <div class="card-body">
          <h5 class="card-title text-center">{{ $products->productname }}</h5>
          <form action="{{route('booking_payment_insert')}}" method="POST">
            @csrf

            <p class="text-muted text-center mb-2">
              <strong>Price per day:</strong> ₹{{ $products->ppd }}
            </p>

            @if($products->stock > 0)
              <p class="text-success fw-bold text-center">🟢 Available</p>
            @else
              <p class="text-danger fw-bold text-center">🔴 Unavailable</p>
            @endif

            <input type="hidden" id="price_per_day_value" value="{{ $products->ppd }}">
            <input type="hidden" id="productid" name="instid" value="{{ $products->instid }}">

            <div class="form-group mb-3" style="margin-left:30px;">
              <label>Required Date</label>
              <input type="date" name="startdate" class="form-control" id="required_date" required>
            </div>

            <div class="form-group mb-3" style="margin-left:30px;">
              <label>Return Date</label>
              <input type="date" name="returndate" class="form-control" id="return_date" required>
            </div>

            <div class="form-group mb-8" style="margin-left:30px;">
              <label>Quantity</label>
              <input type="number" name="quantity" class="form-control" id="quantity" min="1" max="{{ $products->stock }}" value="1" required>
            </div>

            <div class="form-group" style="margin-left:30px;">
              <label>Total Amount</label>
              <input type="text" name="totalamnt" class="form-control" id="total_amount" readonly>
            </div>
        </div>
      </div>
    </div>

    <!-- Right: Payment Form -->
    <div class="col-md-6">
      <div class="card payment-card p-4">
        <h4 class="mb-3 text-center">💳 Payment Details</h4>
        <p class="text-muted text-center mb-4">Complete your booking by providing payment details</p>

        {{-- Hidden fields for totals --}}
        <input type="hidden" name="subtotal" id="subtotal_input">
        <input type="hidden" name="vat" id="vat_input">
        <input type="hidden" name="grand_total" id="grand_total_input">

        <div class="form-group mb-3" style="margin-left:30px;">
          <label>Email address</label>
          <input type="email" class="form-control" name="email" placeholder="you@example.com" required>
        </div>

        <div class="form-group mb-1">
          <label>Card details</label>
          <div class="d-flex gap-2">
            <input type="text" class="form-control" placeholder="Card Number" required pattern="[0-9]{16}" title="Enter valid 16-digit credit card number(no spaces)">
            <input type="text" class="form-control" placeholder="MM/YY" required pattern="^(0[1-9]|1[0-2])\/\d{2}$" title="Enter expiry date in MM/YY format(eg.05/28)">
            <input type="text" class="form-control" placeholder="CVV" required pattern="[0-9]{3}" title="Enter valid 3 or 4 digit cvv">
          </div>
        </div>

        <div class="form-group mb-3" style="margin-left:30px;">
          <label>Cardholder name</label>
          <input type="text" class="form-control" name="cardholder" placeholder="Name" required>
        </div>

        <div class="form-group mb-3" style="margin-left:30px;">
          <label>Billing address</label>
          <select class="form-control mb-2" name="country" required>
            <option value="">Select Country</option>
            <option value="India">India</option>
            <option value="US">United States</option>
            <option value="UK">United Kingdom</option>
          </select>
          <div class="d-flex gap-2">
            <input type="text" class="form-control" name="zip" placeholder="ZIP" required>
            <input type="text" class="form-control" name="state" placeholder="State" required>
          </div>
        </div>

        <hr>
        <div class="d-flex justify-content-between total-section mb-2">
          <span>Total</span> 
          <strong id="grand_total_text">₹0</strong>
        </div>

       <center><button type="submit" class="btn btn-primary btn-block mt-2" style="border-radius: 30px;" id="pay_button">
          Pay ₹0
        </button></center> 
      </form>

      @if(session('success'))
        <script>alert('{{session('success')}}');</script>
      @endif
      </div>
    </div>
  </div>
</div>

<script>
(function () {
  const priceEl = document.getElementById('price_per_day_value');
  const reqEl = document.getElementById('required_date');
  const retEl = document.getElementById('return_date');
  const qtyEl = document.getElementById('quantity');
  const totalEl = document.getElementById('total_amount');

  const grandText = document.getElementById('grand_total_text');
  const payBtn = document.getElementById('pay_button');
  const grandInput = document.getElementById('grand_total_input');

  function formatINR(n) {
    return '₹' + (n || 0).toLocaleString('en-IN', { maximumFractionDigits: 2, minimumFractionDigits: 2 });
  }

  function isValidDate(d) {
    return d instanceof Date && !isNaN(d.getTime());
  }

  function syncReturnMin() {
    if (reqEl.value) {
      retEl.min = reqEl.value;
      if (retEl.value && retEl.value < reqEl.value) {
        retEl.value = reqEl.value;
      }
    }
  }

  function calculateTotal() {
    const price = parseFloat(priceEl.value) || 0;
    const reqVal = reqEl.value;
    const retVal = retEl.value;
    const qty = parseInt(qtyEl.value, 10) || 1;

    if (!reqVal || !retVal) {
      totalEl.value = '';
      updateBill(0);
      return;
    }

    const reqDate = new Date(reqVal + 'T00:00:00');
    const retDate = new Date(retVal + 'T00:00:00');

    if (!isValidDate(reqDate) || !isValidDate(retDate) || retDate < reqDate) {
      totalEl.value = '';
      updateBill(0);
      return;
    }

    const msPerDay = 24 * 60 * 60 * 1000;
    let days = Math.round((retDate - reqDate) / msPerDay);
    if (days === 0) days = 1;

    const total = price * days * qty;
    totalEl.value = total.toFixed(2);
    updateBill(total);
  }

  function updateBill(total) {
    grandText.textContent = formatINR(total);
    payBtn.textContent = 'Pay ' + formatINR(total);
    grandInput.value = total.toFixed(2);
  }

  reqEl.addEventListener('change', () => { syncReturnMin(); calculateTotal(); });
  retEl.addEventListener('change', calculateTotal);
  qtyEl.addEventListener('input', calculateTotal);

  syncReturnMin();
  calculateTotal();
})();
</script>


@endsection
