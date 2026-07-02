<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Welcome to Musical Instrument Rental System</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f9f9f9;
      color: #333;
      padding: 20px;
    }
    .container {
      max-width: 600px;
      background: #fff;
      padding: 25px;
      margin: auto;
      border-radius: 10px;
      box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    h1 {
      color: #4CAF50;
    }
    .footer {
      margin-top: 20px;
      font-size: 13px;
      color: #777;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome, <?php echo e($customer->custname); ?>!</h1>
    <p>Thank you for registering with <strong>Musical Instrument Rental System</strong>. 🎶</p>
    
    <p>We’re excited to have you on board! Now you can:</p>
    <ul>
      <li>Browse a wide range of musical instruments</li>
      <li>Rent instruments easily and affordably</li>
      <li>Manage your bookings anytime</li>
      <li>Stay updated with our latest offers</li>
    </ul>
     <p>Here are your account details:</p>
    <div class="details">
      <p><strong>Name:</strong> <?php echo e($customer->custname); ?></p>
      <p><strong>Username:</strong> <?php echo e($customer->username); ?></p>
      <p><strong>Password:</strong> <?php echo e($customer->password); ?></p>
    </div>
    
    <p>If you have any questions, our support team is always here to help you.</p>
    <p><strong>Happy Playing! 🎸🥁🎹</strong></p>
    
    <div class="footer">
      &copy; <?php echo e(date('Y')); ?> Musical Instrument Rental System. All rights reserved.
    </div>
  </div>
</body>
</html><?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/Guest/email/customermail.blade.php ENDPATH**/ ?>