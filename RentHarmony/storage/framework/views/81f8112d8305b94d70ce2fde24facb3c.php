<!doctype html>
<html lang="en">

  <head>
    <title>RentHarmony &mdash; Rent a music</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="<?php echo e(asset('guest/fonts/icomoon/style.css')); ?>">

    <link rel="stylesheet" href="<?php echo e(asset('guest/css/bootstrap.min.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('guest/css/bootstrap-datepicker.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('guest/css/jquery.fancybox.min.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('guest/css/owl.carousel.min.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('guest/css/owl.theme.default.min.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('guest/fonts/flaticon/font/flaticon.css')); ?>">
    <link rel="stylesheet" href="<?php echo e(asset('guest/css/aos.css')); ?>">

    <!-- MAIN CSS -->
    <link rel="stylesheet" href="<?php echo e(asset('guest/css/style.css')); ?>">

  </head>

  <body>

    
    <div class="site-wrap" id="home-section">

      <div class="site-mobile-menu site-navbar-target">
        <div class="site-mobile-menu-header">
          <div class="site-mobile-menu-close mt-3">
            <span class="icon-close2 js-menu-toggle"></span>
          </div>
        </div>
        <div class="site-mobile-menu-body"></div>
      </div>



      <header class="site-navbar site-navbar-target" role="banner">

        <div class="container">
          <div class="row align-items-center position-relative">

            <div class="col-3">
              <div class="site-logo">
                <a href="index.html"><strong>RentHarmony</strong></a>
              </div>
            </div>

            <div class="col-9  text-right">
              
              <span class="d-inline-block d-lg-none"><a href="#" class=" site-menu-toggle js-menu-toggle py-5 "><span class="icon-menu h3 text-black"></span></a></span>

              <nav class="site-navigation text-right ml-auto d-none d-lg-block" role="navigation" >
                <ul class="site-menu main-menu js-clone-nav ml-auto " >
                  <li class="active"><a href="<?php echo e(route('guestview')); ?>" class="nav-link" style="color:white;">Home</a></li>
                  <li class="active"><a href="<?php echo e(route('customer')); ?>" class="nav-link" style="color:white;">Register</a></li>
                  <li class="active"><a href="<?php echo e(route('customerlogin')); ?>" class="nav-link" style="color:white;">Login</a></li>
                </ul>
              </nav>
            </div>

            
          </div>
        </div>

      </header>
    <?php echo $__env->yieldContent('content'); ?>
      
      


      
      <footer class="site-footer">
        <div class="container">
          <div class="row">
            <div class="col-lg-3">
              <h2 class="footer-heading mb-4">About Us</h2>
              <p>Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. </p>
              <ul class="list-unstyled social">
                <li><a href="#"><span class="icon-facebook"></span></a></li>
                <li><a href="#"><span class="icon-instagram"></span></a></li>
                <li><a href="#"><span class="icon-twitter"></span></a></li>
                <li><a href="#"><span class="icon-linkedin"></span></a></li>
              </ul>
            </div>
            <div class="col-lg-8 ml-auto">
              <div class="row">
                <div class="col-lg-3">
                  <h2 class="footer-heading mb-4">Quick Links</h2>
                  <ul class="list-unstyled">
                    <li><a href="<?php echo e(route('adminlogin')); ?>">Admin</a></li>
                    <li><a href="#">Testimonials</a></li>
                    <li><a href="#">Terms of Service</a></li>
                    <li><a href="#">Privacy</a></li>
                    <li><a href="#">Contact Us</a></li>
                  </ul>
                </div>
                <div class="col-lg-3">
                  <h2 class="footer-heading mb-4">Resources</h2>
                  <ul class="list-unstyled">
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Testimonials</a></li>
                    <li><a href="#">Terms of Service</a></li>
                    <li><a href="#">Privacy</a></li>
                    <li><a href="#">Contact Us</a></li>
                  </ul>
                </div>
                <div class="col-lg-3">
                  <h2 class="footer-heading mb-4">Support</h2>
                  <ul class="list-unstyled">
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Testimonials</a></li>
                    <li><a href="#">Terms of Service</a></li>
                    <li><a href="#">Privacy</a></li>
                    <li><a href="#">Contact Us</a></li>
                  </ul>
                </div>
                <div class="col-lg-3">
                  <h2 class="footer-heading mb-4">Company</h2>
                  <ul class="list-unstyled">
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Testimonials</a></li>
                    <li><a href="#">Terms of Service</a></li>
                    <li><a href="#">Privacy</a></li>
                    <li><a href="#">Contact Us</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <div class="row pt-5 mt-5 text-center">
            <div class="col-md-12">
              <div class="border-top pt-5">
                <p>
              <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
              Copyright &copy;<script>document.write(new Date().getFullYear());</script> All rights reserved | This template is made with <i class="icon-heart text-danger" aria-hidden="true"></i> by <a href="https://colorlib.com" target="_blank" >Colorlib</a>
              <!-- Link back to Colorlib can't be removed. Template is licensed under CC BY 3.0. -->
              </p>
              </div>
            </div>

          </div>
        </div>
      </footer>

    </div>

    <script src="<?php echo e(asset('guest/js/jquery-3.3.1.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/popper.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/bootstrap.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/owl.carousel.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/jquery.sticky.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/jquery.waypoints.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/jquery.animateNumber.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/jquery.fancybox.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/jquery.easing.1.3.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/bootstrap-datepicker.min.js')); ?>"></script>
    <script src="<?php echo e(asset('guest/js/aos.js')); ?>"></script>

    <script src="<?php echo e(asset('guest/js/main.js')); ?>"></script>

  </body>

</html>

<?php /**PATH C:\Laravelprojects\RentHarmony\resources\views/layouts/guestmaster.blade.php ENDPATH**/ ?>