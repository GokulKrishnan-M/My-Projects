<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Rental Request View</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #eef2f7; font-family: 'Segoe UI', sans-serif; }
    .card { border-radius: 1rem; border: none; }
    .rental-img {
      border-radius: 1rem;
      height: 100%;
      max-height: 400px;
      object-fit: cover;
      width: 100%;
      box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    .btn-custom {
      background: linear-gradient(90deg, #0d6efd, #0dcaf0);
      border: none;
      color: white;
      border-radius: 0.7rem;
      font-weight: 500;
      box-shadow: 0 4px 10px rgba(13,110,253,0.3);
      transition: transform 0.2s ease-in-out;
    }
    .btn-custom:hover {
      opacity: 0.9;
      transform: scale(1.05);
    }
    .list-group-item { border: none; padding: 0.8rem 1rem; }
    .badge-status {
      font-size: 0.9rem;
      padding: 0.5em 1em;
      border-radius: 0.5rem;
    }
    .badge-booked { background: #ffc107; color: #000; }
    .badge-return { background: #198754; }
  </style>
</head>
<body>

<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-lg-9">

      <div class="card shadow-lg p-4">
        <div class="row g-4 align-items-center">
          
          <!-- Left: Image -->
          <div class="col-md-5">
            <img src="<?php echo e(asset('uploads/'.$booking->inst->image)); ?>" class="rental-img" alt="Rental Item">
          </div>

          <!-- Right: Rental Details -->
          <div class="col-md-7">
            <h3 class="mb-4 text-primary fw-bold">Rental Request Details</h3>
            
            <ul class="list-group list-group-flush mb-4">
              <li class="list-group-item"><strong>📦 Item:</strong> <?php echo e($booking->inst->instname); ?></li>
              <li class="list-group-item"><strong>👤 Customer:</strong> <?php echo e($booking->cust->custname); ?></li>
              <li class="list-group-item">
                <strong>📅 Booking Date:</strong> <?php echo e(date('d-M-Y', strtotime($booking->bookdate))); ?>

              </li>
              <li class="list-group-item">
                <strong>📌 Required Date:</strong> <?php echo e(date('d-M-Y', strtotime($booking->startdate))); ?>

              </li>
              <li class="list-group-item">
                <strong>🔄 Return Date:</strong> <?php echo e(date('d-M-Y', strtotime($booking->returndate))); ?>

              </li>
              <li class="list-group-item"><strong>🔢 Quantity:</strong> <?php echo e($booking->quantity); ?></li>
              <li class="list-group-item"><strong>💰 Paid Amount:</strong> ₹ <?php echo e(number_format($booking->totalamt)); ?></li>
              <li class="list-group-item">
                <strong>📌 Status:</strong>
                <?php if($booking->status == 'Booked'): ?>
                  <span class="badge badge-status badge-booked">Booked</span>
                <?php elseif($booking->status == 'Return'): ?>
                  <span class="badge badge-status badge-return">Returned</span>
                <?php endif; ?>
              </li>

              
              <?php
                  $today = now();
                  $returnDate = \Carbon\Carbon::parse($booking->returndate);
                  $perDayAmount = $booking->inst->ppd ?? 0;
                  $lateDays = 0;
                  $lateFee = 0;

                  if ($today->greaterThan($returnDate) && $booking->status == 'Booked') {
                      $lateDays = $today->diffInDays($returnDate);
                      $lateFee = $lateDays * $perDayAmount;
                  }
              ?>

              <?php if($lateDays > 0): ?>
                <li class="list-group-item text-danger fw-bold">
                  ⏰ Late by: <?php echo e($lateDays); ?> day(s) <br>
                  💸 Late Fee: ₹ <?php echo e(number_format($lateFee)); ?>

                </li>
              <?php endif; ?>
            </ul>

            <div class="d-flex gap-2">
              <form action="<?php echo e(route('returnBooking', $booking->bookid)); ?>" method="POST" class="w-100">
                <?php echo csrf_field(); ?>
                <input type="hidden" name="fineamount" value="<?php echo e($lateFee); ?>">
                <?php if($booking->status == 'Booked'): ?>
                  <button type="submit" class="btn btn-custom w-100">📥 Return Item</button>
                <?php endif; ?>
              </form>
               <?php if(session('success')): ?>
              <script>alert('<?php echo e(session('success')); ?>');</script>
              <?php endif; ?>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
                </div>
                <?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Admin/viewmorebook.blade.php ENDPATH**/ ?>